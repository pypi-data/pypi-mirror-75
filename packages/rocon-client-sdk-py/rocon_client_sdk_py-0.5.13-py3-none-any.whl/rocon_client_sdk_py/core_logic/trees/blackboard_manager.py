import py_trees
import pydash
import gc
import sys
from .constants import *
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.const import *


class BlackboardManager():
    def __init__(self, context):

        #py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)

        self._board = py_trees.blackboard.Client(name=MASTER_BLACKBOARD_NAME)
        self._board.register_key(key=KEY_CONTEXT, access=py_trees.common.Access.WRITE)
        self._board.context = context

        context.blackboard = self

    @property
    def context(self):
        return self._board.context

    def get(self, key):

        if self._board.is_registered(key, py_trees.common.Access.READ):
            return self._board.get(key)

        else:
            return None

    def set_status(self, value):
        self.set('status', value)

        status = {'status': value}
        self.set_worker_content(status)
        del status

    def set(self, key, value):

        if self._board.is_registered(key=key) is False:
            self._board.register_key(key=key, access=py_trees.common.Access.READ, required=True)
            self._board.register_key(key=key, access=py_trees.common.Access.WRITE, required=True)

        self._board.set(key, value)


    def get_sub(self, key, sub_key):
        data = self.get(key)
        if data:
            return data[sub_key]
        else:
            return None

    def get_worker_content(self, sub_key=None):
        #self.context.rocon_logger.debug(show_caller_info=True)

        if sub_key is None:
            org_worker = self.get('worker')
            update = self.get_worker_content_update()

            if org_worker is None:
                return update

            if update is None:
                return org_worker

            worker = pydash.assign({}, org_worker, update)
            del org_worker
            del update

            return worker
        else:
            return self.get_sub('worker', sub_key)

    def set_worker_content(self, update):
        #self.context.rocon_logger.debug(show_caller_info=True)

        wu = self.get('worker_update')
        if wu:
            worker_update = pydash.assign({}, wu, update)
            del wu
        else:
            worker_update = pydash.assign({}, update)

        self.set('worker_update', worker_update)

        del worker_update

    def get_worker_content_update(self):
        #self.context.rocon_logger.debug(show_caller_info=True)

        return self.get('worker_update')

    def set_worker_update(self, update):
        #self.context.rocon_logger.debug(show_caller_info=True)

        worker_update = self.get('worker_update')
        if worker_update:
            new_update = pydash.assign({}, worker_update, update)
        else:

            new_update = pydash.assign({}, update)

        self.set('worker_update', new_update)

    def get_update_worker_body(self):
        update = self.get_worker_content_update() or {}
        worker_content = self.get_worker_content()

        for key in update:
            if worker_content and worker_content.get(key):
                update[key] = worker_content[key]

        return update

    async def sync_worker(self):
        #self.context.rocon_logger.debug(show_caller_info=True)

        try:
            if self.get_worker_content_update() is None:
                return self.get_worker_content()

            worker_content = self.get_worker_content()
            body = self.get_update_worker_body()

            assert(worker_content is not None)

            updated_worker = await self.context.api_worker.update_worker(worker_content['id'], body)
            if updated_worker:
                self.context.blackboard.set('worker', updated_worker)

            self.context.blackboard.set('worker_update', None)
            worker_content = self.get_worker_content()
            self.context.rocon_logger.debug(worker_content, module_keyword=BT_KEYWORD)
        except Exception as err:
            self.context.rocon_logger.error('Exception Occurred', exception=err)


        return worker_content

    def get_report(self):

        org_report = self.get('report')
        update = self.get_report_update()

        if org_report is None and update is None:
            return None

        if org_report is None:
            del org_report
            report = pydash.assign({}, update)
            return report

        if update is None:
            report = pydash.assign({}, org_report)
            del org_report
            return report

        report = pydash.assign({}, org_report, update)

        del org_report
        del update

        return report

    def set_report(self, update):
        if update is None:
            return

        ru = self.get('report_update')
        if ru:
            report_update = pydash.assign({}, ru, update)
            del ru
        else:
            report_update = pydash.assign({}, update)

        self.set('report_update', report_update)

        del report_update

    def get_report_update(self):
        return self.context.blackboard.get('report_update')

    def set_report_update(self, update):
        return self.context.blackboard.set('report_update', update)

    def get_update_report_body(self):
        update = self.get_report_update() or {}
        report = self.get_report()

        for key in update:
            if report and report.get(key):
                update[key] = pydash.get(report, key)

        del report

        return update

    async def sync_report(self):

        try:
            worker_content = self.get_worker_content()
            body = self.get_update_report_body()

            body['worker'] = pydash.get(worker_content, 'id')
            report = self.get_report()

            id = None
            updated_report = None

            if report:
                id = pydash.get(report, 'id')
                updated_report = await self.context.api_report.update_report(id, body)
                if updated_report:
                    self.context.blackboard.set('report', updated_report)

            self.context.blackboard.set('report_update', None)

            del id
            del body
            del worker_content
            del report
            del updated_report

        except Exception as err:
            self.context.rocon_logger.error('Exception Occurred', exception=err)

    def set_forced_idle_status(self):
        self.context.blackboard.clear_report()
        self.context.blackboard.set_status('idle')
        self.context.blackboard.set('NowProcessInstructionStatus', None)

    def clear_report(self):
        self.context.blackboard.set('report', None)
        self.context.blackboard.set('report_update', None)

    def update_report_result(self, result):
        try:
            report = self.get_report()
            if report is None:
                rocon_logger.debug('report is None')

            if report != None and 'result' in report:
                #updated_result = report['result']
                updated_result = pydash.assign({}, pydash.get(report, 'result'))
            else:
                updated_result = {}


            if 'status' in result:
                pydash.set_(updated_result, 'status', result['status'])

            if 'status_msg' in result:
                pydash.set_(updated_result, 'status_msg', result['status_msg'])

            if 'returns' in result:
                pydash.set_(updated_result, 'returns', result['returns'])

            if 'current' in result:
                pydash.set_(updated_result, 'current', result['current'])

            new_result = {'result': updated_result}
            self.context.blackboard.set_report(new_result)

            del report
            del updated_result
            del new_result

        except Exception as err:
            self.context.rocon_logger.error('Exception occurred', exception=err)

    def update_instruction_result(self, result):
        report = self.context.blackboard.get_report()
        if report is None:
            self.context.rocon_logger.debug('update_instruction_result is None')
            return

        returns = pydash.get(report, 'result.returns') or []
        idx = pydash.find_index(returns, {'id': result['id']})
        if idx != -1:
            pydash.assign(returns[idx], result)
        else:
            returns.append(result)

        self.update_report_result({'returns': returns})


        """
            'trees' 구조 
            {
              trees: {
                '1ac7f790-0cb2-4855-b72a-3dba48c6b5e1': { tree: [Object], treeMemory: [Object], node: [Object] }
              },
              shared: {}
            }
        """

    def get_blackborad_info(self):

        dic_data = {
            'trees': {},
            'shared': {}
        }

        id = self.context.worker.tree_manager.get_tree_id()
        dic_data['trees'][str(id)] = {
            'tree': {
                # 생략
            },
            'treeMemory': {
                # 생략
            },
            'node': self.get_all_node_status()
        }

        return dic_data

    def get_all_node_status(self):
        tree_mgr = self._board.context.worker.tree_manager
        return tree_mgr.get_trees_status()

    def get_blackboard_data(self):
        data = {
            'trees': pydash.reduce_()
        }
        return data

    def reset_blackboard(self):
        rocon_logger.debug('reset blackboard')
