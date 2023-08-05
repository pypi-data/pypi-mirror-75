import pydash
import os
from .worker import Worker


class VirtualWorker(Worker):

    def __init__(self, uuid, worker_name, client_configs, event_loop, working_root, hooks_def_path=None, acts_def_path=None, msgs_def_path=None):

        # 경로 재정의
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hooks_def_path = '{}/virtual_core/hooks'.format(dir_path)
        acts_def_path = '{}/virtual_core/actions'.format(dir_path)
        msgs_def_path = '{}/virtual_core/messages'.format(dir_path)

        super().__init__(uuid, worker_name, client_configs, event_loop, working_root, hooks_def_path, acts_def_path, msgs_def_path)

    async def on_hook(self, hook, hook_body):
        return await hook.on_handle(hook_body)

    async def on_message(self, message, message_body):
        return await message.on_handle(message_body)

    async def on_pre_process_instructions(self, instructions):
        pass

    async def on_process_instruction(self, action, args):
        return await action.on_perform(args)

    async def on_post_process_instructions(self, instructions, is_success):
        pass

    async def on_check_offline_status(self, current_status):
        return True

    async def on_check_error_status(self, current_status):
        return True

    async def get_dev_path_finding_map(self):
        return