import io
import pydash
from aiohttp import web
from PIL import Image
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger


class WebServer():
    def __init__(self, worker_client, port):
        rocon_logger.debug('start web server, port {}'.format(port))
        self._owner_worker_client = worker_client

        self._server = None
        self._runner = None

        self._port = port
        self._host_url = 'localhost'
        self._handler = WebServerRouterHandler(self._owner_worker_client)
        self._now_running = False

        self._routers = [

            web.get('/{uuid}/hello', self._handler.handle_test_hello),

            web.post('/{uuid}/controls/tick', self._handler.handle_start_worker),
            web.delete('/{uuid}/controls/tick', self._handler.handle_stop_worker),
            web.delete('/{uuid}/blackboard', self._handler.handle_reset_worker),
            web.put('/{uuid}/controls/tick', self._handler.handle_set_interval),
            web.get('/{uuid}', self._handler.handle_get_virtual_worker),
            web.get('/{uuid}/options', self._handler.handle_get_options),
            web.get('/{uuid}/blackboard', self._handler.handle_get_blackboard),
            web.get('/{uuid}/location', self._handler.handle_get_location),
            web.get('/{uuid}/controls/messages', self._handler.handle_get_messages),
            web.post('/{uuid}/controls/messages', self._handler.handle_add_messages),

            web.get('/{uuid}/register/wpm', self._handler.handle_register_at_workerpoolmanager),

            web.get('/cmd/ChangedTaskName', self._handler.handle_changed_task_name),

            # For development mode
            web.get('/cmd/EnableShowPathFinding', self._handler.handle_cmd_enable_show_path_finding),
            web.get('/cmd/ShowPathFinding', self._handler.handle_cmd_show_path_finding),
            web.get('/cmd/ClearPathFinding', self._handler.handle_cmd_clear_path_finding),

            web.get('/cmd/relocate', self._handler.handle_cmd_relocate)
        ]

    async def start(self):
        app = web.Application()
        app.add_routes(self._routers)

        try:
            self._runner = web.AppRunner(app)
            await self._runner.setup()

            site = web.TCPSite(self._runner, self._host_url, self._port)

            rocon_logger.debug("======= Serving on http://{}:{}/ ======".format(self._host_url, self._port))
            await site.start()
            self._now_running = True
        except Exception as err:
            rocon_logger.error('Exception occurred', exception=err)
            self._now_running = False

    @property
    def now_running(self):
        return self._now_running

    def show_available_web_command(self):
        rocon_logger.cli_info(" Web Command                              ", show_caller_info=False)

        base_url = 'http://{}:{}'.format(self._host_url, self._port)
        rocon_logger.cli_info(" - Relocate worker's position", show_caller_info=False)
        rocon_logger.cli_info("   {}/cmd/relocate?alias={}".format(base_url, '{alias_location}'), show_caller_info=False)

        if self._owner_worker_client.context.map_manager.feature_enable_show_path is True:
            feature_info = 'feature enabled'
        else:
            feature_info = 'feature disabled'

        rocon_logger.cli_info(" - Enable show path finding({})".format(feature_info), show_caller_info=False)
        rocon_logger.cli_info("   {}/cmd/EnableShowPathFinding?enabled={}".format(base_url, '{boolean}'), show_caller_info=False)

        rocon_logger.cli_info(" - Show path finding({})".format(feature_info), show_caller_info=False)
        rocon_logger.cli_info("   {}/cmd/ShowPathFinding".format(base_url), show_caller_info=False)

        rocon_logger.cli_info(" - Clear path finding({})".format(feature_info), show_caller_info=False)
        rocon_logger.cli_info("   {}/cmd/ClearPathFinding".format(base_url), show_caller_info=False)

        rocon_logger.cli_info(" - Changed task name (Temp. test)", show_caller_info=False)
        rocon_logger.cli_info("   {}/cmd/ChangedTaskName?task_name={}".format(base_url, '{task name}'), show_caller_info=False)

class WebServerRouterHandler():
    def __init__(self, worker_client):
        self._owner_worker_client = worker_client

    async def handle_intro(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        return web.Response(text='Hi there!')

    async def handle_test_hello(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        txt = 'Hello, world'
        return web.Response(text=txt)

    def _check_valid_request(self, request):
        id = request.match_info['uuid']
        if self._owner_worker_client.uuid != id:
            rocon_logger.warning('Not matched uuid (requested uuid = {})'.format(id))
            return False

        return True

    async def handle_get_options(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        response_data = self._owner_worker_client.worker.options
        return web.json_response(response_data)

    async def handle_get_blackboard(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        txt = 'handle_get_blackboard'
        return web.Response(text=txt)

    async def handle_reset_worker(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')


        #TODO reset blackborad
        self._owner_worker_client.reset()

        return web.Response(text='success')

    #TODO JS 구현과 확인 필요 (all)
    async def handle_get_location(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        txt = 'handle_get_location'
        return web.Response(text=txt)

    async def handle_get_messages(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        txt = 'handle_get_messages'
        return web.Response(text=txt)

    async def handle_add_messages(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        data = await request.json()
        '''
        data 는 아래와 같은 dictionary 구조이다. overwrite flag확인하고 key를 제거한다.
        {
            'name' : 'xxx',
            'body' : 'xxx',
            'overwrite' : False
        }
        '''

        overwrite = data['overwrite']
        data.pop('overwrite', None)

        self._owner_worker_client.context.message_manager.push_new_message_data(data, overwrite)

        #리턴값 의미없음.
        return web.json_response({'messages_length': 1})


    async def handle_start_worker(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        data = await request.json()
        interval = data['interval']

        self._owner_worker_client.start(interval)
        return web.Response(text='success')

    async def handle_stop_worker(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        data = await request.json()
        offline = data['offline']
        #TODO set offline

        self._owner_worker_client.stop()
        return web.Response(text='success')

    async def handle_set_interval(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        data = await request.json()
        interval = data['interval']

        self._owner_worker_client.start_tick_timer(interval)
        return web.Response(text='success')

    #TODO 정리
    async def handle_get_virtual_worker(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        response_data = self._owner_worker_client.worker.to_json()
        return web.json_response(response_data)

    async def handle_register_at_workerpoolmanager(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        if self._check_valid_request(request) is False:
            return web.Response(text='Not matched uuid')

        await self._owner_worker_client.register_at_wpm_with_await()

        return web.Response(text='success')

    async def handle_changed_task_name(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))

        task_name = request.query['task_name']

        self._owner_worker_client.changed_task_name(task_name)

        return web.Response(text='success')

    async def handle_cmd_enable_show_path_finding(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        enabled_str = request.query['enabled']

        true_str = ['true']
        false_str = ['false']

        enabled = None
        if enabled_str.lower() in true_str:
            enabled = True
        elif enabled_str.lower() in false_str:
            enabled = False

        if type(enabled) is not bool:
            msg = "'enabled' value is allowed boolean only."
        else:
            msg = 'feature_enable_show_path is set {}'.format(enabled)

            self._owner_worker_client.context.map_manager.feature_enable_show_path = enabled


        return web.Response(text=msg)

    async def handle_cmd_show_path_finding(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        if self._owner_worker_client.context.map_manager.feature_enable_show_path is False:
            msg = 'feature_enable_show_path is False'
            return web.Response(text=msg)

        image = self._owner_worker_client.context.map_manager.get_current_map_image()
        if image is None:
            msg = 'Not found image'
            rocon_logger.debug(msg)
            return web.Response(text=msg)
        else:
            data = self.image_to_byte_array(image)
            return web.Response(body=data, content_type='image/png')

    async def handle_cmd_clear_path_finding(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        if self._owner_worker_client.context.map_manager.feature_enable_show_path is False:
            msg = 'feature_enable_show_path is False'
            return web.Response(text=msg)

        self._owner_worker_client.context.map_manager.clear_current_map_image()

        image = self._owner_worker_client.context.map_manager.get_current_map_image()
        data = self.image_to_byte_array(image)

        return web.Response(body=data, content_type='image/png')

    def image_to_byte_array(self, image:Image):
      imgByteArr = io.BytesIO()
      image.save(imgByteArr, format=image.format)
      imgByteArr = imgByteArr.getvalue()
      return imgByteArr

    async def handle_cmd_relocate(self, request):
        rocon_logger.debug('request url > {}'.format(request.url))
        alias = request.query['alias']

        await self._owner_worker_client._do_relocate_virtual_worker(alias)

        return web.Response(text='success')


