from rocon_client_sdk_py.logger.rocon_logger import rocon_logger

ERROR_HANDLING_LEVEL_SHOW_MESSAGE_ONLY = 0
ERROR_HANDLING_LEVEL_STOP_IMMEDIATELY = 1


class Api():
    def __init__(self, httpclient):
        self._httpclient = httpclient
        self._rocon_logger = rocon_logger
        self._error_handling_level = ERROR_HANDLING_LEVEL_STOP_IMMEDIATELY

    @property
    def rocon_logger(self):
        return self._rocon_logger

    @property
    def error_handling_level(self):
        return self._error_handling_level

    def error_handling(self, response):

        try:
            if self._error_handling_level == ERROR_HANDLING_LEVEL_STOP_IMMEDIATELY:
                raise Exception('ERROR_HANDLING_LEVEL_STOP_IMMEDIATELY')

        except Exception as err:
            err.with_traceback()