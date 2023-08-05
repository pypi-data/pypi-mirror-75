import pydash
from rocon_client_sdk_py.core_logic.context import Context


class MapInfo():
    def __init__(self):
        self._map_list = None

    async def download_maps(self, context: Context):
        try:
            self._map_list = await context.api_site_configuration.get_maps()

            def cb(m):
                return pydash.get(m, 'site')

            self._map_list = pydash.filter_(self._map_list, cb)
            if len(self._map_list) is 0:
                self.rocon_logger.debug('there are no maps on site configuration')
                self._map_list = None
                return self._map_list


        except Exception as err:
            self.rocon_logger.error('failed to download maps')
            self._map_list = None


        return self._map_list