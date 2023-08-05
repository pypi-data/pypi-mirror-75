import pydash
from rocon_client_sdk_py.core_logic.action import Action
from rocon_client_sdk_py.utils.waiter import Waiter
from rocon_client_sdk_py.virtual_core.components.actuators import Actuator

class Lock(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Lock'
        self.func_name = 'lock'

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
                        }
                    ]
                }

        return act_def

    async def on_perform(self, args):

        args_resource = pydash.find(args, {'key':'resource'})
        target_resource_id = pydash.get(args_resource, 'value')
        arg_properties = pydash.get(args_resource, 'properties')
        aligns = pydash.find(arg_properties, {'key': 'align'})

        enter_pose = pydash.pick(pydash.get(aligns, 'value.enter'), ['x', 'y'])

        MAX_RETRY = 100
        REQUEST_INTERVAL = 100
        work_id = self.context.blackboard.get_worker_content()['id']

        actuator = Actuator()
        await actuator.init_path_planner(self.context)
        await actuator.moving(self.context, enter_pose)

        waiter = Waiter('action_lock : on_perform', self.context.event_loop, REQUEST_INTERVAL)
        for i in range(MAX_RETRY):
            self.rocon_logger.debug('check resource have assigned to this worker {}/{}'.format(i+1, MAX_RETRY))
            target_resource = await self.context.api_site_configuration.get_resource(target_resource_id)
            target_slots = target_resource['resource_slots']
            occupied = pydash.find(target_slots, {'user_id': work_id, 'status':'occupied'})
            if occupied:
                self.rocon_logger.debug('confirmed : resource have assigned to this worker')
                return True

            await waiter.wait()

        self.rocon_logger.debug('exceed maximum try to check resource have assigned to this worker')
        return False