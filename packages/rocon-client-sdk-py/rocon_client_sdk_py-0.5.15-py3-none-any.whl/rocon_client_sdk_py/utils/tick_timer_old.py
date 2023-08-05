from threading import Timer
'''
Timer를 이용한 repeat timer 구현시 instance를 생성 소멸 반복시 RSS의 linear한 증가가 보인다.
따라서 대체 구현으로 threading.Event를 사용하는 TickTimer 사용을 권함.
'''

class TickTimerOld():
    def __init__(self, interval_sec, callback_func, repeat=True):
        self._repeat = repeat
        self._interval_sec = interval_sec
        self._callback_func = callback_func
        self._thread = Timer(self._interval_sec, self._handle_func)

    def _handle_func(self):

        if self._callback_func:
            self._callback_func()

        if self._thread:
            self._thread.cancel()
            self._thread = None

        if self._repeat is True:
            self._thread = Timer(self._interval_sec, self._handle_func)
            self._thread.start()

    def start(self):
        self._thread.start()

    def cancel(self):

        if self._thread:
            self._thread.cancel()

        self._thread = None
        self._callback_func = None

