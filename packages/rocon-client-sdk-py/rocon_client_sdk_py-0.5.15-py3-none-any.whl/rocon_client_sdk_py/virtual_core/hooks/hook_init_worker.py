import pydash
from rocon_client_sdk_py.core_logic.context import Context
from rocon_client_sdk_py.core_logic.hook_origin_init_worker import HookOriginInitWorker


class HookInitWorker(HookOriginInitWorker):
    def __init__(self):
        super().__init__()

        self._iniitializers = {'battery':self._init_battery, 'location': self._init_location}
        self._validators = {'battery': self._validate_battery, 'location': self._validate_location}

    async def on_handle(self, worker_record):
        uuid = self.context.worker.uuid
        worker_name = self.context.worker.worker_name

        if worker_record is None:
            self.rocon_logger.debug('Cannot found worker ({}) context file. Generate default worker context'.format(uuid))

            worker_record = {}
            worker_record['uuid'] = uuid
            worker_record['name'] = worker_name
            worker_record['type_specific'] = {}

            for item in self._iniitializers:
                worker_record = await self._iniitializers[item](worker_record)

        else:
            worker_record = await self._patch(worker_record)

        return worker_record

    async def _init_battery(self, worker_record):
        type_specific = worker_record['type_specific']
        pydash.set_(type_specific, 'battery',
                    {
                        'battery_level': 75,
                        'charging_status': 0
                    })

        return worker_record

    async def _init_location(self, worker_record):
        stations = await self.context.api_site_configuration.get_stations()
        for s in stations:
            map = await self.context.api_site_configuration.get_maps(s['map'])
            if map:
                type_specific = worker_record['type_specific']

                if 'location' not in type_specific:
                    type_specific['location'] = {}

                pydash.set_(type_specific['location'], 'map', s['map'])
                pydash.set_(type_specific['location'], 'pose2d', s['pose'])
                return worker_record

        assert(False)

    async def _validate_battery(self, worker_record):
        if pydash.get(worker_record['type_specific'], 'battery') is None:
            return {'result': False, 'message': 'battery information is not exist'}

        return {'result': True}

    async def _patch(self, worker_record):
        for item in self._validators:
            check = await self._validators[item](worker_record)
            if check['result'] is False:
                worker_record = await self._iniitializers[item](worker_record)
                self.rocon_logger.debug('validation failed while path() {}:{}'.format(check['message'], {'updated_worker': worker_record}))

        return worker_record

    async def _validate_location(self, worker_record):
        pose = pydash.get(worker_record['type_specific']['location'], 'pose2d')
        map = pydash.get(worker_record['type_specific']['location'], 'map')

        if pose is None:
            return {'result': False, 'message': 'pose information is not loaded correctly'}

        if map is None:
            return {'result': False, 'message': 'map information is not loaded correctly'}

        return {'result': True}
