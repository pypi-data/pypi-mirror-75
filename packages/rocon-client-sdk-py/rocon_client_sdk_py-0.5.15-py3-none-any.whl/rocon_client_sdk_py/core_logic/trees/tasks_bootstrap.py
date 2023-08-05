import py_trees
import asyncio
from overrides import overrides
from .task import Task, AsyncTask
from rocon_client_sdk_py.core_logic.hook_origin_init_worker import HookOriginInitWorker
from rocon_client_sdk_py.const import *


class TaskIsBooted(Task):

    @overrides
    def __init__(self, name="isBooted"):
        super(TaskIsBooted, self).__init__(name)

    @overrides
    def setup(self):
        pass

    @overrides
    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

    @overrides
    def update(self):
        is_booted = self.context.is_booted

        if is_booted == True:
            self.rocon_logger.debug("update >> Status.SUCCESS", module_keyword=BT_KEYWORD)
            return py_trees.common.Status.SUCCESS
        else:
            self.rocon_logger.debug("update >> Status.FAILURE", module_keyword=BT_KEYWORD)
            return py_trees.common.Status.FAILURE

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskInitWorker(AsyncTask):

    @overrides
    def __init__(self, name="initWorker"):
        super(TaskInitWorker, self).__init__(name)

    @overrides
    def setup(self):
        pass

    @overrides
    def initialise(self):
        super().initialise()
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)
        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

    async def _do_work(self):

        worker_content = self.context.blackboard.get_worker_content()
        if worker_content:
            self.async_task_status = py_trees.common.Status.SUCCESS
            return

        uuid = self.context.worker.uuid
        api_worker = self.context.api_worker

        worker_record = await api_worker.find_one_by_uuid(uuid)

        if worker_record is None or len(worker_record) is 0:
            self.rocon_logger.debug('failed to find worker by uuid' + uuid)
            self.rocon_logger.debug('worker registered very first time. generate worker');
        else:
            self.rocon_logger.debug('registered worker')

        worker_context = None
        name = HookOriginInitWorker.name()
        obj_hook = self.context.hook_manager.find_hook(name)
        if obj_hook:
            self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
            self.rocon_logger.debug(' worker >> on_hook                       ', show_caller_info=False)
            self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
            self.rocon_logger.debug(' hook name : {}, body : {}'.format(obj_hook.name, worker_record))

            worker_context = await self.context.worker.on_hook(obj_hook, worker_record)

        result = worker_context or worker_record
        result = await api_worker.upsert(result)

        self.context.blackboard.set('worker', result)
        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskInitTask(AsyncTask):

    @overrides
    def __init__(self, name="initTask"):
        super(TaskInitTask, self).__init__(name)

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

        api_task = self.context.api_task

        if self.context.blackboard.get('task'):
            self.async_task_status = py_trees.common.Status.SUCCESS
            return

        err_str = await init_task(self.context, api_task)
        if err_str:
            self.rocon_logger.debug(err_str)

        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)

#공용 루틴으로 만듦
async def init_task(context, api_task):
    task_configs = context.blackboard.get('configs')
    taskName = task_configs['taskName']

    options = {
        'name': None if task_configs == None else taskName,
        'description': None if task_configs == None else task_configs['taskDescription']
    }

    #on_load_task
    await context.worker.on_load_task(taskName)

    task_body = await context.action_manager.build_task(options=options)

    worker_content = context.blackboard.get_worker_content()
    if worker_content and 'id' in worker_content:
        # TODO if(data.worker && data.worker.id) 조건 필요 확인
        id = worker_content['id']

        task = await api_task.init_task(id, task_body)

        '''
        2020.05.14
        task는 서버로 부터 받은 updated된 task, 내부 기록은 task_body만 기록하고, heart_beat update task시에 task_body를 업로드한다.
        '''
        context.blackboard.set('task', task_body)
        context.blackboard.set('task_name_changed', None)

        t = context.blackboard.get('task')

        if task is None or len(task) is 0:
            return 'not registered worker'
        else:
            return 'registered worker'

    else:
        return 'initialize worker first. before register task'

    return None

class TaskBootCheck(AsyncTask):

    @overrides
    def __init__(self, name="bootCheck"):
        super(TaskBootCheck, self).__init__(name)

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

        worker = self.context.blackboard.get('worker')
        task = self.context.blackboard.get('task')
        if worker and task:

            try:
                result = await self.context.blackboard.sync_worker()
                self.rocon_logger.debug('boot check finished, set worker status to idle')
                self.async_task_status = py_trees.common.Status.SUCCESS

                return

            except Exception as err:
                self.rocon_logger.error('Exception occurred', exception=err)
                err.with_traceback()
        else:
            self.rocon_logger.debug('worker or task is not initialized')

        self.async_task_status = py_trees.common.Status.FAILURE

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)

        if self.async_task_status == py_trees.common.Status.SUCCESS:
            self.context.is_booted = True
            self.context.blackboard.set_status('idle')
            self.context.blackboard.set('NowProcessInstructionStatus', None)
            self.context.blackboard.set_worker_content({'status': 'idle'})

            self.rocon_logger.debug('\n', show_caller_info=False)
            self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
            self.rocon_logger.debug('       Rocon Client boot completed       ', show_caller_info=False)
            self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
            self.rocon_logger.debug("Press 'h' key to get CLI Help.", show_caller_info=False)

        return self.async_task_status

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)

