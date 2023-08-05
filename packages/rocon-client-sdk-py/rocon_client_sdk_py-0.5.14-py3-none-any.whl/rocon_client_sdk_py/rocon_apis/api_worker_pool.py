from .api import Api


class ApiWorkerPool(Api):

    @property
    def hostname(self):
        return self._httpclient.hostname_worker_pool

    async def register_worker(self, worker_id, reg_data):
        request = self._httpclient.request()
        url = self._httpclient.worker_pool_url('/api/workers/{}/register/'.format(worker_id))
        self.rocon_logger.debug('request.post > {}'.format(url))

        json_data = None
        try:
            async with request.post(url, json=reg_data) as r:

                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Error occurred : {}'.format(exc), exception=exc)

        return json_data