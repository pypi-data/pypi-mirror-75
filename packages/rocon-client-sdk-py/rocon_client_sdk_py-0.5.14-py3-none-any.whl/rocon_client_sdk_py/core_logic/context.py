import json
from .action_manager import ActionManager
from .hook_manager import HookManager
from .message_manager import MessageManager
from .trees.blackboard_manager import BlackboardManager
from .map_manager import MapManager
from rocon_client_sdk_py.rocon_apis import ApiTask
from rocon_client_sdk_py.rocon_apis import ApiWorker
from rocon_client_sdk_py.rocon_apis import ApiWorkerPool
from rocon_client_sdk_py.rocon_apis.api_report import ApiReport
from rocon_client_sdk_py.rocon_apis.api_site_configuration import ApiSiteConfiguration


class Context():
    def __init__(self, worker, event_loop):
        worker.rocon_logger.debug('initializing Context')
        self._worker = worker
        self._is_booted = False

        self._hook_mgr = HookManager(self)
        self._act_mgr = ActionManager(self)
        self._msg_mgr = MessageManager(self)
        self._blackboard_mgr = None
        self._event_loop = event_loop

        self._map_mgr = MapManager(self._worker.httpclient.api_site_config,
                                   event_loop,
                                   self._worker._working_root
                                   )

        self._raise_test_exception = True

    @property
    def api_report(self) -> ApiReport:
        return self._worker.httpclient.api_report

    @property
    def api_task(self) -> ApiTask:
        return self._worker.httpclient.api_task

    @property
    def api_worker(self) -> ApiWorker:
        return self._worker.httpclient.api_worker

    @property
    def api_worker_pool(self) -> ApiWorkerPool:
        return self._worker.httpclient.api_worker_pool

    @property
    def api_site_configuration(self) -> ApiSiteConfiguration:
        return self._worker.httpclient.api_site_config

    @property
    def event_loop(self):
        return self._event_loop

    @property
    def worker(self):
        return self._worker

    @property
    def action_manager(self):
        return self._act_mgr

    @property
    def blackboard(self):
        return self._blackboard_mgr

    @property
    def message_manager(self):
        return self._msg_mgr

    @property
    def hook_manager(self):
        return self._hook_mgr

    @property
    def map_manager(self):
        return self._map_mgr

    @blackboard.setter
    def blackboard(self, blackboard_manager:BlackboardManager):
        self._blackboard_mgr = blackboard_manager

    @property
    def is_booted(self):
        return self._is_booted

    @is_booted.setter
    def is_booted(self, value:bool):
        self._is_booted = value

    @property
    def rocon_logger(self):
        return self.worker.rocon_logger

    def get_trees_stringify(self):

        trees_data ={
            'treeId': str(self.worker.tree_manager.get_tree_id()),
            'tree': self.worker.tree_manager.get_trees_info(),
            'bb': self.blackboard.get_blackborad_info()
        }

        json_data = json.dumps(trees_data)
        return json_data

    def get_working_dir(self):
        return self._working_dir


    @property
    def raise_test_exception(self):
        return self._raise_test_exception

    @raise_test_exception.setter
    def raise_test_exception(self, value:bool):
        self._raise_test_exception = value