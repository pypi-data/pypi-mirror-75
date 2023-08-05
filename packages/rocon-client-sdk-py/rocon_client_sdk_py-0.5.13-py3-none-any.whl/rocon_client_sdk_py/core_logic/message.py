import abc
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger


class Message(object):
    def __init__(self):
        self.name = 'Not_defined'
        self.func_name = 'Not_defined'
        self.rocon_logger = rocon_logger

        self._context = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abc.abstractmethod
    async def on_handle(self, message_body):
        raise NotImplementedError("Please Implement this method")
