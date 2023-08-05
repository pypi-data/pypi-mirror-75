import json
import asyncio
from .api import Api
from rocon_client_sdk_py.const import *


class ApiReport(Api):

    @property
    def hostname(self):
        return self._httpclient.hostname_concert

    async def req_recommend(self, worker_id):
        request = self._httpclient.request()
        url = self._httpclient.scheduler_url('/reports/recommend')
        self.rocon_logger.debug('request.post > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:
            async with request.post(url, json={'worker': worker_id}) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.TimeoutError:
            raise
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def req_ownership(self, report_id, worker_id):
        request = self._httpclient.request()

        req_json_body = json.dumps({'worker': worker_id})
        url = self._httpclient.scheduler_url('/reports/{}/ownership'.format(report_id))
        self.rocon_logger.debug('request.put > {}'.format(url))

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.CancelledError as cerr:
            self.rocon_logger.error('Error occurred : {}'.format(cerr), exception=cerr)
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def update_report(self, report_id, update_body):
        if report_id == None:
            self.rocon_logger.debug('report_id is None')
            return None


        request = self._httpclient.request()

        req_json_body = json.dumps(update_body)
        url = self._httpclient.scheduler_url('/reports/{}'.format(report_id))
        #self.rocon_logger.debug('request.put > {}'.format(url), module_keyword=BT_KEYWORD)
        self.rocon_logger.debug('request.put > {}'.format(url))
        self.rocon_logger.debug('req_json_body : {}'.format(req_json_body))

        json_data = None

        try:
            async with request.put(url, data=req_json_body) as r:
                #self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)
                if r.status is 200:
                    json_data = await r.json()
                    #self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    #self.error_handling(r)

        except asyncio.CancelledError as cerr:
            self.rocon_logger.error('Error occurred : {}'.format(cerr), exception=cerr)
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        del req_json_body
        return json_data

    async def get_reports(self, options):
        request = self._httpclient.request()

        url = self._httpclient.scheduler_url('/reports')
        self.rocon_logger.debug('request.get > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:
            async with request.get(url, params=options) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def get_report_by_id(self, report_id):
        request = self._httpclient.request()

        url = self._httpclient.scheduler_url('/reports/{}'.format(report_id))
        self.rocon_logger.debug('request.get > {}'.format(url), module_keyword=BT_KEYWORD)

        json_data = None
        try:
            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status), module_keyword=BT_KEYWORD)
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data), module_keyword=BT_KEYWORD)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.CancelledError as cerr:
            self.rocon_logger.error('Error occurred : {}'.format(cerr), exception=cerr)
        except Exception as exc:

            if r.status is 404:
                return None
            else:
                self.rocon_logger.error('unhandled error on get_report_by_id')

            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def cancel_report(self, report_id, message, force=False):
        request = self._httpclient.request()

        req_json_body = json.dumps({'message': message, 'force': force})
        url = self._httpclient.scheduler_url('/reports/{}/cancel'.format(report_id))
        self.rocon_logger.debug('request.put > {}'.format(url))

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.CancelledError as cerr:
            self.rocon_logger.error('Error occurred : {}'.format(cerr), exception=cerr)
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def abort_report(self, report_id, message):
        request = self._httpclient.request()
        req_json_body = json.dumps({'message': message})
        url = self._httpclient.scheduler_url('/reports/{}/abort'.format(report_id))
        self.rocon_logger.debug('request.put > {}'.format(url))

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.CancelledError as cerr:
            self.rocon_logger.error('Error occurred : {}'.format(cerr), exception=cerr)
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def handle_revision(self, report, propositions, action):
        request = self._httpclient.request()

        report_body = {'action': action, 'propositions': propositions}
        req_json_body = json.dumps(report_body)
        rep = report['id'] if 'id' in report else report
        url = self._httpclient.scheduler_url('/reports/{}/revision'.format(rep))
        self.rocon_logger.debug('request.put > {}'.format(url))

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    #self.rocon_logger.debug('response data > \n{}'.format(json_data))
                    self.rocon_logger.debug('response data ok')
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except asyncio.CancelledError as cerr:
            self.rocon_logger.error('Error occurred : {}'.format(cerr), exception=cerr)
        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data

    async def approve_revision(self, report):
        return await self.handle_revision(report['id'], report['revision']['propositions'], 'approve')

    async def reject_revision(self, report):
        return await self.handle_revision(report['id'], report['revision']['propositions'], 'reject')