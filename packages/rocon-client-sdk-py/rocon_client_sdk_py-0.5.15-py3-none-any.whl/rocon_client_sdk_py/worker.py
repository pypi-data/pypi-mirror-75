import pydash
import abc
from abc import ABC
from rocon_client_sdk_py.utils.tick_timer import TickTimer
from rocon_client_sdk_py.rocon_apis.http_client import HttpClient
from rocon_client_sdk_py.core_logic.trees.behavior_tree_manager import BehaviorTreeManager
from rocon_client_sdk_py.core_logic.context import Context
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.const import *


class Worker(ABC):
    """
    Worker class
    """
    def __init__(self, uuid, worker_name, client_configs: dict, event_loop, working_root, hooks_def_path, acts_def_path, msgs_def_path):
        """
        :param uuid:            - name of virtualWorker
        :param act_def_paths:   - path of action files
        :param msg_def_paths:   - path of messages
        :param client_configs:  - options object {tickInterval, updateInterval, initWork, configs}
        """
        self._multi_client_options = None
        self._rocon_logger = rocon_logger
        self._rocon_logger.debug('initializing worker')

        self._uuid = uuid
        self._worker_name = worker_name
        self._working_root = working_root
        self._hooks_def_path = hooks_def_path
        self._acts_def_path = acts_def_path
        self._msgs_def_path = msgs_def_path

        self._client_configs = client_configs

        self._call_back_after_tick = None


        if event_loop:
            self.initialize(event_loop)


    def initialize(self, event_loop):
        self._rocon_logger.debug()

        self._tick_interval = pydash.get(self._client_configs, 'tickInterval') or DEFAULT_TICK_INTERVAL_MS
        self._update_interval = pydash.get(self._client_configs, 'updateInterval') or DEFAULT_UPDATE_WORKER_INTERVAL_MS

        self._initial_worker = pydash.get(self._client_configs, 'initialWorker') or {}
        self._configs = pydash.get(self._client_configs, 'configs') or {}

        self._event_loop = event_loop
        self._httpclient = self._init_http_client()

        self._tick_timer = None
        self._context = Context(self, event_loop)

        self._behavior_mgr = BehaviorTreeManager(self._context)
        self._behavior_mgr.blackboard.set('uuid', self._uuid)
        self._behavior_mgr.blackboard.set('configs', self._configs)
        self._behavior_mgr.blackboard.set('actionDefinePaths', self._acts_def_path)
        self._behavior_mgr.blackboard.set('messageDefinePaths', self.msg_def_paths)
        self._behavior_mgr.blackboard.set('tickInterval', self._tick_interval)
        self._behavior_mgr.blackboard.set('updateInterval', self._update_interval)


    @property
    def uuid(self):
        return self._uuid

    @property
    def worker_name(self):
        return self._worker_name

    @property
    def act_def_paths(self):
        return self._acts_def_path

    @property
    def msg_def_paths(self):
        return self._msgs_def_path

    @property
    def httpclient(self):
        return self._httpclient

    @property
    def event_loop(self):
        return self._event_loop

    @property
    def rocon_logger(self):
        return self._rocon_logger

    @property
    def client_configs(self):
        return self._client_configs

    @property
    def task_name(self):
        name = self._configs['taskName']
        return name

    @property
    def multi_client_options(self):
        return self._multi_client_options

    def _init_http_client(self):
        hostname = pydash.get(self._configs, 'hostname.concert')
        siteconf = pydash.get(self._configs, 'hostname.siteConfig')
        worker_pool = pydash.get(self._configs, 'hostname.workerPool')

        httpclient = HttpClient(hostname_concert=hostname, hostname_site_config=siteconf, hostname_worker_pool=worker_pool)
        return httpclient

    def reset(self):
        self.stop()

        self._rocon_logger.debug()
        self._initialize(self._uuid, self._acts_def_path, self._msgs_def_path, self._client_configs, self._event_loop)

    def reset_blackboard(self):
        self._behavior_mgr.blackboard.reset_blackboard()

    def tick(self):
        self._rocon_logger.debug(module_keyword=BT_KEYWORD)

        self._behavior_mgr.tick()
        self.after_tick(self.context)

    def after_tick(self, context):

        if self._call_back_after_tick:
            self._call_back_after_tick(context)

    @property
    def context(self):
        return self._context

    @property
    def tree_manager(self):
        return self._behavior_mgr

    @abc.abstractmethod
    async def on_hook(self, hook, hook_body):
        raise NotImplementedError("Please Implement this method... must call 'await hook.on_handle(hook_body)'\n")

    @abc.abstractmethod
    async def on_message(self, message, message_body):
        raise NotImplementedError("Please Implement this method... must call 'await message.on_handle(message_body)'\n")

    async def on_pre_process_instructions(self, instructions):
        pass

    @abc.abstractmethod
    async def on_process_instruction(self, action, args):
        raise NotImplementedError("Please Implement this method... must call 'await action.on_perform(args)'\n")

    async def on_post_process_instructions(self, instructions, is_success):
        pass

    async def on_check_offline_status(self, current_status):
        return True

    async def on_check_error_status(self, current_status):
        return True

    @abc.abstractmethod
    async def on_load_task(self, task_name):
        raise NotImplementedError("Please Implement this method... must call 'await action.on_load_task(task_name)'\n")


    @property
    def tick_interval(self):
        return self._tick_interval

    @tick_interval.setter
    def tick_interval(self, interval):
        self._tick_interval = interval

    def to_json(self):
        json_data = {
            'uuid': self._uuid,
            'actionDefinePaths': self._acts_def_path,
            'messageDefinePaths': self._msgs_def_path,
            'tickInterval': self.tick_interval,
            'isRunning': True,
            'worker': self.context.blackboard.get_worker_content(),
            'blackboard': self.context.blackboard.get_blackborad_info()
        }

        return json_data

    def start(self, interval_msec = DEFAULT_TICK_INTERVAL_MS):
        self._rocon_logger.debug()
        self.start_tick_timer(interval_msec)

    def stop(self, offline = False):
        self._rocon_logger.debug()
        self.stop_tick_timer()

    def start_tick_timer(self, interval_msec=DEFAULT_TICK_INTERVAL_MS):
        self._rocon_logger.debug()

        self.stop_tick_timer()
        self.tick_interval = interval_msec
        interval_sec = interval_msec / 1000

        self._tick_timer = None
        self._tick_timer = TickTimer(interval_sec, self.tick)

        self._tick_timer.start()

    def stop_tick_timer(self):
        if self._tick_timer:
            self._tick_timer.cancel()

        self._tick_timer = None

    def set_after_tick_callback(self, callback):
        self._call_back_after_tick = callback

    def change_task_name(self, task_name):
        self._configs['taskName'] = task_name

        self._behavior_mgr.blackboard.set('configs', self._configs)



