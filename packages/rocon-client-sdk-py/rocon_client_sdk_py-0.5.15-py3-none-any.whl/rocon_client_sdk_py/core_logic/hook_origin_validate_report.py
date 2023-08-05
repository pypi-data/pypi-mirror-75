import abc
from .hook import Hook

NAME = 'HookValidateReport'


class HookOriginValidateReport(Hook):

    def __init__(self):
        super().__init__()
        self.name = NAME

    @abc.abstractmethod
    async def on_handle(self, validate_status = None):
        '''
        validate_status : {'running', 'finished', 'empty', 'error'}
        running 경우 정상적인 job의 수행 중 상태,
        finished 경우 FMS에서 job을 취소했을때,
        empty의 경우 instruction내용이 없는 경우,
        error의 경우 기타 비정상적인 상황,

        3가지의 경우 현재 수행하고 있는 instructions가 있다면 취소하고 idle상태로 전이한다.
        코어엔진에서는 instructions 루프를 자동으로 강제 중단하며,
        custom 영역에서는 현재 로봇의 제어를 중단해야한다.
        '''

        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def name():
        return NAME