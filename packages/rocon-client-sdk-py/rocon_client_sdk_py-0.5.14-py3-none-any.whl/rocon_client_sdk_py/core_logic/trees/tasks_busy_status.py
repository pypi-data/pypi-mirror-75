import py_trees
import asyncio
import pydash
from .task import Task, AsyncTask
from rocon_client_sdk_py.utils.util import *
from rocon_client_sdk_py.core_logic.hook_origin_check_revision import HookOriginCheckRevision
from rocon_client_sdk_py.core_logic.hook_origin_validate_report import HookOriginValidateReport
from rocon_client_sdk_py.const import *

# for temporary development
USE_DEBUG_TEST_1HOUR_INSTRUCTIONS_LOOP = False


class TaskIsBusyStatus(Task):
    def __init__(self, name="isBusyStatus"):
        super(TaskIsBusyStatus, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

    def update(self):
        # TaskIsBusyStatus

        if self.context.blackboard.get('status') == 'busy':
            self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.SUCCESS), module_keyword=BT_KEYWORD)
            return py_trees.common.Status.SUCCESS

        self.rocon_logger.debug('update >> {}'.format(py_trees.common.Status.FAILURE), module_keyword=BT_KEYWORD)
        return py_trees.common.Status.FAILURE

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskValidateReport(AsyncTask):
    def __init__(self, name="validateReport"):
        super(TaskValidateReport, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        last_updated_ms = self.context.blackboard.get('validate_updated') or 0

        if self.check_valid_interval(DEFAULT_VALIDATE_REPORT_INTERVAL_MS, last_updated_ms) is True:
            # interval 조건을 만족할때,

            self.async_task_status = py_trees.common.Status.RUNNING

            try:
                coro_future = asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
                result = coro_future.result()
            except Exception as err:
                self.rocon_logger.error('Exception occurred', exception=err)
                self.async_task_status = py_trees.common.Status.FAILURE
                #err.with_traceback()

        else:
            self.async_task_status = py_trees.common.Status.SUCCESS

    async def _do_work(self):
        # TaskValidateReport
        report = self.context.blackboard.get_report()
        report_id = pydash.get(report, 'id')
        if report == None or report_id == None:
            self.context.action_manager.validate_status = None
            self.async_task_status = py_trees.common.Status.SUCCESS
            return




        try:
            updated_report = await self.context.api_report.get_report_by_id(report['id'])

            validate_status = pydash.get(updated_report, 'status')
            if pydash.has(updated_report, 'instructions') is False or len(updated_report['instructions']) == 0:
                validate_status = 'empty'

            self.context.action_manager.validate_status = validate_status

            name = HookOriginValidateReport.name()
            obj_hook = self.context.hook_manager.find_hook(name)
            if obj_hook and validate_status != 'running':
                self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                self.rocon_logger.debug(' worker >> on_hook                       ', show_caller_info=False)
                self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                self.rocon_logger.debug(' hook name : {}, body : {}'.format(obj_hook.name, validate_status))

                if validate_status == 'finished':
                    self.rocon_logger.debug('report finished from outside')

                result = await self.context.worker.on_hook(obj_hook, validate_status)

            if validate_status == 'finished':
                '''
                validate report에서는 주로 FMS에서 job을 취소했을 때 worker에서 확인할 수 있는 포인트이다.
                수행중인 job을 stop하고 idle 상태로 이동한다.
                '''
                #self.rocon_logger.debug('report finished from outside')

                '''
                self.context.blackboard.clear_report()
                self.context.blackboard.set_status('idle')
                self.async_task_status = py_trees.common.Status.FAILURE
                self.context.blackboard.set('NowProcessInstructionStatus', None)

                '''
                #curnt_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
                #self.context.blackboard.set('validate_updated', curnt_time_ms)

                #await self.context.blackboard.sync_report()

                self.async_task_status = py_trees.common.Status.SUCCESS
                return

            if validate_status is 'empty':
                '''
                비정상적으로 report의 정보가 존재하지 않을 경우 정리하고 idle 상태로 이동한다.
                '''
                self.rocon_logger.debug('This report is not contains any instruction, mark this abort')

                await self.context.api_report.abort_report(report['id'], 'It has not any instruction')

                self.context.blackboard.clear_report()
                self.context.blackboard.set_status('idle')
                self.async_task_status = py_trees.common.Status.FAILURE
                self.context.blackboard.set('NowProcessInstructionStatus', None)

                curnt_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
                self.context.blackboard.set('validate_updated', curnt_time_ms)
                return

            self.async_task_status = py_trees.common.Status.SUCCESS

            del updated_report

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()
            self.async_task_status = py_trees.common.Status.FAILURE

        del report
        curnt_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
        self.context.blackboard.set('validate_updated', curnt_time_ms)

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskCheckRevision(AsyncTask):
    def __init__(self, name="checkRevision"):
        super(TaskCheckRevision, self).__init__(name)

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise checkRevision", module_keyword=BT_KEYWORD)

        last_updated_ms = self.context.blackboard.get('check_revision_updated') or 0

        if self.check_valid_interval(DEFAULT_CHECK_REVISION_INTERVAL_MS, last_updated_ms) is True:
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
            self.async_task_status = py_trees.common.Status.SUCCESS

    async def _do_work(self):
        # TaskCheckRevision
        report = self.context.blackboard.get_report()
        report_id = pydash.get(report, 'id')
        revision = None
        updated_report = None

        try:

            if report and report_id:
                updated_report = await self.context.api_report.get_report_by_id(report_id)
                revision = pydash.get(updated_report, 'revision.status')

            '''
            if self.context.raise_test_exception:
                self.context.raise_test_exception = False
                raise Exception('test error raised')
            '''

            if revision == 'pending':
                self.rocon_logger.debug('unhandled revision detected (pending revision)')

                name = HookOriginCheckRevision.name()
                obj_hook = self.context.hook_manager.find_hook(name)
                if obj_hook:
                    self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                    self.rocon_logger.debug(' worker >> on_hook                       ', show_caller_info=False)
                    self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                    #self.rocon_logger.debug(' hook name : {}, body : {}'.format(obj_hook.name, updated_report))
                    self.rocon_logger.debug(' hook name : {}'.format(obj_hook.name))

                    result = await self.context.worker.on_hook(obj_hook, updated_report)

            del updated_report
            self.async_task_status = py_trees.common.Status.SUCCESS

        except Exception as err:
            self.async_task_status = py_trees.common.Status.FAILURE
            self.rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

        del report
        curnt_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
        self.context.blackboard.set('check_revision_updated', curnt_time_ms)


    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskProcessInstruction(AsyncTask):
    def __init__(self, name="processInstruction"):
        super(TaskProcessInstruction, self).__init__(name)
        self._now_working = False

        self.test_raise_err = True

    def setup(self):
        pass

    def initialise(self):
        self.rocon_logger.debug("initialise >>", module_keyword=BT_KEYWORD)

        now_working = self.context.blackboard.get('NowProcessInstructionStatus')

        test_pass = False
        if test_pass:
            # For test : instruction 수행없이 cycle 테스트
            self.context.blackboard.set_status('idle')
            self.context.blackboard.set('NowProcessInstructionStatus', None)
            self.async_task_status = py_trees.common.Status.SUCCESS
            return



        if now_working is None:
            self.async_task_status = py_trees.common.Status.RUNNING
            self.context.blackboard.set('NowProcessInstructionStatus', py_trees.common.Status.RUNNING)

        elif now_working == py_trees.common.Status.RUNNING:
            self.async_task_status = py_trees.common.Status.RUNNING
            return
        elif now_working == py_trees.common.Status.SUCCESS:
            self.async_task_status = py_trees.common.Status.SUCCESS
            return
        elif now_working == py_trees.common.Status.FAILURE:
            self.context.blackboard.set('NowProcessInstructionStatus', None)
            self.async_task_status = py_trees.common.Status.FAILURE
            return

        def done_callback(coro):
            print('done run_coroutine_threadsafe')
            coro.done()


        try:
            asyncio.run_coroutine_threadsafe(self._do_work(), self.context.event_loop)
            #coro_future.add_done_callback(done_callback)
            #result = coro_future.result()

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.async_task_status = py_trees.common.Status.FAILURE
            err.with_traceback()
        #finally:
        #    coro_future.done() or coro_future.cancel()


    async def _do_work(self):
        # TaskProcessInstruction

        is_success = True
        self.context.action_manager.validate_status = None

        # For test : instruction 수행없이 cycle 테스트
        test_pass = False
        if test_pass:
            self.async_task_status = py_trees.common.Status.SUCCESS
            self.context.blackboard.set('NowProcessInstructionStatus', py_trees.common.Status.SUCCESS)

            result = {
                'current': None,
                'status': 'success',
                'status_msg': 'finished successfully'
            }
            self.context.blackboard.update_report_result(result)
            return

        report = self.context.blackboard.get_report()
        instructions = pydash.get(report, 'instructions', [])
        self.context.blackboard.update_report_result({'status': 'running', 'status_msg': 'just started'})

        size = len(instructions)
        act_names = pydash.map_(instructions, 'action.func_name')
        self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        self.rocon_logger.debug(' worker >> on_pre_process_instructions   ', show_caller_info=False)
        self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        self.rocon_logger.debug(' received {} actions : {}'.format(size, act_names), show_caller_info=False)
        await self.context.worker.on_pre_process_instructions(instructions)

        self.rocon_logger.debug('There are {} instructions : {}'.format(len(instructions), act_names))

        run_instructions = True
        if run_instructions:
            # TODO 적어도 while 혹은 queue 로 구조 변경 필요? (exception 처리 등)
            for i, inst in enumerate(instructions):
                if self.context.action_manager.is_not_valid_status() == True:

                    #현재 수행을 취소하고 Faiure처리한다.
                    self.async_task_status = py_trees.common.Status.FAILURE
                    return

                self.context.blackboard.update_report_result({'current': inst['id']})

                act = pydash.get(inst, 'action')
                act_func_name = pydash.get(act, 'func_name')
                args = pydash.get(act, 'args')

                self.rocon_logger.debug('now processing the action[{}] : {}'.format(i, act_func_name))

                if act_func_name is None:
                    self.rocon_logger.error('unknown action')
                    self.context.blackboard.set_status('error')
                    self.async_task_status = py_trees.common.Status.FAILURE
                    self._now_working = False
                    return

                inst_result = {
                    'id': pydash.get(inst, 'id'),
                    'status': 'running',
                    'started_at': current_datetime_utc_iso_format(),
                    'finished_at': None,
                    'retries': 0
                }

                self.context.blackboard.update_instruction_result(inst_result)
                #TODO move syncReport somewhere else or make queue for it
                try:
                    await self.context.blackboard.sync_report()
                except Exception as e:
                    pass

                try:
                    obj_act = self.context.action_manager.find_action(act_func_name)
                    if obj_act:

                        self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                        self.rocon_logger.debug(' worker >> on_process_instruction        ', show_caller_info=False)
                        self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                        self.rocon_logger.debug(' perform action : {}'.format(obj_act.name), show_caller_info=False)

                        run_instruction = True
                        if run_instruction:

                            rtn  = await self.context.worker.on_process_instruction(obj_act, args)
                            inst_result['returns'] = rtn
                            if rtn is False:
                                raise RuntimeError('on_process_instruction returned False, so current instruction will be cancelled')

                        del obj_act

                        '''
                        if self.context.raise_test_exception:
                            self.context.raise_test_exception = False
                            raise Exception('test error raised')
                        '''

                        if self.context.action_manager.is_not_valid_status() == True:
                            # 현재 수행을 취소하고 Failure처리한다.

                            #self.rocon_logger.debug('instructions do not valid, so canceled all')
                            #raise RuntimeError('instructions do not valid, so canceled all')

                            self.context.blackboard.clear_report()
                            self._now_working = False
                            self.context.blackboard.set('NowProcessInstructionStatus', py_trees.common.Status.SUCCESS)

                            self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                            self.rocon_logger.debug(' worker >> on_post_process_instructions  ', show_caller_info=False)
                            self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                            await self.context.worker.on_post_process_instructions(instructions, is_success=False)

                            self.async_task_status = py_trees.common.Status.SUCCESS
                            print('he')


                        inst_result['status'] = 'DONE_SUCCESS'
                        inst_result['finished_at'] = current_datetime_utc_iso_format()
                        self.rocon_logger.debug('success to process instruction with result')
                        self.context.blackboard.update_instruction_result(inst_result)

                        try:
                            await self.context.blackboard.sync_report()
                        except Exception as e:
                            report = self.get_report()
                            self.rocon_logger.error('sync_report failed : {}'.format(report))

                    else:
                        self.rocon_logger.debug('Not found action : {}'.format(act_func_name))

                    del inst

                except Exception as err:
                    self.rocon_logger.error('Exception occurred : {}'.format(err), exception=err)
                    inst_result['returns'] = None
                    inst_result['status'] = 'failed'
                    inst_result['finished_at'] = current_datetime_utc_iso_format()

                    self.context.blackboard.update_instruction_result(inst_result)
                    await self.context.blackboard.sync_report()

                    report = self.context.blackboard.get_report()
                    msg = 'failed to process instruction: {}'.format(inst['id'])
                    if report:
                        await self.context.api_report.cancel_report(report['id'], msg, True)

                    self.context.blackboard.clear_report()
                    self.context.blackboard.set_status('idle')
                    self.context.blackboard.set('NowProcessInstructionStatus', None)
                    self.rocon_logger.error('error occurred while processing instruction')
                    self.async_task_status = py_trees.common.Status.FAILURE
                    self.context.blackboard.set('NowProcessInstructionStatus', py_trees.common.Status.FAILURE)
                    self._now_working = False

                    self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                    self.rocon_logger.debug(' worker >> on_post_process_instructions  ', show_caller_info=False)
                    self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
                    await self.context.worker.on_post_process_instructions(instructions, is_success=False)

                    self.async_task_status = py_trees.common.Status.FAILURE
                    return

        # for testing of infinite instructions loop
        if USE_DEBUG_TEST_1HOUR_INSTRUCTIONS_LOOP:
            self.rocon_logger.debug('start USE_DEBUG_TEST_1HOUR_INSTRUCTIONS_LOOP')
            await asyncio.sleep(60 * 60)
            self.rocon_logger.debug('stop USE_DEBUG_TEST_1HOUR_INSTRUCTIONS_LOOP')

        result = {
            'current': None,
            'status': 'success',
            'status_msg': 'finished successfully'
        }
        self.context.blackboard.update_report_result(result)
        self.rocon_logger.debug('finally reportResult updated')

        self._now_working = False
        self.context.blackboard.set('NowProcessInstructionStatus', py_trees.common.Status.SUCCESS)

        self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        self.rocon_logger.debug(' worker >> on_post_process_instructions  ', show_caller_info=False)
        self.rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        await self.context.worker.on_post_process_instructions(instructions, is_success=is_success)

        self.async_task_status = py_trees.common.Status.SUCCESS


    def update(self):

        if self.async_task_status is py_trees.common.Status.RUNNING:
            pass


        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)


class TaskCheckForcedStop(AsyncTask):
    def __init__(self, name="checkForcedStop"):
        super(TaskCheckForcedStop, self).__init__(name)

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



        self.async_task_status = py_trees.common.Status.SUCCESS

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status


class TaskFinishReport(AsyncTask):
    def __init__(self, name="finishReport"):
        super(TaskFinishReport, self).__init__(name)

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
        # TaskFinishReport
        report = self.context.blackboard.get_report()
        result_status = pydash.get(report, 'result.status')
        if result_status == 'success':

            try:
                update = {'finished_at': current_datetime_utc_iso_format(), 'status': 'finished'}
                self.context.blackboard.set_report(update)

                await self.context.blackboard.sync_report()

                del update

            except Exception as err:
                self.rocon_logger.error('Exception occurred', exception=err)
                #err.with_traceback()
        else:
            self.rocon_logger.error('unknown status of report result')

        del report
        del result_status

        self.context.blackboard.clear_report()
        #self.context.blackboard.set_status('idle')
        #self.context.blackboard.set('NowProcessInstructionStatus', None)
        self.async_task_status = py_trees.common.Status.SUCCESS

    def update(self):
        self.rocon_logger.debug('update >> {}'.format(self.async_task_status), module_keyword=BT_KEYWORD)
        return self.async_task_status

    def terminate(self, new_status):
        self.rocon_logger.debug("terminate >>", module_keyword=BT_KEYWORD)
