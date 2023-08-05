import py_trees
import asyncio
from overrides import overrides
from .task import Task, AsyncTask
from rocon_client_sdk_py.const import *


class TaskHandleControlMessage(AsyncTask):
    def __init__(self, name="handleControlMessage"):
        super(TaskHandleControlMessage, self).__init__(name)

    @overrides
    def setup(self):
        pass

    @overrides
    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE

    async def _do_work(self):
        '''
        메시지 처리의 기본 원칙은 BehaviorTree상에서 현재의 node에서 message_manager를 통해 message queue에 있는 
        메시지를 하나씩 읽어 처리한다. 
        메시지큐에 쌓이는 메시지는 외부(VirtualWorker_UI에서 보내는 메시지 내부에서 생성한 메시지, 임의의 출처에서 받는 메시지 등이 
        쌓이게 된다.
        TaskHandleControlMessage 처리시 마다 message queue에서 우선순위에 따른 처리 메시지 하나를 읽어서 처리한다.
        '''
        self.async_task_status = py_trees.common.Status.SUCCESS
        message_manager = self.context.message_manager

        msg_data = self.context.message_manager.pop_message_data()
        if msg_data:
            message_inst = message_manager.find_message(msg_data['name'])
            if message_inst is None:
                self.rocon_logger.error('malformed message handler: {}, {}'.format(msg_data['key'], {'message': msg_data}))
                self.async_task_status = py_trees.common.Status.FAILURE
                return

            try:
                message_body = msg_data['body']
                self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                self.rocon_logger.debug(' worker >> on_message                    ', show_caller_info=False)
                self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                self.rocon_logger.debug(' message name : {}, body : {}'.format(message_inst.name, message_body))

                await self.context.worker.on_message(message_inst, message_body)


            except Exception as err:
                self.rocon_logger.error('error occurred while processing message : {}'.format({
                    'message': msg_data
                }), exception=err)
                self.async_task_status = py_trees.common.Status.FAILURE
                return

        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)

