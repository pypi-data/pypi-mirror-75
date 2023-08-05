import asyncio
import pydash
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger

STATUS = {
    'initializing': 'INITIALIZING',
    'idle': 'IDLE',
    'error': 'ERROR',
    'toDeparture': 'TO_DEPARTURE',
    'onDeparture': 'ON_DEPARTURE',
    'toDestination': 'TO_DESTINATION',
    'onDestination': 'ON_DESTINATION'
}


class ElevatorConsumer():
    def __init__(self):
        self.rocon_logger = rocon_logger
        pass

    def is_door_open(self, status):
        return status == STATUS['onDeparture'] or status == STATUS['onDestination']

    async def ensure_elevator(self, context, teleported_id, status):
        TIMEOUT = 5*60*1000
        CHECKING_INTERVAL = 1000

        request = context.api_site_configuration.request
        url = context.api_site_configuration.get_url(
            'temp.iot_operator/facilities/elevators/{}'.format(teleported_id))

        rtn = False
        for i in range(TIMEOUT/CHECKING_INTERVAL):
            try:
                async with request.post(url, json={'action': 'open'}) as r:
                    if r.status == 200:
                        json_data = await r.json()
                        if json_data['status'] == status:
                            self.rocon_logger.debug('elevator status is {}'.format(status))
                            rtn = True
                            break

            except Exception as exc:
                self.rocon_logger.error('there is problem while request open autodoor')
                self.rocon_logger.error('Exception occurred', exception=exc)

            await asyncio.sleep(CHECKING_INTERVAL/1000)

        if rtn is False:
            self.rocon_logger.debug('failed to waiting for keep opening elevator door: timeout exceed')
        return rtn

    async def call_elevator(self, context, teleporter, departure_gate, destination_gate):
        request = context.api_site_configuration.request

        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/elevators/{}/services'.format(iot_op_url, teleporter['id'])

        req_body={
            'departure_floor': str(pydash.get(departure_gate, 'properties.floor_id')),
            'destination_floor': str(pydash.get(destination_gate, 'properties.floor_id'))
        }

        if 'departure_floor' not in req_body or 'destination_floor' not in req_body:
            raise Exception('req body for calling elevator is not enough, {}'.format(req_body))

        rtn_data = None
        try:
            async with request.post(url, json=req_body) as r:
                if r.status == 200:
                    json_data = await r.json()
                    rtn_data = json_data['serviceId']
                else:
                    self.rocon_logger.debug('response not success while calling Elevator')
                    raise Exception('response not success while calling Elevator')

        except Exception as exc:
            self.rocon_logger.error('call_elevator() failed')
            self.rocon_logger.error('Exception occurred', exception=exc)

        return rtn_data

    async def ensure_elevator_door_open(self, context, teleporter_id):
        RETRY = 10
        RETRY_INTERVAL_MS = 1000

        for i in range(RETRY):

            rtn, json_data = await self.check_elevator_status(context, teleporter_id)
            if rtn == True and self.is_door_open(json_data['status']) == True:
                self.rocon_logger.debug('elevator door keep opening detected')
                return True

            await asyncio.sleep(RETRY_INTERVAL_MS / 1000)


        if rtn is False:
            self.rocon_logger.debug('failed waiting for keep opening elevator door: timeout exceed')
        return rtn

    async def close_elevator_door(self, context, teleported_id, service_id, message, result):
        RETRY = 10
        RETRY_INTERVAL = 1000

        request = context.api_site_configuration.request
        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/elevators/{}/services/{}/messages'.format(iot_op_url, teleported_id, service_id)

        desire_status = None
        if message == 'board':
            desire_status = STATUS['onDeparture']
        elif message == 'unboard':
            desire_status = STATUS['onDestination']

        if desire_status is None:
            raise Exception('unkown message to close_elevator_door: {}'.format(message))

        req_body = {
            'message': message,
            'status': desire_status,
            'result': result
        }

        rtn = False
        for i in range(RETRY):
            try:
                async with request.post(url, json=req_body) as r:
                    if r.status == 200:
                        rtn = True
                        break
                    else:
                        self.rocon_logger.debug('there is a problem while request close_elevator_door : {}'.format(r.status))

            except Exception as exc:
                self.rocon_logger.error('there is a problem while request close_elevator_door')
                self.rocon_logger.error('Exception occurred', exception=exc)


            await asyncio.sleep(RETRY_INTERVAL/1000)

        if rtn is False:
            self.rocon_logger.debug('failed to request close elevator door: maximum retry exceed')

        return rtn

    async def ensure_elevator_door_closed(self, context, teleporter_id):
        RETRY = 10
        RETRY_INTERVAL_MS = 1000

        for i in range(RETRY):

            rtn, json_data = await self.check_elevator_status(context, teleporter_id)
            if rtn == True and self.is_door_open(json_data['status']) == False:
                return True

            await asyncio.sleep(RETRY_INTERVAL_MS / 1000)

        self.rocon_logger.debug('failed to ensure elevator door closed: maximum retry exceed')
        return False

    async def check_elevator_status(self, context, teleporter_id):
        request = context.api_site_configuration.request
        worker = context.worker
        iot_op_url = worker._configs['temp']['iot_operator']
        url = 'http://{}/facilities/elevators/{}'.format(iot_op_url, teleporter_id)

        json_data = None
        rtn = False
        try:
            async with request.get(url) as r:
                if r.status == 200:
                    json_data = await r.json()
                    rtn = True
                else:
                    self.rocon_logger.debug('there is a problem while request close_elevator_door : {}'.format(r.status))
                    rtn = False

        except Exception as exc:
            self.rocon_logger.error('there is problem while request ensure_elevator_door_closed')
            self.rocon_logger.error('Exception occurred', exception=exc)

        return rtn, json_data