import pydash
from rocon_client_sdk_py.core_logic.action import Action
from rocon_client_sdk_py.virtual_core.components.actuators import Actuator
from rocon_client_sdk_py.virtual_core.components.autodoor_consumer import AutodoorConsumer
from rocon_client_sdk_py.virtual_core.components.elevator_consumer import ElevatorConsumer
from rocon_client_sdk_py.utils.waiter import Waiter
from rocon_client_sdk_py.virtual_core.report_handler import *
from rocon_client_sdk_py.utils.path_planner import PathPlanner


class UseResource(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Use Resource'
        self.func_name = 'use_resource'
        self._actuator = None

    async def on_define(self):
        self.rocon_logger.debug('define the action of {}'.format(self.name))

        act_def = None
        if self.context.worker.use_worker_config_server:
            # worker configuration에서 pre defined action 확인
            task = self.context.worker.origin_worker_task
            act_def = None
            if task and 'actions' in task:
                act_def = pydash.find(task['actions'], {'func_name': self.func_name})

        else:
            # pre defined action이 없으면 임시로 자체 생성
            if act_def is None:
                api_site_config = self.context.api_site_configuration
                result = await api_site_config.get_resources()

                exclusive_area_list = pydash.get(result, 'ExclusiveArea')
                auto_door_list = pydash.get(result, 'Autodoor')
                teleporter_list = pydash.get(result, 'Teleporter')

                use_resource_list = pydash.concat(exclusive_area_list, auto_door_list, teleporter_list)
                resource_list = []
                def cb(resource):
                    if resource:
                        resource_list.append(
                            {'alias': resource['name'], 'value': resource['id']})

                if use_resource_list:
                    resource_list = pydash.map_(use_resource_list, cb)

                act_def = {
                    'name': self.name,
                    'func_name': self.func_name,
                    'args': [
                        {
                            'key': 'resource_id',
                            'type': 'string',
                            'default': resource_list[0] if len(resource_list) > 0 else None,
                            'domain': resource_list,
                        },
                        {
                            'key': 'resource_type',
                            'type': 'string',
                            'enum': ['ExclusiveArea', 'Autodoor', 'Teleporter'],
                            'default': {'alias': 'ExclusiveArea', 'value': 'ExclusiveArea'},
                            'domain': [
                                {'alias': 'ExclusiveArea', 'value': 'ExclusiveArea'},
                                {'alias': 'Autodoor', 'value': 'Autodoor'},
                                {'alias': 'Elevator', 'value': 'Teleporter'}
                            ]
                        },
                        {
                            'key': 'params',
                            'type': 'object',
                            'default': {},
                            'domain': {}
                        }
                    ]
                }

        return act_def

    def get_arg_value(self, args, key):
        arg = pydash.find(args, {'key': key})
        if arg:
            return arg['value']

        return None

    async def perform_autodoor(self, target_autodoor):
        worker_content = self.context.blackboard.get_worker_content()
        worker_location = pydash.get(worker_content, 'type_specific.location')

        aligns = target_autodoor['aligns']
        if worker_location['map'] != target_autodoor['map']:
            self.rocon_logger.debug('perform_autodoor : does not match worker\'s current map with target resources {}'.format({
                'worker_map': worker_location['map'],
                'resource_map': target_autodoor['map']
            }))

            raise Exception('perform_autodoor : does not match worker\'s current map with target resources')

        if self._actuator is None:
            self._actuator = Actuator()
            await self._actuator.init_path_planner(self.context)

        def cb(point):
            path = self._actuator.path_planner.get_path(target_autodoor['map'], worker_location['pose2d'], point)
            point['distance'] = self._actuator.path_planner.get_distance(path)
            return point

        aligns = pydash.map_(aligns, cb)
        aligns = pydash.sort_by(aligns, 'distance')
        entry_pose = aligns[0]
        exit_pose = aligns[len(aligns) - 1]

        autodoor_consumer = AutodoorConsumer()

        #1. move to entry point
        await self._actuator.moving(self.context, entry_pose)
        #2. request door open
        await autodoor_consumer.request_open_autodoor(self.context, target_autodoor['id'])
        #3. waiting autodoor open
        await autodoor_consumer.ensure_autodoor_opened(self.context, target_autodoor['id'])
        #4. move to exit point
        await self._actuator.moving(self.context, exit_pose)
        #5. close door
        await autodoor_consumer.request_close_autodoor(self.context, target_autodoor['id'])
        await autodoor_consumer.ensure_autodoor_closed(self.context, target_autodoor['id'])

        #6. release autodoor resource
        target_slots = target_autodoor['resource_slots']
        occupied = pydash.find(target_slots, {'user_id': pydash.get(worker_content, 'id'), 'status': 'occupied'})
        await self.context.api_site_configuration.return_resource(worker_content['id'], target_autodoor['id'], occupied['id'])
        return True

    async def perform_teleporter(self, target_teleporter, params):
        worker_content = self.context.blackboard.get_worker_content()
        worker_location = pydash.get(worker_content, 'type_specific.location')

        destination_map_id = params['destination_map_id']
        departure_map_id = params['departure_map_id']

        if worker_location['map'] != departure_map_id:
            self.rocon_logger.debug('cannot process use_resource: Teleporter: departure map{} is not same with worker\'s current map{}'.format(departure_map_id, worker_location['map']))
            return False

        entry_gate = await self.context.api_site_configuration.get_teleporter_gate(target_teleporter['id'], departure_map_id)
        exit_gate = await self.context.api_site_configuration.get_teleporter_gate(target_teleporter['id'], destination_map_id)

        entry_point = pydash.get(entry_gate, 'aligns.entries.0')
        exit_point = pydash.get(exit_gate, 'aligns.exits.0')

        elevator_consumer = ElevatorConsumer()

        #1. waiting elevator arrive
        service_id = await elevator_consumer.call_elevator(self.context, target_teleporter, entry_gate, exit_gate)
        result = await elevator_consumer.ensure_elevator_door_open(self.context, target_teleporter['id'])
        if result is False:
            self.rocon_logger.error('failed to ensure_elevator_door_open before riding elevator')
            return False

        self.rocon_logger.debug('elevator door opened and ready to ride')

        if self._actuator is None:
            self._actuator = Actuator()
            await self._actuator.init_path_planner(self.context)

        #2. move to entry point
        await self._actuator.moving(self.context, entry_point)
        #3. move to center of elevator gate
        await self._actuator.bulldozer_moving(self.context, pydash.pick(entry_gate['area'], ['x', 'y', 'theta']))
        #4. close door
        try:
            result = await elevator_consumer.close_elevator_door(self.context, target_teleporter['id'], service_id, 'board', 'success')
            if result is False:
                self.rocon_logger.debug('failed to closeElevatorDoor after ride elevator')
                return False
        except Exception as err:
            self.rocon_logger.error('exception occurred', exception=err)
            #raise Exception(err)
            return False

        result = await elevator_consumer.ensure_elevator_door_closed(self.context, target_teleporter['id'])
        #TODO result가 false로 넘어오는것 확인
        if result is False:
            self.rocon_logger.error('failed to ensureElevatorDoorClosed after riding elevator')
            self.rocon_logger.error('check iot operator. pass this error on virtual.')

        self.rocon_logger.debug('elevator door closed after ride elevator')

        #5. ensure elevator door open before unboard elevator
        result = await elevator_consumer.ensure_elevator_door_open(self.context, target_teleporter['id'])
        if result is False:
            return False

        self.rocon_logger.debug('elevator door opened and ready to ride')

        #6. change map to destination map (initial location is exit of destination gate)
        self.rocon_logger.debug('request change position with map')
        await self._actuator.change_position(self.context, pydash.pick(exit_gate['area'], ['x', 'y', 'theta']), exit_gate['map'])
        #7. move exit point
        await self._actuator.bulldozer_moving(self.context, exit_point, backward_progress=True)
        #8. close door
        if await elevator_consumer.close_elevator_door(self.context, target_teleporter['id'], service_id, 'unboard', 'success') is False:
            self.rocon_logger.debug('failed to closeElevatorDoor after unboard elevator')
            return False

        self.rocon_logger.debug('elevator door closed after unboard elevator')

        target_slots = target_teleporter['resource_slots']
        occupied = pydash.find(target_slots, {'user_id': pydash.get(worker_content, 'id'), 'status': 'occupied'})
        await self.context.api_site_configuration.return_resource(pydash.get(worker_content, 'id'), target_teleporter['id'], occupied['id'])
        self.rocon_logger.debug('resource returned')
        return True

    async def perform_narrow_corridor(self, target_resource):
        worker_content = self.context.blackboard.get_worker_content()
        worker_location = pydash.get(worker_content, 'type_specific.location')

        # In case of using narrow corridor
        # 1. get align info from scheduler
        if worker_location['map'] != target_resource['map']:
            self.rocon_logger.debug('perform_narrow_corridor: does not mathc worker\'s current map with target resources', {
                'worker_map': worker_location['map'],
                'resource_map': target_resource['map']
            })

            raise Exception('perform_narrow_corridor: does not match worker\'s current map with target resources worker_map:{}, resource_map: {}'.format(worker_location['map'], target_resource['map']))

        if self._actuator is None:
            self._actuator = Actuator()
            await self._actuator.init_path_planner(self.context)


        report = self.context.blackboard.get_report()
        get_enter_exit_properties = get_enter_exit_aligns(report, target_resource)

        # 2. move to nearest align point
        await self._actuator.moving(self.context, get_enter_exit_properties['enter'])
        # 3. move to farther align point
        await self._actuator.moving(self.context, get_enter_exit_properties['exit'])
        # 4. return occupied resource slot
        MAX_RETRY = 100
        REQUEST_INTERVAL = 100
        worker_id = worker_content['id']
        waiter = Waiter('action_use_resource : perform_narrow_corridor', self.context.event_loop, REQUEST_INTERVAL)

        for i in range(MAX_RETRY):
            self.rocon_logger.debug('return occupied resource {}/{}'.format(i+1, MAX_RETRY))
            target_slots = target_resource['resource_slots']
            occupied = pydash.find(target_slots, {'user_id': worker_id, 'status': 'occupied'})

            try:
                await self.context.api_site_configuration.return_resource(worker_id, target_resource['id'], occupied['id'])
                return True
            except Exception as err:
                self.rocon_logger.debug('failed to return resource with error')

            await waiter.wait()

        self.rocon_logger.debug('exceed maximum try to return occupied resource')
        return False

    async def on_perform(self, args):
        resource_id = self.get_arg_value(args, 'resource_id')
        resource_type = self.get_arg_value(args, 'resource_type')
        target_resource = await self.context.api_site_configuration.get_resource(resource_id)

        if resource_type == 'ExclusiveArea':
            return await self.perform_narrow_corridor(target_resource)
        elif resource_type == 'Autodoor':
            return await self.perform_autodoor(target_resource)
        elif resource_type == 'Teleporter':
            instruction_param = self.get_arg_value(args, 'params')
            return await self.perform_teleporter(target_resource, instruction_param)
        else:
            self.rocon_logger.debug('unhandled resource type: {}'.format(resource_type))
            return False
