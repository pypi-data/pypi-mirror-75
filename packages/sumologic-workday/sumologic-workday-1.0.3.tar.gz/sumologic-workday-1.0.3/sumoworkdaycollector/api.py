import signal
import sys
import traceback
import re
import time
from datetime import datetime, timedelta
from sumoappclient.sumoclient.base import BaseAPI
from sumoappclient.sumoclient.httputils import ClientMixin
from sumoappclient.common.utils import get_current_timestamp, convert_date_to_epoch, convert_utc_date_to_epoch
from sumoappclient.sumoclient.factory import OutputHandlerFactory
from requests.auth import HTTPBasicAuth


def convert_epoch_to_utc_isoformat_date(timestamp, milliseconds=False):
    # https://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
    try:
        if milliseconds:
            timestamp = timestamp/1000.0
        date_str = datetime.utcfromtimestamp(timestamp).isoformat()
    except Exception as e:
        raise Exception(f'''Error in converting timestamp {timestamp}''')

    return date_str


class WorkdayAPI(BaseAPI):

    MOVING_WINDOW_DELTA = 0.001
    isoformat = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, kvstore, config, api_url):
        super(WorkdayAPI, self).__init__(kvstore, config)
        self.api_config = self.config['Workday_API_Config']
        self.api_url = api_url
        self.api_name = api_url.split("/")[-1]
        self.tenant_name = self.api_config['WORKDAY_REST_API_ENDPOINT'].split("/")[-1]
        self.source_name = self.api_name.lower()
        self.pathname = f'''{self.source_name}.json'''
        self._validate_urls(self.api_config["WORKDAY_REST_API_ENDPOINT"], self.api_config["REFRESH_TOKEN_ENDPOINT"])
        self.current_state = self.get_state()
        signal.signal(signal.SIGINT, self.exit_gracefully)  # for Ctrl-C
        signal.signal(signal.SIGTERM, self.exit_gracefully) # kill command
        self.workdaysess = ClientMixin.get_new_session(MAX_RETRY=self.collection_config['MAX_RETRY'],
                                                       BACKOFF_FACTOR=self.collection_config['BACKOFF_FACTOR'])
        self.STOP_TIME_OFFSET_SECONDS += self.api_config['API_CALL_DELAY_SECONDS']

    def get_window(self, last_event_time_epoch):
        start_time_epoch = last_event_time_epoch + self.MOVING_WINDOW_DELTA
        end_time_epoch = get_current_timestamp() - self.collection_config['END_TIME_EPOCH_OFFSET_SECONDS']

        # initially last_event_time_epoch is same as current_time_stamp so endtime becomes lesser than starttime

        while not (end_time_epoch - start_time_epoch > 2):
            end_time_epoch = int((start_time_epoch + get_current_timestamp())/2)

        return start_time_epoch, end_time_epoch

    def _refresh_access_token(self):
        status, data = ClientMixin.make_request(self.api_config["REFRESH_TOKEN_ENDPOINT"], method="post",
                                                session=self.workdaysess, logger=self.log,
                                                TIMEOUT=self.api_config['TIMEOUT'], MAX_RETRY=self.collection_config['MAX_RETRY'],
                                                BACKOFF_FACTOR=self.collection_config['BACKOFF_FACTOR'],
                                                auth = (self.api_config["CLIENT_ID"], self.api_config["CLIENT_SECRET"]),
                                                data = {"refresh_token": self.api_config["REFRESH_TOKEN"],
                                                        "grant_type": "refresh_token" })
        if not status:
            raise Exception("Not able to retrieve access_token %s" % data)
        elif "access_token" in data:
            self.log.debug("Refresh Token generated: %s" % data["access_token"])
            return data["access_token"]
        else:
            raise ValueError("'access_token' field not returned in successful response")

    def _validate_urls(self, rest_api_endpoint, token_endpoint):
        REST_API_ENDPOINT_PATTERN = re.compile("^https://(?P<host>[^/:]+)(?::\d+)?/ccx/api/v1/(?P<tenant>[^/]+)$")
        TOKEN_ENDPOINT_PATTERN = re.compile("^https://(?P<host>[^/:]+)(?::\d+)?/ccx/oauth2/(?P<tenant>[^/]+)/token$")

        # Validate url patterns
        match = REST_API_ENDPOINT_PATTERN.match(rest_api_endpoint)
        if not match:
            raise ValueError("REST API Endpoint must match the format \"https://<hostname>/ccx/api/v1/<tenant>\"")
        else:
            base_url_groups = match.groupdict()

        match = TOKEN_ENDPOINT_PATTERN.match(token_endpoint)
        if not match:
            raise ValueError("Token Endpoint must match the format \"https://<hostname>/ccx/oauth2/<tenant>/token\"")
        else:
            token_url_groups = match.groupdict()

        # Validate both urls are from the same environment / tenant
        if base_url_groups["host"] != token_url_groups["host"]:
            raise ValueError("REST API Endpoint and Token Endpoint hostnames do not match")
        if base_url_groups["tenant"] != token_url_groups["tenant"]:
            raise ValueError("REST API Endpoint and Token Endpoint tenant ids do not match")

    def fetch(self):
        log_type = self.get_key()
        next_request = True
        count = 0
        total = kwargs = None
        try:
            output_handler = OutputHandlerFactory.get_handler(self.collection_config['OUTPUT_HANDLER'],
                                                              path=self.pathname,
                                                              config=self.config)
            url, kwargs = self.build_fetch_params()
            self.log.info(
                f'''Fetching LogType: {log_type}  starttime: {kwargs['params']['from']} endtime: {kwargs['params'][
                    'to']} Offset: {kwargs['params']['offset']}''')

            while next_request:
                has_error = False
                send_success = has_next_page = False
                status, data = ClientMixin.make_request(url, method="get", session=self.workdaysess, logger=self.log,
                                                        TIMEOUT=self.api_config['TIMEOUT'],
                                                        MAX_RETRY=self.collection_config['MAX_RETRY'],
                                                        BACKOFF_FACTOR=self.collection_config['BACKOFF_FACTOR'],
                                                        **kwargs)
                fetch_success = status and "data" in data
                if fetch_success:
                    total = int(data["total"])
                    has_next_page = kwargs['params']['offset'] < total
                    num_fetched_items = len(data["data"])
                    if num_fetched_items > 0:
                        payload = self.transform_data(data["data"])
                        if len(payload) > 0:
                            params = self.build_send_params()
                            send_success = output_handler.send(payload, **params)
                        else:
                            self.log.info("No data to send after filtering")
                            send_success = True
                        if send_success:
                            count += 1
                            kwargs['params']['offset'] += num_fetched_items

                            # update state only after sending to sumo
                            self.current_state.update(self.get_updated_state(payload, self.current_state))
                            self.log.debug(f'''Successfully sent LogType: {log_type} Offset: {kwargs['params'][
                                'offset']}  Datalen: {len(payload)} starttime: {kwargs['params']['from']} endtime: {
                            kwargs['params']['to']} last_event_time: {convert_epoch_to_utc_isoformat_date(self.current_state['last_event_time_epoch'])}''')

                            # time not available save current state new page num else continue
                            # not saving on every successful send to optimize on network call
                            if not self.is_time_remaining():
                                self.save_state()

                        else:
                            # show err unable to send save current state
                            has_error = True
                            self.log.error(
                                f'''Failed to send LogType: {log_type} Offset: {kwargs['params']['offset']} starttime: {
                                kwargs['params']['from']} endtime: {kwargs['params']['to']} last_event_time: {convert_epoch_to_utc_isoformat_date(self.current_state['last_event_time_epoch'])}''')
                    else:
                        self.log.debug(f'''Moving starttime window LogType: {log_type} Offset: {kwargs['params'][
                            'offset']} starttime: {kwargs['params']['from']} endtime: {kwargs['params'][
                            'to']} response: {data} last_event_time: {convert_epoch_to_utc_isoformat_date(self.current_state['last_event_time_epoch'])}''')

                        # genuine no result window no change
                        # page_num has finished increase window save last_event_time_epoch and resetting offset
                        if kwargs['params']['offset'] >= 0:
                            self.current_state = {"offset": -1, "last_event_time_epoch": self.current_state['last_event_time_epoch']}
                            self.save_state()

                else:
                    has_error = True
                    self.log.error(f'''Failed to fetch LogType: {log_type} Offset: {kwargs['params'][
                        'offset']} Reason: {data} starttime: {kwargs['params']['from']} endtime: {kwargs['params'][
                        'to']} last_event_time: {convert_epoch_to_utc_isoformat_date(self.current_state['last_event_time_epoch'])}''')

                if has_error:
                    self.save_state()

                next_request = (not has_error) and has_next_page and self.is_time_remaining()
                self.log.debug(f''' NextRequest: {next_request} HasNextpage: {has_next_page} Total: {total}''')
                if next_request:
                    self.log.debug(f'''Sleeping for {self.api_config['API_CALL_DELAY_SECONDS']} seconds ...''')
                    time.sleep(self.api_config['API_CALL_DELAY_SECONDS'])
        finally:
            self.workdaysess.close()
            self.log.info(
                f'''Completed LogType: {log_type} RequestCount: {count} Offset: {self.current_state['offset']} kwargs: {kwargs} last_event_time: {convert_epoch_to_utc_isoformat_date(self.current_state['last_event_time_epoch'])}''')

    def get_key(self):
        key = f'''{self.tenant_name}-{self.api_name}'''
        return key

    def save_state(self):
        key = self.get_key()
        self.kvstore.set(key, self.current_state)

    def exit_gracefully(self, signum, frame):
        self.log.info("Exiting Gracefully killed by SignalNum: %s" % signum)
        self.save_state()
        sys.exit(0)

    def get_state(self):
        key = self.get_key()
        if not self.kvstore.has_key(key):
            self.current_state = {"last_event_time_epoch": self.DEFAULT_START_TIME_EPOCH, "offset": -1}
            self.save_state()
        obj = self.kvstore.get(key)
        return obj

    def build_fetch_params(self):
        # Todo can be optimized ask what's the time limit of access token expiry

        if self.current_state["offset"] == -1:
            self.current_state['start_time_epoch'], self.current_state['end_time_epoch'] = self.get_window(self.current_state['last_event_time_epoch'])
            self.current_state['offset'] = 0

        access_token = self._refresh_access_token()
        start_time_date = convert_epoch_to_utc_isoformat_date(self.current_state['start_time_epoch'])
        end_time_date = convert_epoch_to_utc_isoformat_date(self.current_state['end_time_epoch'])
        url = f'''{self.api_config['WORKDAY_REST_API_ENDPOINT']}{self.api_url}'''
        request_params = {
            "headers": {
              "Authorization": "Bearer {}".format(access_token),
              "Content-Type": "application/json"
            },
            "params": {
                "from": start_time_date,
                "to": end_time_date,
                "offset": self.current_state['offset'],
                "limit": self.api_config['PAGINATION_LIMIT']
            }
        }
        if "audit" in self.api_url:
            request_params['params']["type"] = "userActivity"

        return url, request_params

    def build_send_params(self):
        return {
            "extra_headers": {"X-Sumo-Name": self.source_name},
            "endpoint_key": "HTTP_LOGS_ENDPOINT"
        }

    def get_updated_state(self, data, current_state):
        last_event_time_epoch = convert_utc_date_to_epoch(data[0]["requestTime"], date_format=self.isoformat) if len(
            data) > 0 else None
        for item in data:
            current_timestamp = convert_utc_date_to_epoch(item["requestTime"], date_format=self.isoformat)
            last_event_time_epoch = max(current_timestamp, last_event_time_epoch)
        return {"last_event_time_epoch": last_event_time_epoch, "offset": current_state["offset"] + len(data)}

    def transform_data(self, content):
        modified_data = []
        blacklisted_data_count = 0
        black_listing_enabled = "audit" in self.api_url and self.api_config.get("BLACKLIST_TASK_NAMES", [])
        for item in content:
            item["tenant_name"] = self.tenant_name
            if black_listing_enabled:
                if not isinstance(self.api_config["BLACKLIST_TASK_NAMES"], list):
                    raise Exception("BLACKLIST_TASK_NAMES in config file should be a list")
                if item["taskDisplayName"] not in self.api_config["BLACKLIST_TASK_NAMES"]:
                    modified_data.append(item)
                else:
                    blacklisted_data_count += 1
            else:
                modified_data.append(item)

        if black_listing_enabled:
            self.log.info("Blacklisted Data Count: %d" % blacklisted_data_count)
        return modified_data


class WorkdayReport(BaseAPI):

    MOVING_WINDOW_DELTA = 0.001
    INTERVAL_INCREMENT_IF_NO_DATA = 60*60 #60*60*24

    def __init__(self, kvstore, config, report_url, REPORT_CONFIG_NAME='Workday_Report_Config', DATETIME_FIELD="Session_Start", SOURCE_NAME="signonlogs"):
        super(WorkdayReport, self).__init__(kvstore, config)

        self.report_name = report_url.split("/")[-1]
        self.tenant_name = report_url.split("/")[-3]
        self.report_url = report_url
        self.report_config = self.config[REPORT_CONFIG_NAME]
        self.source_name = SOURCE_NAME
        self.DATETIME_FIELD = DATETIME_FIELD
        self.pathname = f'''{self.source_name}.json'''
        self.current_state = self.get_state()
        signal.signal(signal.SIGINT, self.exit_gracefully)  # for Ctrl-C
        signal.signal(signal.SIGTERM, self.exit_gracefully)  # kill command
        self.workdaysess = ClientMixin.get_new_session(MAX_RETRY=self.collection_config['MAX_RETRY'],
                                                       BACKOFF_FACTOR=self.collection_config['BACKOFF_FACTOR'])
        self.STOP_TIME_OFFSET_SECONDS += self.report_config['API_CALL_DELAY_SECONDS']

    def get_window(self, last_event_time_epoch, interval):
        start_time_epoch = last_event_time_epoch + self.MOVING_WINDOW_DELTA
        end_time_epoch = min(start_time_epoch + interval, get_current_timestamp() - self.collection_config['END_TIME_EPOCH_OFFSET_SECONDS'])

        # initially last_event_time_epoch is same as current_time_stamp so endtime becomes lesser than starttime
        while not (end_time_epoch - start_time_epoch > 2):
            end_time_epoch = int((start_time_epoch + get_current_timestamp())/2)

        return start_time_epoch, end_time_epoch

    def fetch(self):
        log_type = self.get_key()
        next_request = True
        count = 0
        total = None
        try:
            output_handler = OutputHandlerFactory.get_handler(self.collection_config['OUTPUT_HANDLER'],
                                                              path=self.pathname,
                                                              config=self.config)

            max_end_time_epoch = get_current_timestamp() - self.collection_config['END_TIME_EPOCH_OFFSET_SECONDS']
            while next_request:
                url, kwargs = self.build_fetch_params()
                self.log.info(
                    f'''Fetching LogType: {log_type}  starttime: {kwargs['params']['From_Moment']} endtime: {kwargs['params'][
                        'To_Moment']} FetchInterval: {self.current_state["fetch_interval"]}''')

                has_error = False
                send_success = False
                status, data = ClientMixin.make_request(self.report_url, method="get",
                                                        session=self.workdaysess, logger=self.log,
                                                        TIMEOUT=self.report_config['TIMEOUT'],
                                                        MAX_RETRY=self.collection_config['MAX_RETRY'],
                                                        BACKOFF_FACTOR=self.collection_config['BACKOFF_FACTOR'],
                                                        **kwargs)

                fetch_success = status and "Report_Entry" in data
                if fetch_success:

                    num_fetched_items = len(data["Report_Entry"])
                    if num_fetched_items > 0:
                        payload = self.transform_data(data["Report_Entry"])
                        params = self.build_send_params()
                        send_success = output_handler.send(payload, **params)
                        if send_success:
                            count += 1

                            # increase by 2 till max
                            self.current_state["fetch_interval"] = min(self.current_state["fetch_interval"]*2, self.report_config["MAX_FETCH_INTERVAL"])

                            # update state only after sending to sumo
                            self.current_state.update(self.get_updated_state(payload, self.current_state))
                            self.log.debug(f'''Successfully sent LogType: {log_type}  Datalen: {len(payload)
                            } starttime: {kwargs['params']['From_Moment']} endtime: {kwargs['params']['To_Moment']
                            } last_event_time: {convert_epoch_to_utc_isoformat_date(self.current_state['last_event_time_epoch'])
                            } FetchInterval: {self.current_state["fetch_interval"]}''')

                            # time not available save current state new page num else continue
                            # not saving on every successful send to optimize on network call
                            if not self.is_time_remaining():
                                self.save_state()

                        else:
                            # show err unable to send save current state
                            has_error = True
                            self.log.error(
                                f'''Failed to send LogType: {log_type} starttime: {
                                kwargs['params']['From_Moment']} endtime: {kwargs['params'][
                                    'To_Moment']} last_event_time: {convert_epoch_to_utc_isoformat_date(
                                    self.current_state['last_event_time_epoch'])} FetchInterval: {self.current_state["fetch_interval"]}''')
                    else:
                        self.log.debug(f'''No Result Found LogType: {log_type} starttime: {kwargs['params']['From_Moment']} endtime: {kwargs['params'][
                            'To_Moment']} response: {data} last_event_time: {convert_epoch_to_utc_isoformat_date(
                            self.current_state['last_event_time_epoch'])} FetchInterval: {self.current_state["fetch_interval"]}''')

                        # genuine no result window no change or
                        # page_num has finished increase window calc last_event_time_epoch and resetting offset

                        self.current_state = {"last_event_time_epoch": self.current_state['last_event_time_epoch'],
                                                  "fetch_interval": self.current_state["fetch_interval"] + self.INTERVAL_INCREMENT_IF_NO_DATA}
                        self.save_state()

                else:
                    has_error = True
                    self.log.error(f'''Failed to fetch LogType: {log_type} Offset: {kwargs['params'][
                        'offset']} Reason: {data} starttime: {kwargs['params']['From_Moment']} endtime: {kwargs['params'][
                        'To_Moment']} last_event_time: {convert_epoch_to_utc_isoformat_date(
                        self.current_state['last_event_time_epoch'])}''')

                    # decrease by 2 in case more than 2GB
                    # Todo ask status code
                    self.current_state["fetch_interval"] = max(self.current_state["fetch_interval"] / 2,
                                                               self.report_config["MIN_FETCH_INTERVAL"])
                if has_error:
                    self.save_state()

                _, end_time_epoch = self.get_window(self.current_state["last_event_time_epoch"],
                                                                       self.current_state['fetch_interval'])
                has_next_page = end_time_epoch < max_end_time_epoch
                next_request = (not has_error) and has_next_page and self.is_time_remaining()

                self.log.debug(f''' NextRequest: {next_request} HasNextpage: {has_next_page} Total: {total}''')
                if next_request:
                    self.log.debug(f'''Sleeping for {self.report_config['API_CALL_DELAY_SECONDS']} seconds ...''')
                    time.sleep(self.report_config['API_CALL_DELAY_SECONDS'])
        finally:
            self.workdaysess.close()
            self.log.info(f'''Completed LogType: {log_type} RequestCount: {count} FetchInterval: {self.current_state["fetch_interval"]} last_event_time: {convert_epoch_to_utc_isoformat_date(
                    self.current_state['last_event_time_epoch'])}''')

    def get_key(self):
        key = f'''{self.tenant_name}-{self.report_name}'''
        return key

    def save_state(self):
        key = self.get_key()
        self.kvstore.set(key, self.current_state)

    def exit_gracefully(self, signum, frame):
        self.log.info("Exiting Gracefully killed by SignalNum: %s" % signum)
        self.save_state()
        sys.exit(0)

    def get_state(self):
        key = self.get_key()
        if not self.kvstore.has_key(key):
            self.current_state = {"last_event_time_epoch": self.DEFAULT_START_TIME_EPOCH, "fetch_interval": self.report_config["MAX_FETCH_INTERVAL"]}
            self.save_state()
        obj = self.kvstore.get(key)
        return obj

    def build_fetch_params(self):
        start_time_epoch, end_time_epoch = self.get_window(self.current_state["last_event_time_epoch"], self.current_state['fetch_interval'])
        start_time_date = convert_epoch_to_utc_isoformat_date(start_time_epoch)
        end_time_date = convert_epoch_to_utc_isoformat_date(end_time_epoch)
        request_params = {
            "headers": {
              "Content-Type": "application/json"
            },
            "params": {
                "From_Moment": start_time_date,
                "To_Moment": end_time_date,
                "format": "json"
            },
            "auth": HTTPBasicAuth(username=self.report_config["ISU_USERNAME"],
                             password=self.report_config["ISU_PASSWORD"]),
        }

        return self.report_url, request_params

    def build_send_params(self):
        return {
            "extra_headers": {"X-Sumo-Name": self.source_name},
            "endpoint_key": "HTTP_LOGS_ENDPOINT"
        }

    def get_updated_state(self, data, current_state):

        last_event_time_epoch = convert_date_to_epoch(data[0][self.DATETIME_FIELD]) if len(
            data) > 0 else None
        for item in data:
            current_timestamp = convert_date_to_epoch(item[self.DATETIME_FIELD])
            last_event_time_epoch = max(current_timestamp, last_event_time_epoch)
        return {"last_event_time_epoch": last_event_time_epoch, "fetch_interval": current_state["fetch_interval"]}

    def transform_data(self, content):
        for item in content:
            item["tenant_name"] = self.tenant_name
        return content
