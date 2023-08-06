# -*- coding: future_fstrings -*-

import traceback
import os
from concurrent import futures
from random import shuffle
from sumoappclient.sumoclient.base import BaseCollector
from api import WorkdayAPI, WorkdayReport


class WorkdayCollector(BaseCollector):
    SINGLE_PROCESS_LOCK_KEY = 'is_workdaycollector_running'
    CONFIG_FILENAME = "sumoworkdaycollector.yaml"
    DATA_REFRESH_TIME = 60*60*1000

    def __init__(self):
        self.project_dir = self.get_current_dir()
        super(WorkdayCollector, self).__init__(self.project_dir)
        #Todo Ask Default Retention
        if self.collection_config["BACKFILL_DAYS"] > 1:
            self.log.warning("Backfill days > 1 is not supported")
            self.collection_config["BACKFILL_DAYS"] = 1

    def get_current_dir(self):
        cur_dir = os.path.dirname(__file__)
        return cur_dir

    def is_running(self):
        self.log.debug("Acquiring single instance lock")
        return self.kvstore.acquire_lock(self.SINGLE_PROCESS_LOCK_KEY)

    def stop_running(self):
        self.log.debug("Releasing single instance lock")
        return self.kvstore.release_lock(self.SINGLE_PROCESS_LOCK_KEY)

    def build_task_params(self):

        tasks = []

        if "Workday_Report_Config" in self.config:
            tasks.append(WorkdayReport(self.kvstore, self.config, self.config['Workday_Report_Config']['SIGNON_REPORT_URL']))

        if "Workday_API_Config" in self.config:
            tasks.append(WorkdayAPI(self.kvstore, self.config, self.config["Workday_API_Config"]["AUDIT_API_URL"]))

        # for handling any other report
        # for k, v in self.config.items():
        #     if k.endswith("Report_Config") and k != "Workday_Report_Config":
        #         report_url = self.config[k].get("REPORT_URL")
        #         source_name = self.config[k].get("SOURCE_NAME")
        #         datetime_field = self.config[k].get("DATETIME_FIELD")
        #         if report_url and source_name and datetime_field:
        #             tasks.append(WorkdayReport(self.kvstore, self.config, report_url, REPORT_CONFIG_NAME=k, DATETIME_FIELD=datetime_field, SOURCE_NAME=source_name))

        self.log.info("%d Tasks Generated" % len(tasks))
        return tasks

    def run(self):
        if self.is_running():
            try:
                self.log.info('Starting Workday Forwarder...')
                task_params = self.build_task_params()
                shuffle(task_params)
                all_futures = {}
                self.log.debug("spawning %d workers" % self.config['Collection']['NUM_WORKERS'])
                with futures.ThreadPoolExecutor(max_workers=self.config['Collection']['NUM_WORKERS']) as executor:
                    results = {executor.submit(apiobj.fetch): apiobj for apiobj in task_params}
                    all_futures.update(results)
                for future in futures.as_completed(all_futures):
                    param = all_futures[future]
                    api_type = str(param)
                    try:
                        future.result()
                        obj = self.kvstore.get(api_type)
                    except Exception as exc:
                        self.log.error(f"API Type: {api_type} thread generated an exception: {exc}", exc_info=True)
                    else:
                        self.log.info(f"API Type: {api_type} thread completed {obj}")
            finally:
                self.stop_running()
        else:
            if not self.is_process_running(["sumoworkdaycollector"]):
                self.kvstore.release_lock_on_expired_key(self.SINGLE_PROCESS_LOCK_KEY, expiry_min=10)

    def test(self):
        if self.is_running():
            task_params = self.build_task_params()
            shuffle(task_params)
            try:
                for apiobj in task_params:
                    apiobj.fetch()
                    # print(apiobj.__class__.__name__)
            finally:
                self.stop_running()


def main(*args, **kwargs):

    try:
        ns = WorkdayCollector()
        ns.run()
        # ns.test()
    except BaseException as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()
