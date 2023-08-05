import io
import json
from .api import Api


class ApiConfiguration(Api):

    @property
    def request(self):
        return self._httpclient.request()

    @property
    def hostname(self):
        return self._httpclient.hostname_config

    def get_url(self, sub_url):
        url = self._httpclient.config_url(sub_url)
        return url

    async def get_stations(self, station_id=''):
        request = self._httpclient.request()

        sub_id = '/' + station_id if station_id != '' else ''
        url = self._httpclient.config_url('/api/stations{}'.format(sub_id))
        self.rocon_logger.debug('request.get > {}'.format(url))

        json_data = None
        try:
            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data

    async def get_locations(self, destination_id=''):
        request = self._httpclient.request()

        if len(destination_id) > 0:
            url = self._httpclient.config_url('/api/locations/{}'.format(destination_id))
        else:
            url = self._httpclient.config_url('/api/locations')

        self.rocon_logger.debug('request.get > {}'.format(url))

        json_data = None
        try:
            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    #self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data

    async def get_resource(self, resource_id):
        request = self._httpclient.request()

        url = self._httpclient.config_url('/api/resources/{}'.format(resource_id))
        self.rocon_logger.debug('request.get > {}'.format(url))

        json_data = None
        try:
            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data

    async def get_resources(self):
        request = self._httpclient.request()

        url = self._httpclient.config_url('/api/resources')
        self.rocon_logger.debug('request.get > {}'.format(url))

        json_data = None
        try:
            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data

    async def get_maps(self, map=''):
        request = self._httpclient.request()
        map_sub = '/' + map if len(map) > 0 else ''
        url = self._httpclient.config_url('/api/maps{}'.format(map_sub))
        self.rocon_logger.debug('request.get > {}'.format(url))

        json_data = None
        try:
            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data

    async def get_map_monochrome_image(self, path):
        request = self._httpclient.request()
        url = self._httpclient.config_url(path)
        self.rocon_logger.debug('request.get > {}'.format(url))

        rtn_data = None
        try:

            async with request.get(url) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    data = await r.read()
                    rtn_data = io.BytesIO(data)
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

            if rtn_data is None:
                self.rocon_logger.error('image is none')

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)
            exc.with_traceback()

        return rtn_data


    async def get_zones(self, zone_type, map_id):
        query = {'map':map_id, 'type':zone_type}
        request = self._httpclient.request()
        url = self._httpclient.config_url('/api/zones')
        self.rocon_logger.debug('request.get > {}'.format(url))

        json_data = None
        try:
            async with request.get(url, params=query) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data

    async def return_resource(self, worker_id, resource_id, slot_id = None):
        request = self._httpclient.request()
        url = self._httpclient.config_url('/api/resources/{}/slots/{}'.format(resource_id, slot_id))
        req_json_body = json.dumps({'status': 'gone'})

        json_data = None
        try:
            async with request.put(url, data=req_json_body) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)

        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return json_data


    async def get_teleporter_gate(self, teleporter_id, map_id):
        request = self._httpclient.request()
        url = self._httpclient.config_url('/api/teleporter-gates')
        query = {
            'teleporter': teleporter_id,
            'map': map_id,
            'populate':'resource_slots'
        }

        self.rocon_logger.debug('request.get > {}'.format(url))

        rtn_data = None
        try:
            async with request.get(url, params=query) as r:
                self.rocon_logger.debug('response status > {}'.format(r.status))
                if r.status is 200:
                    json_data = await r.json()
                    self.rocon_logger.debug('response data > \n{}'.format(json_data))
                    rtn_data = json_data[0]
                else:
                    self.rocon_logger.error('Error status occurred : {}'.format(r))
                    self.error_handling(r)


        except Exception as exc:
            self.rocon_logger.error('Exception occurred', exception=exc)

        return rtn_data