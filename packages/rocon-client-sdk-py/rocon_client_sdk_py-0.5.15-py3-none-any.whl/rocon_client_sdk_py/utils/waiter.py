import threading
import asyncio
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.utils.tick_timer import TickTimer
from threading import Timer


class Waiter():
    def __init__(self, name, event_loop, timeout_msec = -1):
        self._name = name
        self._timeout_msec = timeout_msec
        self._event = Subject()
        self._wait_exit = False
        self.result_ob = None
        self._event_loop = event_loop
        self._timer = None

        self.scheduler = AsyncIOScheduler(loop=event_loop)
        self.done = asyncio.Future()


    def set_timeout(self, timeout_msec):
        self._timeout_msec = timeout_msec

    def _timeout_callback(self):

        self._event.on_next('timeout')

    async def wait(self):

        try:
            if self._timeout_msec > 0:
                #self._timer = threading.Timer(self._timeout_msec/1000, self._timeout_callback)
                if self._timer:
                    self._timer.cancel()
                    self._timer = None

                self._timer = Timer(self._timeout_msec/1000, self._timeout_callback)
                self._timer.start()

            self._wait_exit = False

            def cb_next(data):
                try:
                    if self._timer:
                        self._timer.cancel()
                        self._timer = None

                    rocon_logger.debug('waiter({}) callback next : {}'.format(self._name, data))
                    self._wait_exit = True
                    self.done.set_result(data)

                    self._event = None
                except Exception as err:
                    rocon_logger.error('Waiter error occurred : {}'.format(err), exception=err)

            def cb_completed():
                try:
                    self.done.set_result('done')

                except Exception as err:
                    rocon_logger.error('Waiter error occurred : {}'.format(err), exception=err)

            #self._event.subscribe(on_next=cb_next, on_completed=cb_completed, scheduler=self.scheduler)
            self._event.subscribe(on_next=cb_next, scheduler=self.scheduler)
            result = await self.done

        except Exception as error:
            rocon_logger.error('Waiter error occurred : {}'.format(error), exception=error)

        return result

    def end(self, msg):

        if self._event:
            self._event.on_next(msg or 'success')
            self._event.on_completed()
        #self.result_ob.dispose()

    def set_next(self, msg):

        if self._event:
            self._event.on_next(msg)


    def cancel(self):
        #TODO
        pass