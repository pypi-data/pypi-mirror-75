import py_trees
import asyncio
import pydash
from overrides import overrides
from .task import AsyncTask
from rocon_client_sdk_py.utils.util import *
from rocon_client_sdk_py.const import *


class TaskUpdateWorker(AsyncTask):
    def __init__(self, name="updateWorker"):
        super(TaskUpdateWorker, self).__init__(name)

        self.t_last = None

    def __del__(self):
        pass

    @overrides
    def setup(self):
        pass

    @overrides
    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        if self.async_task_status == py_trees.common.Status.RUNNING:
            print('here')

        status = self.context.blackboard.get('status')
        if status == 'busy':
            self.async_task_status = py_trees.common.Status.SUCCESS
            return

        worker_content = self.context.blackboard.get_worker_content()
        last_updated_at = pydash.get(worker_content, 'updated_at')
        last_updated_ms = 0

        if last_updated_at:
            last_updated_ms = get_time_milliseconds(last_updated_at)
        else:
            # TODO 'updated_at' 기록되지 않은 경우, 다른 이슈 없는지 재확인 필요
            pass

        if last_updated_ms is not 0 and self.check_valid_interval(DEFAULT_UPDATE_WORKER_INTERVAL_MS, last_updated_ms) is True:
            # interval 조건을 만족할때,
            self.async_task_status = py_trees.common.Status.RUNNING

            try:
                coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
                result = coro_future.result()

            except Exception as err:
                self.rocon_logger.error('Exception occurred', exception=err)
                self.async_task_status = py_trees.common.Status.FAILURE
                err.with_traceback()

        else:
            # interval 이하의 경우 SUCCESS 처리한다.
            self.async_task_status = py_trees.common.Status.SUCCESS

    async def _do_work(self):
        '''
        blackboard에 기록된 worker_content를 주기적으로 concert server에 업데이트하는 역할
        sdk user에게 노출 불필요하며, sdk 유저는 worker_content의 포맷에 맞는 데이터를 기록할 의무를 가짐
        :return:
        '''

        if self.context.blackboard.get_worker_content_update() is None:
            self.context.blackboard.set_worker_content({'updated_at': current_datetime_utc_iso_format()})

        try:
            # TODO sync_worker를 주기적으로 하는데, 다른 루틴에서도 필요에 따라 호출하고 있다. 큐로 관리해 최신 데이터 기준으로 업데이트 구조 변경 필요
            result = await self.context.blackboard.sync_worker()

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE
            err.with_traceback()
            return

        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status


    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskUpdateTask(AsyncTask):
    def __init__(self, name="updateTask"):
        super(TaskUpdateTask, self).__init__(name)

    @overrides
    def setup(self):
        pass

    @overrides
    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        if self.async_task_status == py_trees.common.Status.RUNNING:
            return


        if self.context.blackboard.get('status') is 'busy':
            self.async_task_status = py_trees.common.Status.SUCCESS
            return


        last_updated_ms = self.context.blackboard.get('task_updated') or 0

        if self.check_valid_interval(DEFAULT_UPDATE_TASK_INTERVAL_MS, last_updated_ms) is True:
            # interval 조건을 만족할때,
            self.async_task_status = py_trees.common.Status.RUNNING
            try:
                coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
                result = coro_future.result()

            except Exception as err:
                self.rocon_logger.error('Exception occurred', exception=err)
                err.with_traceback()

        else:
            # interval 이하의 경우 SUCCESS 처리한다.
            self.async_task_status = py_trees.common.Status.SUCCESS

    async def _do_work(self):
        '''
        정해진 시간 간격으로 concert server로 부터 task 정보를 받아서 blackboard에 기록한다.
        sdk user에게 노출 불필요함.
        :return:
        '''
        task_body = self.context.blackboard.get('task')
        worker = self.context.blackboard.get('worker')
        id = worker['id']

        try:
            task_body['worker'] = id
            result = await self.context.api_task.upsert(task_body)
            '''
            2020.05.14 
            task 업데이트 정책은 robot내의 생성 task 데이터만 업로드한다. 
            기존 upsert 후 서버로 부터 받은 result에는 개별 robot 외의 부가 데이터가 포함되어 있어 주기적 업데이트시 부가 데이터의 재업로드 방지 위함.
            
            self.context.blackboard.set('task', result)
            
            로봇의 task 변경이 발생할 때 task_body를 업데이트해야한다.
            '''

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE
            err.with_traceback()
            return

        curnt_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
        self.context.blackboard.set('task_updated', curnt_time_ms)
        self.async_task_status = py_trees.common.Status.SUCCESS

    @overrides
    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    @overrides
    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)

