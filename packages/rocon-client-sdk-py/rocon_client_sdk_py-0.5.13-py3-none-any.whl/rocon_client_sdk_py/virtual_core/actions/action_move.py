import pydash
from rocon_client_sdk_py.core_logic.action import Action
from rocon_client_sdk_py.virtual_core.components.actuators import Actuator


class Move(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Move'
        self.func_name = 'move'

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
                domain_goal_finishing = [{'alias': 'True', 'value': True}, {'alias': 'False', 'value': False}]

                api_site_config = self.context.api_site_configuration
                result = await api_site_config.get_locations()

                domain_destination = []
                def cb(location):
                    domain_destination.append({'alias':location['name'], 'value':location['id']})

                pydash.map_(result, cb)

                act_def = {
                    'name': self.name,
                    'func_name': self.func_name,
                    'args': [
                        {
                            'key': 'destination',
                            'options': {
                                'min': 0,
                                'user_input': False,
                                'max': 0
                            },
                            'default': domain_destination[0],
                            'domain': domain_destination,
                            'type': 'string'
                        },
                        {
                            'key': 'goal_finishing',
                            'type': 'boolean',
                            'default': domain_goal_finishing[0],
                            'domain': domain_goal_finishing,
                        },
                        {
                            'key': 'finishing_timeout',
                            'type': 'number',
                            'default': 30,
                            'domain': [0, 10, 20, 30, 40, 50, 60],
                            'options': {
                                'user_input': True,
                                'min': 0,
                                'max': 300
                            }
                        }
                    ]
                }

        return act_def

    async def on_perform(self, args):

        try:
            destination_id = pydash.find(args, {'key': 'destination'})['value']
            destination = await self.context.api_site_configuration.get_locations(destination_id=destination_id)
            self.context.rocon_logger.debug('move to {}({})'.format(destination['name'], destination['type']))

            self.rocon_logger.debug('get destination object from site configuration server')

            if destination is None:
                self.rocon_logger.debug('failed to get destination')

            actuator = Actuator()
            await actuator.init_path_planner(self.context)

            await actuator.moving(self.context, destination['pose'], destination_id)

            del actuator
            del destination
            del destination_id

        except Exception as err:
            self.context.rocon_logger.error('Exception occurred', exception=err)
            return False

        return True
