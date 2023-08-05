import time
import yaml
import os
import psutil
from datetime import datetime


'''
    usage : class AnyCalss(metaclass=SingletonMetaClass):
'''


class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_time_sec(dtstr):
    #now = dt.now()
    dtstr = dtstr.replace('T', ' ')
    dtstr = dtstr.replace('Z', '')
    dtn = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S.%f')

    curnt_time_sec = time.mktime(dtn.timetuple()) + dtn.microsecond/1000000.0
    #curnt_time_ms = curnt_time_sec*1000

    return curnt_time_sec


def get_time_milliseconds(dtstr):
    """
    :param dtn: string datetime format as '%Y-%m-%dT%H:%M:%S.%f'
    :return:
    """
    sec = get_time_sec(dtstr)
    return sec*1000


def current_datetime_iso_format():
    datetime_now = datetime.now()
    isostring = datetime.strftime(datetime_now, '%Y-%m-%dT%H:%M:%S')
    return isostring.format(int(round(datetime_now.microsecond / 1000.0)))


def current_datetime_utc_iso_format():
    utc_datetime = datetime.utcnow()

    isostring = datetime.strftime(utc_datetime, '%Y-%m-%dT%H:%M:%S.{0}Z')
    return isostring.format(int(round(utc_datetime.microsecond/1000.0)))


def load_dict_from_yaml(filepathname) -> dict:
    try:
        config_dic = yaml.load(open(filepathname), Loader=yaml.FullLoader)

        return config_dic
    except yaml.YAMLError as exc:

        return None

def save_to_yaml(filepathname, config_dic):
    try:
        with open(filepathname, 'w') as f:
            f.write(yaml.safe_dump(config_dic))
    except yaml.YAMLError as err:
        return None


def show_memory_usage(logger, uuid=None):

    pid = os.getpid()
    ps = psutil.Process(pid)
    mem_usage = ps.memory_info()
    #print(mem_usage)

    PER_UNIT = 1024*1024

    logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
    logger.debug('                          Rocon Client Memory Usage                              ', show_caller_info=False)
    logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
    logger.debug('uuid   : {}'.format(uuid), show_caller_info=False)
    logger.debug('pid    : {}'.format(pid), show_caller_info=False)
    logger.debug('rss    : {0:9.2f} (MB)  {1}'.format(mem_usage.rss/PER_UNIT,
                    '"Resident Set Size," this is the non-swapped physical memory a process has used.'), show_caller_info=False)
    logger.debug('vms    : {0:9.2f} (MB)  {1}'.format(mem_usage.vms/PER_UNIT,
                    '"Virtual Memory Size", this is the total amount of virtual memory used by the process.'), show_caller_info=False)
    logger.debug('shared : {0:9.2f} (MB)  {1}'.format(mem_usage.shared/PER_UNIT,
                    'memory that could be potentially shared with other processes'), show_caller_info=False)
    logger.debug('text   : {0:9.2f} (MB)  {1}'.format(mem_usage.text/PER_UNIT,
                    '"Text Resident Set", the amount of memory devoted to executable code.'), show_caller_info=False)
    logger.debug('lib    : {0:9.2f} (MB)  {1}'.format(mem_usage.lib/PER_UNIT,
                    'the memory used by shared libraries'), show_caller_info=False)
    logger.debug('data   : {0:9.2f} (MB)  {1}'.format(mem_usage.data/PER_UNIT,
                    '"Data Resident Set", the amount of physical memory devoted to other than executable code.'), show_caller_info=False)
    logger.debug('dirty  : {0:9.2f} (MB)  {1}'.format(mem_usage.dirty/PER_UNIT,
                    'the number of dirty pages'), show_caller_info=False)
    logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)