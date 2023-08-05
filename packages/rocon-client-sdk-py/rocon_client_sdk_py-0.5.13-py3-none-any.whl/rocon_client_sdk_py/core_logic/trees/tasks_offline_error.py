import py_trees
import asyncio
from overrides import overrides
from .task import Task, AsyncTask
from rocon_client_sdk_py.const import *
from rocon_client_sdk_py.utils.util import *

class TaskIsOfflineStatus(AsyncTask):
    def __init__(self, name="isOfflineStatus"):
        super(TaskIsOfflineStatus, self).__init__(name)

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
            err.with_traceback()

    async def _do_work(self):
        status = self.context.blackboard.get('status')

        #self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        #self.rocon_logger.debug(' worker >> on_check_offline_status       ', show_caller_info=False)
        #self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        rtn = await self.context.worker.on_check_offline_status(status)
        if rtn is False:
            self.rocon_logger.error('something wrong in custom check_offline_status')
            self.async_task_status = py_trees.common.Status.FAILURE

        else:
            self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status


    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskIsErrorStatus(AsyncTask):
    def __init__(self, name="isErrorStatus"):
        super(TaskIsErrorStatus, self).__init__(name)

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
            err.with_traceback()

    async def _do_work(self):
        status = self.context.blackboard.get('status')

        #self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        #self.rocon_logger.debug(' worker >> on_check_error_status         ', show_caller_info=False)
        #self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        rtn = await self.context.worker.on_check_error_status(status)

        if status is 'error':
            self.rocon_logger.debug('now error status', module_keyword=BT_KEYWORD)

        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)