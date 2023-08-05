import pydash
from rocon_client_sdk_py.core_logic.action import Action
from rocon_client_sdk_py.virtual_core.components.actuators import Actuator
from rocon_client_sdk_py.utils.waiter import Waiter


class Unlock(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Unlock'
        self.func_name = 'unlock'

    async def on_define(self):
        self.rocon_logger.debug('define the action of {}'.format(self.name))

        act_def = None
        if self.context.worker.use_worker_config_server:
            # worker configuration에서 pre defined action 확인
            task = self.context.worker.origin_worker_task
            act_def = None
            if task and 'actions' in task:
                act_def = pydash.find(task['actions'], {'func_name': self.func_name})

        else:
            # pre defined action이 없으면 임시로 자체 생성
            if act_def is None:
                api_site_config = self.context.api_site_configuration
                result = await api_site_config.get_resources()

                exclusive_area = pydash.get(result, 'ExclusiveArea')
                resource_list = []
                def cb(resource):
                    resource_list.append(
                        {'alias': resource['name'], 'value': resource['id']})

                if exclusive_area:
                    pydash.map_(exclusive_area, cb)

                act_def = {
                    'name': self.name,
                    'func_name': self.func_name,
                    'args': [
                        {
                            'type': 'string',
                            'key': 'resource',
                            'default': resource_list[0] if len(resource_list) > 0 else None,
                            'domain': resource_list,
                            'options':{'user_input': False}
                        },
                        {
                            'type': 'object',
                            'key': 'quit',
                            'default': {},
                            'domain': [],
                            'options': {'user_input': False}
                        }
                    ]
                }

        return act_def

    async def on_perform(self, args):

        args_resource = pydash.find(args, {'key': 'resource'})
        target_resource_id = pydash.get(args_resource, 'value')
        arg_properties = pydash.get(args_resource, 'properties')
        aligns = pydash.find(arg_properties, {'key': 'align'})

        exit_pose = pydash.pick(pydash.get(aligns, 'value.exit'), ['x', 'y'])

        MAX_RETRY = 100
        REQUEST_INTERVAL = 100
        worker_content = self.context.blackboard.get_worker_content()
        worker_id = worker_content['id']

        actuator = Actuator()
        await actuator.init_path_planner(self.context)
        await actuator.moving(self.context, exit_pose)

        waiter = Waiter('action_unlock : on_perform', self.context.event_loop, REQUEST_INTERVAL)
        for i in range(MAX_RETRY):
            self.rocon_logger.debug('return occupied resuorce {}/{}'.format(i+1, MAX_RETRY))
            target_resource = await self.context.api_site_configuration.get_resource(target_resource_id)
            target_slots = target_resource['resource_slots']
            occupied = pydash.find(target_slots, {'user_id': worker_id, 'status': 'occupied'})

            try:
                await self.context.api_site_configuration.return_resource(worker_id, target_resource_id, occupied['id'])
                return True
            except Exception as err:
                self.rocon_logger.error('failed to return resource with error', exception=err)

            await waiter.wait()

        self.rocon_logger.debug('exceed maximum try to return occupied resource')
        return False
