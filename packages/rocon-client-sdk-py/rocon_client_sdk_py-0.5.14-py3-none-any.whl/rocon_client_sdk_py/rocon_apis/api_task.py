import json
from .api import Api
from rocon_client_sdk_py.const import *


class ApiTask(Api):

    @property
    def hostname(self):
        return self._httpclient.hostname_concert

    async def init_task(self, worker_id, task_body):
        task_body['worker'] = worker_id
        return await self.upsert(task_body)

    async def upsert(self, req_body):
        request = self._httpclient.request()
        url = self._httpclient.scheduler_url('/tasks/')

        """
        req_body = {
            "name": "7th_floor_delivery(v)",
            "description": "same with real_delivery but difference domains (like locations)",
            "actions": [
                {
                    "func_name": "undock",
                    "args": [],
                    "fixed": False
                },
                {
                    "func_name": "move",
                    "args": [
                        {
                            "key": "destination",
                            "type": "string",
                            "value": None,
                            "domain": [
                                "homebase",
                                "1@7@etri12b",
                                "1-2@7@etri12b",
                                "1-3@7@etri12b",
                                "1-4@7@etri12b",
                                "3@7@etri12b",
                                "4@7@etri12b",
                                "5@7@etri12b",
                                "6@7@etri12b",
                                "7@7@etri12b",
                                "8@7@etri12b",
                                "10@7@etri12b",
                                "10@7@etri12b",
                                "10@7@etri12b"
                            ],
                            "default": "homebase"
                        },
                        {
                            "key": "gesture",
                            "type": "string",
                            "value": None,
                            "domain": [
                                "confirming",
                                "rf_auth",
                                "move"
                            ]
                        }
                    ],
                    "fixed": False
                },
                {
                    "func_name": "dock",
                    "args": [
                        {
                            "key": "destination",
                            "type": "string",
                            "value": None,
                            "domain": [
                                "homebase",
                                "charging_station_1",
                                "in_hell_fire",
                                "nearest"
                            ],
                            "default": "homebase"
                        },
                        {
                            "key": "gesture",
                            "type": "string",
                            "value": None,
                            "domain": []
                        }
                    ],
                    "fixed": False
                }
            ],
            "fixed": False,
            "worker": "5948e00718a0b0c51b0f38ca"
        }
        """

        req_json_body = json.dumps(req_body)

        self.rocon_logger.debug('request.put > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:

            headers = {'Content-type': 'application/json'}
            async with request.put(url, data=req_json_body, headers = headers) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data
