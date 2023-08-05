import asyncio
import pydash
import py_trees
from .task import Task, AsyncTask
from rocon_client_sdk_py.const import *
from rocon_client_sdk_py.core_logic.trees.tasks_bootstrap import init_task


class TaskIsIdleStatus(Task):
    def __init__(self, name="isIdleStatus"):
        super(TaskIsIdleStatus, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

    def update(self):
        status = self.context.blackboard.get('status')
        self.rocon_logger.debug('status : {}'.format(status), module_keyword=BT_KEYWORD)

        if status is 'idle':
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.SUCCESS), module_keyword=BT_KEYWORD)
            return py_trees.common.Status.SUCCESS
        else:
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.FAILURE), module_keyword=BT_KEYWORD)
            return py_trees.common.Status.FAILURE

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)

class TaskIsNotIdleStatus(Task):
    def __init__(self, name="isNotIdleStatus"):
        super(TaskIsNotIdleStatus, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

    def update(self):
        status = self.context.blackboard.get('status')
        self.rocon_logger.debug('status : {}'.format(status), module_keyword=BT_KEYWORD)

        if status is not 'idle':
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.SUCCESS), module_keyword=BT_KEYWORD)
            return py_trees.common.Status.SUCCESS
        else:
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.FAILURE), module_keyword=BT_KEYWORD)
            return py_trees.common.Status.FAILURE

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskHealthCheck(Task):
    def __init__(self, name="healthCheck"):
        super(TaskHealthCheck, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

    def update(self):
        #TODO add more healthCheck core_logic here
        self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.SUCCESS), module_keyword=BT_KEYWORD)

        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskCheckNoChanges(Task):
    def __init__(self, name="checkNoChanges"):
        super(TaskCheckNoChanges, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

    def update(self):
        status = self.context.blackboard.get('task_name_changed')
        self.rocon_logger.debug('task_name_changed : {}'.format(status), module_keyword=BT_KEYWORD)

        if status:
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.FAILURE), module_keyword=BT_KEYWORD)
            #TaskUpdateTaskName 에서 update 처리
            return py_trees.common.Status.FAILURE
        else:
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.SUCCESS), module_keyword=BT_KEYWORD)
            return py_trees.common.Status.SUCCESS


class TaskUpdateTaskName(AsyncTask):
    def __init__(self, name="updateTaskName"):
        super(TaskUpdateTaskName, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)
        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()

        except Exception as err:
            self.rocon_logger.error('Exception occurred', module_keyword=BT_KEYWORD, exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE

    async def _do_work(self):
        task_name = self.context.blackboard.get('task_name_changed')
        self.context.blackboard.set('task_name_changed', None)

        #변경된 task_name으로 내부 업데이트
        self.rocon_logger.debug('updating task with new task name({})'.format(task_name))

        #변경된 이름으로 task 재초기화
        api_task = self.context.api_task

        try:
            await init_task(self.context, api_task)

        except asyncio.CancelledError as cerr:
            print(cerr)
        except Exception as err:
            print(err)
        else:
            print('unexpected')

        self.async_task_status = py_trees.common.Status.SUCCESS

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status


class TaskInitReportFromExistReport(AsyncTask):
    def __init__(self, name="initReportFromExistReport"):
        super(TaskInitReportFromExistReport, self).__init__(name)

    def setup(self):
        pass


    def initialise(self):

        if self.async_task_status == py_trees.common.Status.RUNNING:
            return

        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)
        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()

        except Exception as err:
            self.rocon_logger.error('Exception occurred', module_keyword=BT_KEYWORD, exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE



    async def _do_work(self):
        #self.rocon_logger.debug('TaskInitReportFromExistReport >> _do_work')
        worker = self.context.blackboard.get('worker')
        id = worker['id']

        # status__ne has double under bar '__'
        options = {'worker': id, 'status__ne': 'finished'}

        try:
            last_report = await self.context.api_report.get_reports(options)

            if len(last_report) == 0:
                self.rocon_logger.debug('There is no processing report for this worker', module_keyword=BT_KEYWORD)

            else:
                if last_report[0]['status'] == 'pending':

                    self.context.blackboard.set('report', last_report[0])
                    self.async_task_status = py_trees.common.Status.SUCCESS
                    #self.rocon_logger.debug('TaskInitReportFromExistReport >> SUCCESS')
                    return
                else:
                    # TODO In future the worker can continuously process report after unexpected rebooting if possible
                    self.rocon_logger.debug('{} exist reports are detected. It will cancel > {}'.format(len(last_report), last_report[0]))

                    id = pydash.get(last_report[0], 'id')
                    msg = 'cannot resume processing report on this version of virtual worker now. cancel it.'
                    result = await self.context.api_report.cancel_report(id, msg, True)

                    #self.rocon_logger.debug(result, module_keyword=BT_KEYWORD)

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            #TODO 장시간 idle 상태에서 이곳으로 빠지는 경우 확인 필요 (pc 대기상태, 네트웍 상태등 확인)
            #err.with_traceback()

        self.async_task_status = py_trees.common.Status.FAILURE

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskRequestRecommendation(AsyncTask):
    def __init__(self, name="requestRecommendation"):
        super(TaskRequestRecommendation, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)
        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE
            err.with_traceback()

    async def _do_work(self):
        worker = self.context.blackboard.get('worker')
        id = worker['id']

        try:
            recommend = await self.context.api_report.req_recommend(id)

            if recommend and len(recommend) > 0:
                self.context.blackboard.set('report_recommendation', recommend)
                self.async_task_status = py_trees.common.Status.SUCCESS
                return

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

        self.async_task_status = py_trees.common.Status.FAILURE


    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskGetOwnership(AsyncTask):
    def __init__(self, name="getOwnership"):
        super(TaskGetOwnership, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        if self.async_task_status == py_trees.common.Status.RUNNING:
            return

        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

    async def _do_work(self):

        worker_content = self.context.blackboard.get_worker_content()
        worker_id = worker_content['id']

        recommend = self.context.blackboard.get('report_recommendation')
        if recommend is None:
            self.rocon_logger.debug('failed to take ownership of report: empty recommendation')
            self.async_task_status = py_trees.common.Status.FAILURE
            return

        try:
            '''
            if self.context.raise_test_exception:
                self.context.raise_test_exception = False
                raise Exception('test error raised')
            '''

            id = pydash.get(recommend, '0.id')
            target_report = await self.context.api_report.req_ownership(id, worker_id)
            self.rocon_logger.debug('target_report : {}'.format(target_report))
            self.context.blackboard.set('recommend', None)

            if target_report != None and 'worker' in target_report and target_report['worker'] == worker_id:
                self.context.blackboard.set('report', target_report)
                self.async_task_status = py_trees.common.Status.SUCCESS
                return
            else:
                msg = 'Failed to take ownership of report : {}'.format(target_report)
                self.rocon_logger.error(msg)

                msg = 'report is not valid. so it will be cancel.'
                result = await self.context.api_report.cancel_report(id, msg, True)


                # TODO  need to recovery routine here
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)

        self.async_task_status = py_trees.common.Status.FAILURE

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskHandleFirstRevision(AsyncTask):
    def __init__(self, name="handleFirstRevision"):
        super(TaskHandleFirstRevision, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        if self.async_task_status == py_trees.common.Status.RUNNING:
            return

        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE
            err.with_traceback()

    async def _do_work(self):

        report = self.context.blackboard.get_report()
        if report is None:
            self.async_task_status = py_trees.common.Status.FAILURE
            return

        if pydash.get(report, 'revision') is None:
            self.async_task_status = py_trees.common.Status.SUCCESS
            return

        try:
            accepted_revision = await self.context.api_report.approve_revision(report)

            if pydash.get(accepted_revision, 'revision.status') == 'approved':
                self.context.blackboard.set('report', accepted_revision)
                self.async_task_status = py_trees.common.Status.SUCCESS
                return

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

        self.async_task_status = py_trees.common.Status.FAILURE

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskStartReport(AsyncTask):
    def __init__(self, name="startReport"):
        super(TaskStartReport, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        if self.async_task_status == py_trees.common.Status.RUNNING:
            return

        self.async_task_status = py_trees.common.Status.RUNNING

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE
            err.with_traceback()

    async def _do_work(self):
        worker_content = self.context.blackboard.get_worker_content()
        worker_id = worker_content['id']
        report = self.context.blackboard.get_report()

        self.async_task_status = py_trees.common.Status.FAILURE

        if report is None:
            return

        try:
            update_body={'status': 'running', 'worker': worker_id}
            updated_report = await  self.context.api_report.update_report(report['id'], update_body)

            if updated_report is not None and updated_report['status'] == 'running':
                self.context.blackboard.set_status('busy')
                self.async_task_status = py_trees.common.Status.SUCCESS

            del updated_report

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)
