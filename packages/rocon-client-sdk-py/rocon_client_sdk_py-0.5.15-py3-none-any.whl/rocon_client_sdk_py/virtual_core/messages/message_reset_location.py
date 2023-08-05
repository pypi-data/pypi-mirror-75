import pydash
from rocon_client_sdk_py.core_logic.message import Message


class ResetLocation(Message):
    def __init__(self):
        super().__init__()
        self.name = 'resetLocation'

    async def on_handle(self, message_body):
        worker_content = self.context.blackboard.get_worker_content()
        location = pydash.get(worker_content, 'type_specific.location')
        updated_type_specific = worker_content['type_specific']
        updated_type_specific['location'] = pydash.assign({}, location, message_body)
        self.context.blackboard.set_worker_content({'type_specific': updated_type_specific})
        await self.context.blackboard.sync_worker()
        return True