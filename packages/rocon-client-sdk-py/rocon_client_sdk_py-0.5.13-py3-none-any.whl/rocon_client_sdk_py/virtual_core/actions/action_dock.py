import asyncio
import pydash
from rocon_client_sdk_py.core_logic.action import Action
from rocon_client_sdk_py.utils.path_planner import PathPlanner


class Dock(Action):
    def __init__(self):
        super().__init__()
        self.name = 'Dock'
        self.func_name = 'dock'

    async def on_define(self):
        self.rocon_logger.debug('define the action of {}'.format(self.name))

        act_def = None
        if self.context.worker.use_worker_config_server:
            #worker configuration에서 pre defined action 확인
            task = self.context.worker.origin_worker_task
            act_def = None
            if task and 'actions' in task:
                act_def = pydash.find(task['actions'], {'func_name':self.func_name})

        else:
            #pre defined action이 없으면 임시로 자체 생성
            if act_def is None:
                api_site_config = self.context.api_site_configuration
                result = await api_site_config.get_stations()

                domain_station = []
                def cb(station):
                    domain_station.append({'alias': station['name']+'('+str(station['marker_value'])+')', 'value': station['id']})
                pydash.map_(result, cb)

                act_def = {
                    'name': self.name,
                    'func_name': self.func_name,
                    'args': [
                        {
                            'key': 'station',
                            'type': 'number',
                            'default': domain_station[len(domain_station) -1],
                            'domain': domain_station
                        }
                    ]
                }

        return act_def

    async def on_perform(self, args):
        station_id = pydash.find(args, {'key': 'station'})['value']
        station = await self.context.api_site_configuration.get_stations(station_id)

        if station is None:
            self.rocon_logger.debug('failed to get station')

        worker_content = self.context.blackboard.get_worker_content()
        worker_location = pydash.get(worker_content, 'type_specific.location')
        path_planner = PathPlanner(self.context)

        path = path_planner.get_path(worker_location['map'], worker_location['pose2d'], station['pose'])
        trajectory = path_planner.path_to_trajectory(worker_location['pose2d'], path)

        self.rocon_logger.debug('start to moving robot on path')

        for point in trajectory:
            worker_content = self.context.blackboard.get_worker_content()
            updated_type_specific = worker_content['type_specific']
            if 'theta' in point:
                pass
            else:
                point['theta'] = pydash.get(worker_content, 'type_specific.location.pose2d.theta')

            updated_type_specific['location'] = pydash.assign({}, updated_type_specific['location'], {
                'map': worker_location['map'],
                'pose2d': point
            })

            self.context.blackboard.set_worker_content({'type_specific': updated_type_specific})
            await self.context.blackboard.sync_worker()
            await asyncio.sleep(1)

        updated_type_specific['location']['pose2d']['theta'] = station['pose']['theta']
        self.context.blackboard.set_worker_content({'type_specific': updated_type_specific})
        await self.context.blackboard.sync_worker()
        await asyncio.sleep(1)
        return True
