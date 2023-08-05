import pydash
import json
from .api import Api
from rocon_client_sdk_py.const import *


class ApiWorker(Api):

    @property
    def hostname(self):
        return self._httpclient.hostname_concert

    async def find_one_by_uuid(self, uuid):
        request = self._httpclient.request()
        url = self._httpclient.scheduler_url('/workers?uuid={}'.format(uuid))
        self.rocon_logger.debug('request.get > {}'.format(url), module_keyword=BT_KEYWORD)

        rtn_data = None
        async with request.get(url) as r:
            self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)
            if r.status is 200:
                json_data = await r.json()
                self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                if len(json_data) > 0:
                    rtn_data = json_data[0]
                else:
                    self.rocon_logger.error('Not registered : {}'.format(uuid))
            else:
                self.rocon_logger.error('Error status occurred : {}'.format(r))
                self.error_handling(r)

        if rtn_data is None:
            return None

        return rtn_data

    async def upsert(self, body):
        request = self._httpclient.request()
        req_body = pydash.pick(body, ['status', 'name', 'type_specific', 'release_version', 'type', 'uuid'])
        req_json_body = json.dumps(req_body)

        url = self._httpclient.scheduler_url('/workers/')
        self.rocon_logger.debug('request.put > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:

            async with request.put(url, data=req_json_body) as r:
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


    async def update_worker(self, worker_id, update):
        allowed_update = ['type_specific', 'status', 'name']
        update_body = pydash.pick(update, allowed_update)
        request = self._httpclient.request()
        req_json_body = json.dumps(update_body)
        url = self._httpclient.scheduler_url('/workers/{}'.format(worker_id))
        self.rocon_logger.debug('request.put > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)

                if r.status == 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

                if 'error' in json_data:
                    self.rocon_logger.error('Error Occurred >> {}'.format(json_data))

        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def set_location(self, worker_id, location_info):
        request = self._httpclient.request()
        req_json_body = json.dumps(location_info)
        url = self._httpclient.scheduler_url('/workers/{}'.format(worker_id))
        self.rocon_logger.debug('request.put > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)

                if r.status == 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

                if 'error' in json_data:
                    self.rocon_logger.error('Error Occurred >> {}'.format(json_data))

        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data