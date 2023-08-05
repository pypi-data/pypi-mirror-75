import logging
import inspect
import sys
import linecache
import glob
import os
from logging.handlers import RotatingFileHandler
from rocon_client_sdk_py.utils.util import *


DEFAULT_SHOW_CALLER_INFO = True
DEFAULT_SAVE_TO_SERVER = False

MAX_LOG_FILESIZE = 1024*1024*3
MAX_LOG_BACKUP_COUNT = 50


class RoconLogger(metaclass=SingletonMetaClass):
    def __init__(self, max_filesize = MAX_LOG_FILESIZE, max_backup_count=MAX_LOG_BACKUP_COUNT):
        self.show_caller_info = DEFAULT_SHOW_CALLER_INFO
        self.enable = True

        self.enabled_remove_old_logs = True


        self._path = 'log'
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        else:

            if self.enabled_remove_old_logs is True:
                #log_files = glob.glob('{}/rocon_*_utc_*'.format(self._path), recursive=False)
                log_files = glob.glob('{}/rocon*'.format(self._path), recursive=False)
                for f in log_files:
                    try:
                        os.remove(f)
                    except OSError as e:
                        print("Error: %s : %s" % (f, e.strerror))


        self._logging_level = logging.DEBUG

        self._logger = logging.getLogger('RoconLogger')
        self._logger.setLevel(self._logging_level)

        self._formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        self._log_filename = None

        self._max_backup_count = max_backup_count
        self._max_filesize = max_filesize

        self._console_handler = None
        self.enable_console_handler(enable=True)

        self._file_handler = None
        self.enable_file_handler(enable=True)

        self._disabled_logging_module_keywords = set()

    def enable_console_handler(self, enable=True):
        if enable is False:
            if self._console_handler:
                self._logger.removeHandler(self._console_handler)

            self._console_handler = None
        else:
            if self._console_handler is None:

                self._console_handler = logging.StreamHandler()
                self._console_handler.setLevel(self._logging_level)
                self._console_handler.setFormatter(self._formatter)
                self._logger.addHandler(self._console_handler)

    def enable_file_handler(self, enable=True, pre_fix=None):

        if self._log_filename is not None and os.path.exists(self._log_filename):
            os.remove(self._log_filename)


        current_time = current_datetime_iso_format()
        current_utc_time = current_datetime_utc_iso_format()

        if pre_fix:
            #self._log_filename = '{}/rocon_{}_{}_utc_{}.log'.format(self._path, pre_fix, current_time, current_utc_time)
            self._log_filename = '{}/rocon_{}.log'.format(self._path, pre_fix)
        else:
            #self._log_filename = '{}/rocon_{}_utc_{}.log'.format(self._path, current_time, current_utc_time)
            self._log_filename = '{}/rocon.log'.format(self._path)

        if self._file_handler:
            self._logger.removeHandler(self._file_handler)
            self._file_handler = None

        if enable is True:
            if self._file_handler is None:
                self._file_handler = RotatingFileHandler(self._log_filename, mode='a', maxBytes=self._max_filesize,
                                                         backupCount=self._max_backup_count, encoding=None, delay=0)
                self._file_handler.setFormatter(self._formatter)
                self._logger.addHandler(self._file_handler)


    def debug(self, log_msg='', module_keyword = '', show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if self.enable is False:
            return

        if module_keyword in self._disabled_logging_module_keywords:
            return

        caller_info = self._get_caller_info(inspect.currentframe().f_back, show_caller_info)
        mod_keyword = '[{}] '.format(module_keyword) if len(module_keyword) > 0 else ''
        text = '{}{}{}'.format(mod_keyword, caller_info, log_msg)
        self._logger.debug(text)

    def info(self, log_msg='', module_keyword = '', show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if self.enable is False:
            return

        caller_info = self._get_caller_info(inspect.currentframe().f_back, show_caller_info)
        mod_keyword = '[{}] '.format(module_keyword) if len(module_keyword) > 0 else ''
        text = '{}{}{}'.format(mod_keyword, caller_info, log_msg)
        self._logger.info(text)

    def cli_info(self, log_msg='', module_keyword = '', show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if self.enable is False:
            return

        caller_info = self._get_caller_info(inspect.currentframe().f_back, show_caller_info)
        mod_keyword = '[{}] '.format(module_keyword) if len(module_keyword) > 0 else ''
        text = '{}{}{}'.format(mod_keyword, caller_info, log_msg)
        print(text)

    def warning(self, log_msg='', module_keyword = '', show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if self.enable is False:
            return

        caller_info = self._get_caller_info(inspect.currentframe().f_back, show_caller_info)
        mod_keyword = '[{}] '.format(module_keyword) if len(module_keyword) > 0 else ''
        text = '{}{}{}'.format(mod_keyword, caller_info, log_msg)
        self._logger.warning(text)

    def error(self, log_msg='', module_keyword = '', show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if self.enable is False:
            return

        caller_info = self._get_caller_info(inspect.currentframe().f_back, show_caller_info)
        mod_keyword = '[{}] '.format(module_keyword) if len(module_keyword) > 0 else ''

        exc_type, exc_obj, tb = sys.exc_info()
        if tb:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            if exception:
                linecache.checkcache(filename)
                line = linecache.getline(filename, lineno, f.f_globals)
                self._logger.error('EXCEPTION in \n{}\nLINE : {}\n"{}"\n : {}'.format(filename, lineno, line.strip(), exc_obj))
            else:
                self._logger.error('ERROR in \n{}\nLINE : {}'.format(filename, lineno))

        text = '{}{}{}'.format(mod_keyword, caller_info, log_msg)
        self._logger.error(text)

    def critical(self, log_msg='', module_keyword = '', show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if self.enable is False:
            return

        caller_info = self._get_caller_info(inspect.currentframe().f_back, show_caller_info)

        mod_keyword = '[{}] '.format(module_keyword) if len(module_keyword) > 0 else ''
        exc_type, exc_obj, tb = sys.exc_info()
        if tb:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            if exception:
                linecache.checkcache(filename)
                line = linecache.getline(filename, lineno, f.f_globals)
                self._logger.error('EXCEPTION in \n{}\nLINE : {}\n"{}"\n : {}'.format(filename, lineno, line.strip(), exc_obj))
            else:
                self._logger.error('ERROR in \n{}\nLINE : {}'.format(filename, lineno))

        text = '{}{}{}'.format(mod_keyword, caller_info, log_msg)
        self._logger.critical(text)

    def _get_caller_info(self, frame, show_caller_info=DEFAULT_SHOW_CALLER_INFO, save_to_server=DEFAULT_SAVE_TO_SERVER, exception=None):
        if show_caller_info is False or self.show_caller_info is False:
            return ''

        if 'self' in frame.f_locals:
            # caller is method of class
            caller_class_name = frame.f_locals["self"].__class__.__name__
            caller_method_name = frame.f_code.co_name

            caller_info = '{}.{}() : '.format(caller_class_name, caller_method_name)
        else:
            caller_method_name = frame.f_code.co_name
            caller_info = '{}() : '.format(caller_method_name)


        return caller_info

    def disable_logging_by_moduel_keyword(self, keyword):
        self._disabled_logging_module_keywords.add(keyword)
        #print(self._disabled_logging_module_keywords)

    def enable_logging_by_moduel_keyword(self, keyword):

        if keyword in self._disabled_logging_module_keywords:
            self._disabled_logging_module_keywords.remove(keyword)


rocon_logger = RoconLogger()
