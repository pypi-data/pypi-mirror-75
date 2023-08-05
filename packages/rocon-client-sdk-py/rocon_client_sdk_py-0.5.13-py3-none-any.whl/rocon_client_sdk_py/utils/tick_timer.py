import threading
from datetime import timedelta


class TickTimer(threading.Thread):
    def __init__(self, interval_sec, callback_func, repeat=True, *args, **kwargs):
        threading.Thread.__init__(self)
        self._repeat = repeat

        self.daemon = False
        self.stopped = threading.Event()
        self.interval = timedelta(seconds=interval_sec)
        self.excute = callback_func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            self.excute(*self.args, **self.kwargs)

            if self._repeat == False:
                break

        print('done')

    def stop(self):

        self.stopped.set()
        self.join()

    def cancel(self):
        self.stop()