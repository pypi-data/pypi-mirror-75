import py_trees
import asyncio
from .constants import *
from rocon_client_sdk_py.core_logic.context import Context
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.utils.util import *

class CommonBlackBoard(metaclass=SingletonMetaClass):
    def __init__(self):
        self._blackboard = None
        self._context = None

    @property
    def blackboard(self):
        return self._blackboard

    @property
    def context(self):
        return self._context

    def set(self, blackboard):
        self._blackboard = blackboard

        if self._blackboard.is_registered(KEY_CONTEXT) is False:
            self._blackboard.register_key(key=KEY_CONTEXT, access=py_trees.common.Access.READ)

        if self._context is None:
            self._context = self._blackboard.get(KEY_CONTEXT)


class TaskBase(py_trees.behaviour.Behaviour):
    def __init__(self, name="NoNamed"):
        super(TaskBase, self).__init__(name)
        self.rocon_logger = rocon_logger
        self._blackboard = None
        self._context = None

    @property
    def context(self) -> Context:
        if self._blackboard is None:

            test_singletone = False

            if test_singletone:
                cbb = CommonBlackBoard()
                if cbb.blackboard is None:
                    bb = py_trees.blackboard.Client(name=MASTER_BLACKBOARD_NAME)
                    cbb.set(bb)

                self._blackboard = cbb.blackboard
                self._context = cbb.context
                return self._context

            self._blackboard = py_trees.blackboard.Client(name=MASTER_BLACKBOARD_NAME)
            if self._blackboard.is_registered(KEY_CONTEXT) is False:
                self._blackboard.register_key(key=KEY_CONTEXT, access=py_trees.common.Access.READ)

            if self._context is None:
                self._context = self._blackboard.get(KEY_CONTEXT)

        return self._context

    @asyncio.coroutine
    def bug(self):
        raise Exception('not consumed')

    def check_valid_interval(self, req_interval_ms, last_updated_ms):
        '''
        마지막 업데이트된 시간과 현재 시간 갭이 주어진 req_interval 보다 같거나 크면 True 리턴, 그렇지 않으면 False 리턴
        :param req_interval: ms
        :param last_updated_at: ms
        :return:
        '''
        curnt_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
        gap = curnt_time_ms - last_updated_ms

        if gap < req_interval_ms:
            return False

        return True


class Task(TaskBase):
    def __init__(self, name="Task NoNamed"):
        super(Task, self).__init__(name)


class AsyncTask(TaskBase):
    def __init__(self, name="AsyncTask NoNamed"):
        super(AsyncTask, self).__init__(name)

        self.async_task_status = py_trees.common.Status.INVALID
