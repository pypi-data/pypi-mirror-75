import abc
from .hook import Hook

NAME = 'HookCheckRevision'


class HookOriginCheckRevision(Hook):

    def __init__(self):
        super().__init__()
        self.name = NAME

    @abc.abstractmethod
    async def on_handle(self, updated_report):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def name():
        return NAME