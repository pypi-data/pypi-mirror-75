import asyncio
import threading
import paho.mqtt.client as mqtt
import os, psutil
import abc
import time
import pydash
from rocon_client_sdk_py.server.web_server import WebServer
from rocon_client_sdk_py.worker import Worker
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.const import *
from rocon_client_sdk_py.info import info
from rocon_client_sdk_py.utils.util import *


class WorkerClient():
    def __init__(self, run_multi_client=False, multi_client_options=None):
        self._rocon_logger = rocon_logger
        self._rocon_logger.debug('\n', show_caller_info=False)
        self._rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        self._rocon_logger.debug('       Start Rocon Client (Hello!)       ', show_caller_info=False)
        self._rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        self._rocon_logger.debug('\n', show_caller_info=False)
        self._rocon_logger.debug('initializing Rocon Client')

        self._init_event_loop()

        self._mqtt_client = None
        self._worker = self.on_create(self._event_loop, run_multi_client=run_multi_client, multi_client_options=multi_client_options)
        if self._worker is None:
            return

        self._worker._multi_client_options = multi_client_options
        self._worker.set_after_tick_callback(self._callback_after_tick)

        # start web server
        self._server_port = self._worker._client_configs['configs']['server']['port']
        self._web_server = WebServer(self, self._server_port)

        self._server_enabled = self._worker._client_configs['configs']['server']['enabled']

        # interaction with worker pool
        self._worker_pool_registered = False
        self._worker_pool_enabled_register = self._worker._client_configs['configs']['workerPool']['enabled_register']
        self._worker_pool_enabled_mqtt_publishing = self._worker._client_configs['configs']['workerPool']['enabled_mqtt_publishing']


        if self._server_enabled is True:
            future = asyncio.run_coroutine_threadsafe(self._web_server.start(), self._event_loop)
            result = future.result()

            # register into WorkerPool
            if self._worker_pool_enabled_register is True:
                self.register_at_wpm()

        self._rocon_logger.debug('initialized Rocon Client')
        self._worker.start_tick_timer(DEFAULT_TICK_INTERVAL_MS)


        if self._worker._multi_client_options:
            alias_location = self._worker._multi_client_options['start_location_alias']
            result = self.relocate_virtual_worker(alias_location)


    @property
    def rocon_logger(self):
        return self._rocon_logger


    def _init_event_loop(self):
        self._event_thread = None
        self._event_loop = asyncio.get_event_loop()
        #self._event_loop.set_debug(True)

        def run_it_forever(loop):
            self.rocon_logger.debug('run event loop forever')
            asyncio.set_event_loop(loop)
            loop.run_forever()
            self._rocon_logger.debug('stopped event loop')

        self._event_thread = threading.Thread(target=run_it_forever, args=(self._event_loop,), daemon=True)
        self._event_thread.start()

    @property
    def worker(self):
        """Worker 객체
        :return: 생성된 Worker 객체 리턴
        """
        return self._worker

    @property
    def uuid(self):
        """Worker의 고유한 uuid
        :return: uuid 값 리턴
        """
        return self._worker.uuid

    @property
    def context(self):
        return self._worker.context

    def run(self):

        cli_info = "[Rocon Client CLI] Enter 'q' to quilt, 'h' to help\n>"
        input_cmd = ''
        while input_cmd.lower() != 'q':

            try:
                input_cmd = input(cli_info)

                cmd_str = input_cmd.lower()
                cmd_args = cmd_str.split(' ')
                cmd = cmd_args[0]
                if cmd == 'h':
                    self._rocon_logger.cli_info("\n", show_caller_info=False)
                    self._rocon_logger.cli_info("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", show_caller_info=False)
                    self._rocon_logger.cli_info("               Rocon Client CLI(Command line interface) Help                     ", show_caller_info=False)
                    self._rocon_logger.cli_info("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", show_caller_info=False)
                    self._rocon_logger.cli_info("  'q' : Quit                                     ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'r' : Start tick-loop                          ", show_caller_info=False)
                    self._rocon_logger.cli_info("  's' : Stop tick-loop                           ", show_caller_info=False)
                    self._rocon_logger.cli_info("  't' : Start just one tick                      ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'i' : Show information                         ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'm' : Show Memory Usage                        ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'w' : Show available web command list          ", show_caller_info=False)
                    self._rocon_logger.cli_info("                                                 ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'sb' : Show log of behavior-tree's logic       ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'hb' : Hide log of behavior-tree's logic       ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'ch' : Show custom user defined help           ", show_caller_info=False)
                    self._rocon_logger.cli_info("                                                 ", show_caller_info=False)
                    self._rocon_logger.cli_info("  - Command for Virtual Robot                    ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'relocate {alias}' : Relocate worker's position", show_caller_info=False)
                    self._rocon_logger.cli_info("      ex) relocate 3F_Infodesk                   ", show_caller_info=False)
                    self._rocon_logger.cli_info("  'button {'O'|'X'|'E_PLUS'}' : push button(human input)", show_caller_info=False)
                    self._rocon_logger.cli_info("      ex) button O                               ", show_caller_info=False)

                    self._rocon_logger.cli_info("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", show_caller_info=False)
                    self._rocon_logger.cli_info("\n", show_caller_info=False)

                elif cmd == 't':
                    self._worker.tick()
                elif cmd == 'r':
                    self._worker.start_tick_timer(DEFAULT_TICK_INTERVAL_MS)
                elif cmd == 's':
                    self._worker.stop_tick_timer()
                elif cmd == 'i':
                    self._show_info()
                elif cmd == 'm':
                    show_memory_usage(self._rocon_logger, uuid=self.uuid)
                elif cmd == 'w':
                    self._web_server.show_available_web_command()
                elif cmd == 'sb':
                    self._rocon_logger.enable_logging_by_moduel_keyword(BT_KEYWORD)
                elif cmd == 'hb':
                    self._rocon_logger.disable_logging_by_moduel_keyword(BT_KEYWORD)
                elif cmd == 'relocate':
                    result = False
                    alias_location = ''
                    if len(cmd_args) > 1:
                        alias_location = ' '.join(cmd_args[1:])
                        result = self.relocate_virtual_worker(alias_location)

                    if result is False:
                        self._rocon_logger.cli_info("Not found the location ('{}')".format(alias_location), show_caller_info=False)
                elif cmd == 'button':
                    result = False
                    if len(cmd_args) > 1:
                        button_type = ' '.join(cmd_args[1])
                        result = self.button_push(button_type)

                elif cmd == 'ch':
                    self.on_custom_command_line(cmd)
                else:
                    #그외의 명령은 사용자 정의로 간주하고 이벤트 발생시킨다.
                    self.on_custom_command_line(cmd, cmd_args=cmd_args)

            except KeyboardInterrupt:
                self._rocon_logger.cli_info("\nResuming... ")
                continue

            #time.sleep(0.5)

        self.on_destroy()

    def on_create(self, run_multi_client=False, multi_client_options=None) -> Worker:
        self._rocon_logger.debug()

        return None

    def on_destroy(self):
        self._rocon_logger.debug('destroying Rocon Client')

        self.stop()

        self._event_loop.stop()
        if self._event_thread:
            self._event_thread.join(30)

        self._rocon_logger.debug('event loop is closed? : {}'.format(str(self._event_loop.is_closed())))
        self._rocon_logger.debug('event loop is running? : {}'.format(str(self._event_loop.is_running())))
        self._rocon_logger.debug('event_thread alive? : {}'.format(str(self._event_thread.is_alive())))

        self._rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)
        self._rocon_logger.debug('     Shutdown Rocon Client (Bye!)     ', show_caller_info=False)
        self._rocon_logger.debug('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=', show_caller_info=False)

    @abc.abstractmethod
    def on_changed_task_name(self, task_name):
        raise NotImplementedError(
            "Please Implement this method...'\n")

    def register_at_wpm(self):

        api_pool = self._worker.context.api_worker_pool
        #TODO need to change the name of 'Agent'
        reg_data = {
            'uuid': self._worker.uuid,
            'hostWorkerClient': 'localhost',
            'portWorkerClient': self._server_port
        }


        self._worker_pool_registered = False
        
        future = asyncio.run_coroutine_threadsafe(api_pool.register_worker(self._worker.uuid, reg_data), self._event_loop)
        result = future.result()

        if result is None:
            self._rocon_logger.error('{} registration failed in WorkerPool'.format(self._worker.uuid))
        else:
            self._worker_pool_registered = True
            self._rocon_logger.debug('{} registration succeeded in WorkerPool'.format(self._worker.uuid))

    async def register_at_wpm_with_await(self):

        api_pool = self._worker.context.api_worker_pool
        # TODO need to change the name of 'Agent'
        reg_data = {
            'uuid': self._worker.uuid,
            'hostWorkerClient': 'localhost',
            'portWorkerClient': self._server_port
        }

        result = await api_pool.register_worker(self._worker.uuid, reg_data)
        if result is None:
            self._rocon_logger.error('{} registration failed in WorkerPool'.format(self._worker.uuid))
        else:
            self._worker_pool_registered = True
            self._rocon_logger.debug('{} registration succeeded in WorkerPool'.format(self._worker.uuid))


    def mqtt_on_connect(self, client, userdata, flags, rc):
        if self._worker_pool_enabled_mqtt_publishing and self._worker_pool_registered:
            try:
                self._rocon_logger.debug('connected with result code {}'.format(str(rc)))
                client.subscribe('tree/')  #
            except Exception as err:
                self._rocon_logger.error('mqtt control error : {}'.format(err))

    def mqtt_on_message(self, client, userdata, msg):
        if self._worker_pool_enabled_mqtt_publishing and self._worker_pool_registered:
            self._rocon_logger.debug('{} {}'.format(msg.topic, str(msg.payload)))


    def mqtt_publish(self, payload):
        if self._worker_pool_enabled_mqtt_publishing and self._worker_pool_registered:
            try:
                if self._mqtt_client == None:
                    self.start_mqtt()

                self._mqtt_client.publish('tree/{}'.format(self._worker.uuid), payload)
            except Exception as err:
                self._rocon_logger.error('mqtt control error : {}'.format(err))


    def start_mqtt(self):
        # mqtt subscribe
        if self._mqtt_client is None:
            self.close_mqtt()

        self._mqtt_client = mqtt.Client()
        self._mqtt_client.on_connect = self.mqtt_on_connect
        self._mqtt_client.on_message = self.mqtt_on_message

        self._mqtt_client.connect('localhost', port=10997)
        self._mqtt_client.loop_start()

    def close_mqtt(self):
        if self._mqtt_client:
            self._mqtt_client.loop_stop()
            self._mqtt_client.disconnect()
            self._mqtt_client = None

        self._rocon_logger.debug('closed mqtt')

    def restart(self):
        self.stop()
        self._worker.reset()

    def start(self, interval_msec = DEFAULT_TICK_INTERVAL_MS):
        self._worker.start(interval_msec)
        self.start_mqtt()

    def stop(self, offline = False):
        self._worker.stop(offline)
        self.close_mqtt()

    def start_tick_timer(self, interval):
        self._worker.start_tick_timer(interval)

    def _callback_after_tick(self, context):
        if self._worker_pool_enabled_mqtt_publishing and self._worker_pool_registered:
            publishing_data = context.get_trees_stringify()
            self.mqtt_publish(publishing_data)

    def _show_info(self):
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('                         Rocon Client Information                                ')
        print('                                                                                 ')
        print('                                                                  SDK ver : {}   '.format(info.version))
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print(' UUID                : {}'.format(self._worker.uuid))
        print(' Hosts')
        print('  + Scheduler        : {}'.format(self._worker.context.api_report.hostname))
        print('  + SiteConfig.      : {}'.format(self._worker.context.api_site_configuration.hostname))
        print('  + WorkerPool       : {}'.format(self._worker.context.api_worker_pool.hostname))
        print('    + enabled_register         : {}'.format(self._worker_pool_enabled_register))
        print('    + enabled_mqtt_publishing  : {}'.format(self._worker_pool_enabled_mqtt_publishing))
        print('    + registered               : {}'.format(self._worker_pool_registered))
        print('')
        print(' Server')
        print('  + port             : {}'.format(self._server_port))
        print('  + enabled          : {}'.format(self._server_enabled))
        print('  + now running      : {}'.format(self._web_server.now_running))
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    def relocate_virtual_worker(self, alias_location_name):

        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_relocate_virtual_worker(alias_location_name), self.context.event_loop)
            result = coro_future.result()

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            result = False

        return result

    def button_push(self, button_type):
        try:
            coro_future = asyncio.run_coroutine_threadsafe(self._do_button_push(button_type), self.context.event_loop)
            result = coro_future.result()
        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            result = False

        return result

    async def _do_relocate_virtual_worker(self, alias_location_name):

        location = await self.context.api_site_configuration.get_location(alias_location_name)

        if location:
            loc_info = {'pose2d': location['pose'], 'semantic_location': location['id'], 'map': location['map']}
            msg_data = {'name':'resetLocation',
                        'body':loc_info}

            self.context.message_manager.push_new_message_data(msg_data)
            return True

        return False

    def _do_button_push(self, button_type):

        msg_data = {
            'name' : 'virtualButtons',
            'body': button_type
        }
        self.context.message_manager.push_new_message_data(msg_data)

        return True

    def changed_task_name(self, task_name):
        '''
        외부로 부터 task name의 변경을 통보 받을때 호출된다.
        현재 web_server의 handle_changed_task_name 에 의해 호출됨.

        변경 사항은 client에 통보해 로컬 config 파일을 업데이트한다.
        '''
        self.on_changed_task_name(task_name)

        #내부 엔진상의 업데이트는 작업이 끝난 idle상태에서 업데이트 한다.

        #self._worker.update_task_name(task_name)

        self.context.blackboard.set('task_name_changed', task_name)


    def on_custom_command_line(self, cmd, cmd_args=None):
        '''
        CLI로 입력된 명령 중 코어에서 처리하지 않는 명령들은 on_custom_command_line 이벤트로 pass된다.
        사용자 정의형 cli를 테스트할 경우 사용한다.
        :param cmd_args:
        :return:
        '''
        pass