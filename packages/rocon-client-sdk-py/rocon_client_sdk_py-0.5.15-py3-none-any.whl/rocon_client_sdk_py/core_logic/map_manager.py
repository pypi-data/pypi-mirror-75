import pydash
import asyncio
from PIL import Image
import os
import json
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger


class MapManager():
    def __init__(self, api_site_configuration, event_loop, working_root):

        self._api_site_configuration = api_site_configuration
        self._map_path_names = {}
        self._prohibit_zones = {}
        self._map_list = None

        self._feature_enable_show_path = False
        self._current_map_image = None
        self._current_map_name = None

        self._working_dir = working_root

        try:
            feature = asyncio.run_coroutine_threadsafe(self.download_maps(), event_loop)
            self._map_list = feature.result()
        except Exception as err:
            rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()

        rocon_logger.debug('downloaded maps successfully')

    async def download_maps(self):
        try:
            self._map_list = await self._api_site_configuration.get_maps()

            def cb(m):
                return pydash.get(m, 'site')

            self._map_list = pydash.filter_(self._map_list, cb)
            if len(self._map_list) is 0:
                rocon_logger.debug('there are no maps on site configuration')
                self._map_list = None
                return self._map_list

            self._map_path_names = {}
            path = '{}/assets/maps/'.format(self._working_dir)

            for map in self._map_list:
                map_id = map['id']
                map_image = await self.get_map_monochrome_image_from_configuration(map)


                if not os.path.exists(path):
                    os.makedirs(path)

                # to save image
                image_file_name = '{}{}.bmp'.format(path, map_id)
                map_image.save(image_file_name)

                json_file_name = '{}{}.json'.format(path, map_id)
                with open(json_file_name, 'w') as outfile:
                    json.dump(map, outfile)

                self._map_path_names[map_id] = image_file_name
                self._prohibit_zones[map_id] = await self._api_site_configuration.get_zones('prohibit', map_id)
                map_image.close()

        except Exception as err:
            rocon_logger.error('failed to download maps', exception=err)
            self._map_list = None

        return self._map_list

    def get_map_info_list(self):
        return self._map_list

    def get_map_info(self, map_id):
        map_info = pydash.find(self._map_list, {'id': map_id})
        return map_info

    def load_map_image(self, map_id) -> Image:

        if map_id not in self._map_path_names:
            rocon_logger.debug('not found map image for map id as {}'.format(map_id))
            return None

        image = Image.open(self._map_path_names[map_id])

        return image

    #get_map_image_by_name
    def load_map_image_by_name(self, name) -> Image:

        for map in self._map_list:
            if map['name'] == name:
                map_id = map['id']
                return self.load_map_image(map_id)

        return None

    def get_current_map_image_by_name(self, name)-> Image:
        if self._feature_enable_show_path is False:
            return None

        if self._current_map_name is None or self._current_map_name != name:
            if self._current_map_image is not None:
                self._current_map_image.close()

            self._current_map_name = name
            self._current_map_image = self.load_map_image_by_name(name)

        return self._current_map_image

    def get_current_map_image(self):
        return self._current_map_image

    def clear_current_map_image(self):
        if self._current_map_image is not None:
            self._current_map_image.close()

        self._current_map_image = self.load_map_image_by_name(self._current_map_name)

    @property
    def feature_enable_show_path(self):
        return self._feature_enable_show_path

    @feature_enable_show_path.setter
    def feature_enable_show_path(self, enabled:bool):
        self._feature_enable_show_path = enabled
        if enabled is False:
            if self._current_map_image is not None:
                self._current_map_image.close()
                self._current_map_image = None

    def clear_map_path_image_by_name(self, name):

        #TODO 재구성 필요
        pass
        '''
        org_image = self.get_map_image_by_name(name)
        if org_image:
            path_image = self.get_map_path_image_by_name(name)

            path_image.paste(org_image)
        '''

    #def get_map_images(self):
    #    return self._grid_map_images

    def get_prohibit_zones(self, map_id):
        if map_id not in self._prohibit_zones:
            rocon_logger.debug('not found prohibit zone for map id as {}'.format(map_id))
            return None

        return self._prohibit_zones[map_id]

    def get_prohibit_zones_list(self):
        return self._prohibit_zones

    async def get_map_monochrome_image_from_configuration(self, map)-> Image:

        grid_map_image = None

        try:
            monochrome_image = await self._api_site_configuration.get_map_monochrome_image('/public/' + pydash.get(map, 'files.monochrome'))
            if monochrome_image:
                grid_map_image = image = Image.open(monochrome_image)

            #grid_map_image.show()

        except Exception as err:
            rocon_logger.error('Exception occurred', exception=err)
            err.with_traceback()
            return None

        return grid_map_image

    def get_map_names(self):
        names = pydash.map_(self._map_list, lambda map: map['name'])

        return names

    async def get_locations(self):
        return await self._api_site_configuration.get_locations()