import pydash
from rx.subject import Subject
from rocon_client_sdk_py.core_logic.action import Action
from rocon_client_sdk_py.utils.waiter import Waiter
from rocon_client_sdk_py.virtual_core.components.button_requests import ButtonRequests


class Wait(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Wait'
        self.func_name = 'wait'

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

                domain_door_behavior = [{'alias': 'True', 'value': True}, {'alias': 'False', 'value': False}];

                act_def = {
                    'name': self.name,
                    'func_name': self.func_name,
                    'args':[
                        {
                            'key': 'type',
                            'type': 'string',
                            'default': 'human_input',
                            'domain': [
                                {'alias': 'Duration', 'value': 'duration'},
                                {'alias': 'Controlled by system', 'value': 'signal'},
                                {'alias': 'Until button press', 'value': 'human_input'}
                            ],
                            'options':{
                                'user_input': False,
                                'regex': None
                            }
                        },
                        {
                            'key': 'timeout',
                            'type': 'number',
                            'default': 30000,
                            'domain': [
                                {'alias': 'forever', 'value': -1},
                                {'alias': '10000 ms', 'value': 10000},
                                {'alias': '20000 ms', 'value': 20000},
                                {'alias': '30000 ms', 'value': 30000},
                                {'alias': '40000 ms', 'value': 40000},
                                {'alias': '50000 ms', 'value': 50000},
                                {'alias': '60000 ms', 'value': 60000}
                            ],
                            'options':{
                                'user_input': True,
                                'regex': None
                            }
                        },
                        {
                            'key': 'param',
                            'type': 'string',
                            'default': 'revision',
                            'domain': ['revision', 'success', 'fail']
                        },
                        {
                            'key': 'door_behavior',
                            'type': 'boolean',
                            'default': domain_door_behavior[1],
                            'domain': domain_door_behavior
                        }
                    ]
                }

        return act_def

    def cb_next(self, data):
        self.rocon_logger.debug('finish wait with signal')
        self.result = True
        self._wait_exit = True
        self.waiter.end('success')
        self.waiter_inf.end('success')
        return True

    def cb_completed(self):
        self.rocon_logger.debug('received cb_completed')

    async def type_signal(self, args):
        timeout = pydash.find(args, {'key':'timeout'})['value_alias']['value']
        brs = ButtonRequests(self.context)
        self.waiter = Waiter('action_wait : type_signal', self.context.event_loop, timeout)
        self.waiter_inf = Waiter('action_wait : type_signal_inf', self.context.event_loop, -1)
        self.result = False
        SIGNAL = 'signal'
        self._wait_exit = False

        subj = Subject()
        button_req = {
            'button_id': SIGNAL,
            'uuid': self.context.worker.uuid,
            'button': 'O',
            'notify': subj
        }

        subj.subscribe(on_next=self.cb_next, on_completed=self.cb_completed)
        brs.set_button_request(button_req)

        # set timeout
        if timeout > 0:
            timeout_result = await self.waiter.wait()
            if timeout_result == 'timeout':
                self.rocon_logger.debug('finish wait, exceed timeout')
                brs.remove_button_request(SIGNAL, self.context.worker.uuid)
                raise Exception('timeout exceed')
            elif timeout_result is not None:
                self.rocon_logger.debug('timeout waiter has been terminated with message : {}'.format(timeout_result))
                brs.remove_button_request(SIGNAL, self.context.worker.uuid)
            else:
                #None case
                pass

        else:
            # in case of infinite waiting
            inf_wait_result = await self.waiter_inf.wait()
            if inf_wait_result != 'success':
                self.rocon_logger.debug('timeout waiter has been terminated with message: {}'.format(inf_wait_result))

        self.rocon_logger.debug('done type_signal of action_wait')
        return self.result

    async def type_human_input(self, args):
        timeout = pydash.find(args, {'key': 'timeout'})['value']
        brs = ButtonRequests(self.context)
        self.waiter = Waiter('action_wait : type_human_input', self.context.event_loop, timeout)
        self.waiter_inf = Waiter('action_wait : type_human_input_inf', self.context.event_loop, -1)
        self.result = False
        SIGNAL = 'human_input'
        self._wait_exit = False

        subj = Subject()
        button_req = {
            'button_id': SIGNAL,
            'uuid': self.context.worker.uuid,
            'button': 'O',
            'notify': subj
        }

        subj.subscribe(on_next=self.cb_next, on_completed=self.cb_completed)
        brs.set_button_request(button_req)

        # set timeout
        if timeout > 0:
            timeout_result = await self.waiter.wait()
            if timeout_result == 'timeout':
                self.rocon_logger.debug('finish wait, exceed timeout')
                brs.remove_button_request(SIGNAL, self.context.worker.uuid)

            elif timeout_result is not None:
                self.rocon_logger.debug('timeout waiter has been terminated with message: {}'.format(timeout_result))
                brs.remove_button_request(SIGNAL, self.context.worker.uuid)
            else:
                # None case
                pass

        else:
            # in case of infinite waiting
            inf_wait_result = await self.waiter_inf.wait()
            if inf_wait_result != 'success':
                self.rocon_logger.debug('timeout waiter has been terminated with message: {}'.format(inf_wait_result))

        self.rocon_logger.debug('done type_signal of action_wait')
        return self.result

    async def on_perform(self, args):
        type = pydash.find(args, {'key': 'type'})['value']
        timeout = pydash.find(args, {'key': 'timeout'})['value']

        if type == 'duration':
            self.rocon_logger.debug('start to waiting... for {}sec'.format(timeout/1000))
            waiter = Waiter('action_wait : duration', self.context.event_loop, timeout)
            await waiter.wait()
            return True
        elif type == 'signal':
            rtn = await self.type_signal(args)
            return rtn
        elif type == 'human_input':
            rtn = await self.type_human_input(args)
            return rtn
        else:
            self.rocon_logger.debug('unknown wait type')
            return False
