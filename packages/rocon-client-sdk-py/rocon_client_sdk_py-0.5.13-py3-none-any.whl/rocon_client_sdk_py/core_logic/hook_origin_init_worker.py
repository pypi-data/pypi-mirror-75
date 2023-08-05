import abc
from .hook import Hook

NAME = 'HookInitWorker'


class HookOriginInitWorker(Hook):

    def __init__(self):
        super().__init__()
        self.name = NAME

    @abc.abstractmethod
    async def on_handle(self, worker_record):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def name():
        return NAME