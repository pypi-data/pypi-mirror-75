from rocon_client_sdk_py.core_logic.action import Action


class Notify(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Notify'
        self.func_name = 'notify'

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
                act_def = {
                    'name': self.name,
                    'func_name': self.func_name,
                    'args':[
                        {
                            'key': 'default_sender',
                            'name': 'Default Sender',
                            'domain': [],
                            'type': 'string',
                            'default': None,
                            'options': {
                                'user_input': True
                            }
                        },
                        {
                            'key': 'default_message',
                            'name': 'Default Message',
                            'domain': [],
                            'type': 'string',
                            'default': None,
                            'options': {
                                'user_input': True
                            }
                        },
                        {
                            'key': 'default_method',
                            'name': 'Default Method',
                            'type': 'object',
                            'properties': [
                                {
                                    'key': 'email',
                                    'name': 'E-mail',
                                    'type': 'boolean',
                                    'default': True
                                },
                                {
                                    'key': 'sms',
                                    'name': 'SMS',
                                    'type': 'boolean',
                                    'default': False
                                },
                                {
                                    'key': 'web_push',
                                    'name': 'Web_push',
                                    'type': 'boolean',
                                    'default': False
                                }
                            ]
                        },
                        {
                            'key': 'receivers',
                            'name': 'Receiver',
                            'domain': [],
                            'type': 'object',
                            'properties': [
                                {
                                    'key': 'custom_sender',
                                    'name': 'Custom Sender',
                                    'domain': [],
                                    'type': 'string',
                                    'default': None,
                                    'options': {
                                        'user_input': True
                                    }
                                },
                                {
                                    'key': 'custom_message',
                                    'name': 'Custom Message',
                                    'domain': [],
                                    'type': 'string',
                                    'default': None,
                                    'options': {
                                        'user_input': True
                                    }
                                },
                                {
                                    'key': 'custom_method',
                                    'name': 'Custom Method',
                                    'type': 'object',
                                    'properties': [
                                        {
                                            'key': 'email',
                                            'name': 'E-mail',
                                            'type': 'boolean',
                                            'default': True
                                        },
                                        {
                                            'key': 'sms',
                                            'name': 'SMS',
                                            'type': 'boolean',
                                            'default': False
                                        },
                                        {
                                            'key': 'web_push',
                                            'name': 'Web_push',
                                            'type': 'boolean',
                                            'default': False
                                        }
                                    ]
                                },
                                {
                                    'key': 'receiver_id',
                                    'name': 'Receiver ID',
                                    'domain': [],
                                    'type': 'string',
                                    'default': None,
                                    'options': {
                                        'user_input': True
                                    }
                                },
                                {
                                    'key': 'receiver_type',
                                    'name': 'Receiver Type',
                                    'domain': [],
                                    'type': 'string',
                                    'default': None,
                                    'options': {
                                        'user_input': True
                                    }
                                }
                            ]
                        }
                    ]
                }

        return act_def

    async def on_perform(self, args):
        self.rocon_logger.debug('it is not implemented yet...')
        return True
