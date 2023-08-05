import aiohttp
from .api_worker import ApiWorker
from .api_report import ApiReport
from .api_task import ApiTask
from .api_site_configuration import ApiSiteConfiguration
from .api_worker_pool import ApiWorkerPool
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger


class HttpClient():
    def __init__(self, hostname_concert='localhost:10602', hostname_site_config='localhost:10605', hostname_worker_pool='localhost:10999'):
        self._hostname_concert = hostname_concert
        self._hostname_site_config = hostname_site_config
        self._hostname_worker_pool = hostname_worker_pool

        # http client instance 생성
        # TODO instance 생성 및 request/response interceptor 처리 루틴 방안 검토 필요
        self._headers = {'Content-type': 'application/json'}

        self._verify_ssl = False
        self._enable_clear_closed = False
        self._force_close = False
        self._request = aiohttp.ClientSession(headers=self._headers,
                  connector=aiohttp.TCPConnector(verify_ssl=self._verify_ssl,
                                                 enable_cleanup_closed=self._enable_clear_closed,
                                                 force_close=self._force_close))


        # api 속성 설정
        self.api_worker = ApiWorker(self)
        self.api_report = ApiReport(self)
        self.api_task = ApiTask(self)
        self.api_site_config = ApiSiteConfiguration(self)
        self.api_worker_pool = ApiWorkerPool(self)

        self._logger = rocon_logger

    def ensure_path(self, path):
        if path[0] != '/':
            return '/{}'.format(path)

        return path

    def gateway_url(self, path):
        return 'http://{}{}'.format(self._hostname_concert, self.ensure_path(path))

    def scheduler_url(self, path):
        return 'http://{}/scheduler/v0{}'.format(self._hostname_concert, self.ensure_path(path))

    def site_config_url(self, path):
        return 'http://{}{}'.format(self._hostname_site_config, self.ensure_path(path))

    def worker_pool_url(self, path):
        return 'http://{}{}'.format(self._hostname_worker_pool, self.ensure_path(path))

    def request(self):
        if self._request.closed:
            self._request = aiohttp.ClientSession(headers=self._headers,
                      connector=aiohttp.TCPConnector(verify_ssl=self._verify_ssl,
                                                     enable_cleanup_closed=self._enable_clear_closed,
                                                     force_close=self._force_close))

        return self._request

    def logger(self):
        return self._logger

    @property
    def hostname_concert(self):
        return self._hostname_concert

    @property
    def hostname_site_config(self):
        return self._hostname_site_config

    @property
    def hostname_worker_pool(self):
        return self._hostname_worker_pool