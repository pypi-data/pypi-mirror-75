import asyncio
import json
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger


class AutodoorConsumer():
    def __init__(self):
        self.rocon_logger = rocon_logger
        pass

    async def request_open_autodoor(self, context, autodoor_id):
        RETRY = 10
        INTERVAL = 1000
        request = context.api_site_configuration.request

        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/autodoors/{}/commands'.format(iot_op_url, autodoor_id)

        rtn = False
        for i in range(RETRY):
            try:
                async with request.post(url, json={'action': 'open'}) as r:
                    if r.status == 200:
                        self.rocon_logger.debug('Open Autodoor: {} requested'.format(autodoor_id))
                        rtn = True
                        break

            except Exception as exc:
                self.rocon_logger.error('there is problem while request open autodoor')
                self.rocon_logger.error('Exception occurred', exception=exc)

            await asyncio.sleep(INTERVAL/1000)

        return rtn

    async def request_close_autodoor(self, context, autodoor_id):
        RETRY = 10
        INTERVAL = 1000
        request = context.api_site_configuration.request

        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/autodoors/{}/commands'.format(iot_op_url, autodoor_id)

        rtn = False
        for i in range(RETRY):
            try:
                async with request.post(url, json={'action': 'close'}) as r:
                    if r.status == 200:
                        self.rocon_logger.debug('Close Autodoor: {} requested'.format(autodoor_id))
                        rtn = True
                        break

            except Exception as exc:
                self.rocon_logger.error('there is problem while request close autodoor')
                self.rocon_logger.error('Exception occurred', exception=exc)

            await asyncio.sleep(INTERVAL/1000)

        return rtn

    async def ensure_autodoor_opened(self, context, autodoor_id):
        RETRY = 20
        INTERVAL = 1000
        request = context.api_site_configuration.request

        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/autodoors/{}'.format(iot_op_url, autodoor_id)

        rtn = False
        for i in range(RETRY):
            try:
                async with request.get(url) as r:
                    if r.status == 200:
                        json_data = await r.json()
                        if json_data['status'] == 'OPENED':
                            rtn = True
                            break

                        self.rocon_logger.debug('Status of Autodoor: {} is {} it\'s not match with opened'.format(autodoor_id, json_data))

            except Exception as exc:
                self.rocon_logger.error('there is problem while checking autodoor is open or not')
                self.rocon_logger.error('Exception occurred', exception=exc)


            self.rocon_logger.debug('Check Autodoor : {} open 1000ms later'.format(autodoor_id))
            await asyncio.sleep(INTERVAL / 1000)

        if rtn is False:
            self.rocon_logger.debug('failed to waiting autodoor, exceed timeout')
        return rtn

    async def ensure_autodoor_closed(self, context, autodoor_id):
        RETRY = 20
        INTERVAL = 1000
        request = context.api_site_configuration.request
        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/autodoors/{}'.format(iot_op_url, autodoor_id)

        rtn = False
        for i in range(RETRY):
            try:
                async with request.get(url) as r:
                    if r.status == 200:
                        json_data = await r.json()
                        if json_data['status'] == 'CLOSED':
                            rtn = True
                            break

                        self.rocon_logger.debug('Status of Autodoor: {} is {} it\'s not match with opened'.format(autodoor_id, json_data))

            except Exception as exc:
                self.rocon_logger.error('there is problem while checking autodoor is open or not')
                self.rocon_logger.error('Exception occurred', exception=exc)


            self.rocon_logger.debug('Check Audtodoor: {} open 1000ms later'.format(autodoor_id))
            await asyncio.sleep(INTERVAL / 1000)

        if rtn is False:
            self.rocon_logger.debug('failed to waiting autodoor, exceed timeout')
        return rtn

    async def get_status(self, context, autodoor_id):

        request = context.api_site_configuration.request
        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/autodoors/{}'.format(iot_op_url, autodoor_id)

        rtn = False

        try:
            async with request.get(url) as r:
                if r.status == 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('Autodoor({}) Status : {}'.format(autodoor_id, json_data))
                    rtn = True
                else:
                    self.rocon_logger.error('err : {}'.format(r))

        except Exception as exc:
            self.rocon_logger.error('there is problem while request get_status of autodoor')
            self.rocon_logger.error('Exception occurred', exception=exc)

        return rtn

    async def request_autodoor_action(self, context, autodoor_id, action='open'):

        request = context.api_site_configuration.request
        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/autodoors/{}/door'.format(iot_op_url, autodoor_id)

        rtn = False

        try:
            req_json_body=json.dumps({
                'action': action,
                'relayId': 1
            })
            self.rocon_logger.debug('request json_body : {}'.format(req_json_body))

            async with request.post(url, json=req_json_body) as r:
                if r.status == 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('Autodoor({}) {} : {}'.format(autodoor_id, action, json_data))
                    rtn = True
                else:
                    self.rocon_logger.error('err : {}'.format(r))

        except Exception as exc:
            self.rocon_logger.error('there is a problem while request autodoor action({})'.format(action))
            self.rocon_logger.error('Exception occurred', exception=exc)

        return rtn