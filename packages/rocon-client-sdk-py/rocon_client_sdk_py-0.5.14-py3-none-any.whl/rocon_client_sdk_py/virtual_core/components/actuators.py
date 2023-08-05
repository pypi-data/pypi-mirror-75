import asyncio
import pydash
from PIL import ImageDraw
from rocon_client_sdk_py.utils.path_planner import PathPlanner
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.utils.util import *


UPDATE_SLEEP_INTERVAL = 700

class Actuator(metaclass=SingletonMetaClass):
    def __init__(self):
        self.rocon_logger = rocon_logger
        self.path_planner = None

    def __del__(self):
        self.rocon_logger = None
        self.path_planner = None

    async def change_position(self, context, destination_pose, destination_map=None):
        worker_content = context.blackboard.get_worker_content()
        worker_location = pydash.get(worker_content, 'type_specific.location')

        updated_type_specific = worker_content['type_specific']
        if 'theta' in destination_pose is None:
            destination_pose['theta'] = pydash(worker_content, 'type_specific.location.pose2d.theta')

        update = {
                'map': destination_map or worker_location['map'],
                'pose2d': destination_pose or worker_location['pose2d'],
                'semantic_location': None
            }

        if 'location' in updated_type_specific:
            updated_type_specific['location'] = pydash.assign({}, updated_type_specific['location'], update)
        else:
            updated_type_specific['location'] = pydash.assign({}, update)


        context.blackboard.set_worker_content({'type_specific':updated_type_specific})
        await context.blackboard.sync_worker()
        self.rocon_logger.debug('position changed')
        return True

    async def init_path_planner(self, context):
        self.path_planner = PathPlanner(context)

    async def moving(self, context, destination_pose, semantic_location_id=None):

        try:
            worker_content = context.blackboard.get_worker_content()
            worker_location = pydash.get(worker_content, 'type_specific.location')

            path = self.path_planner.get_path(worker_location['map'], worker_location['pose2d'], destination_pose)

            # draw original path on the path map image
            map_id = worker_location['map']
            map = self.path_planner.get_map_by_id(map_id)

            # path finding 경로 그리기
            if context.map_manager.feature_enable_show_path is True:
                image = context.map_manager.get_current_map_image_by_name(map['name'])
                def cb(pose):
                    mono_p = self.path_planner.pose_to_mono(map, pose)
                    return (
                        mono_p['x'], mono_p['y']
                    )

                mono_path = pydash.map_(path, cb)
                self.draw_path_on_path_map(image, mono_path, color_path='green', radius=1)


            trajectory = self.path_planner.path_to_trajectory(worker_location['pose2d'], path)
            '''
            #마지막 위치 추가 - get_path의 dest위치가 트러짐 보정.
            if len(path) > 0:
                last_theta = pydash.get(trajectory[-1], 'theta')
                last = copy.copy(destination_pose)
                pydash.assign(last, {'theta': last_theta})
                trajectory.append(last)
            '''
            del path
            del map

            self.rocon_logger.debug('start to moving robot on path')

            disable_moving_simulation = pydash.get(context.worker.multi_client_options, 'disable_moving_simulation')
            if disable_moving_simulation:
                if len(trajectory) > 2:
                    new_trajectory = []
                    new_trajectory.append(trajectory[0])
                    new_trajectory.append(trajectory[len(trajectory)-1])

                    trajectory = new_trajectory


            for idx, point in enumerate(trajectory):
                worker_content = context.blackboard.get_worker_content()
                if 'error' in worker_content:
                    self.rocon_logger.error('worker_content is something wrong : {}'.format(worker_content))

                updated_type_specific = pydash.get(worker_content, 'type_specific')
                if updated_type_specific:
                    if 'theta' in point and point['theta'] != None:
                        pass
                    else:
                        point['theta'] = pydash.get(worker_content, 'type_specific.location.pose2d.theta')

                    updated_type_specific['location'] = pydash.assign({}, updated_type_specific['location'], {
                        'map': worker_location['map'],
                        'pose2d': point,
                        'semantic_location': None
                    })

                    context.blackboard.set_worker_content({'type_specific': updated_type_specific})
                    await context.blackboard.sync_worker()
                else:
                    self.rocon_logger.error('cannot found updated_type_specific : {}'.format(updated_type_specific))

                await asyncio.sleep(UPDATE_SLEEP_INTERVAL/1000)

            trajectory = None


            updated_type_specific = pydash.get(context.blackboard.get_worker_content(), 'type_specific')
            if updated_type_specific:
                pydash.set_(updated_type_specific, 'location.semantic_location', semantic_location_id)
                context.blackboard.set_worker_content({'type_specific': updated_type_specific})

                await context.blackboard.sync_worker()
            else:
                self.rocon_logger.error('cannot found updated_type_specific : {}'.format(updated_type_specific))

        except Exception as err:
            print(err)
            err.with_traceback()

        return True


    async def bulldozer_moving(self, context, destination_pose, semantic_location_id=None, backward_progress=False):
        worker_content = context.blackboard.get_worker_content()
        worker_location = pydash.get(worker_content, 'type_specific.location')

        path = self.path_planner.get_path(worker_location['map'], worker_location['pose2d'], destination_pose)

        # draw original path on the path map image
        map_id = worker_location['map']
        map = self.path_planner.get_map_by_id(map_id)

        # path finding 경로 그리기
        if context.map_manager.feature_enable_show_path is True:
            image = context.map_manager.get_current_map_image_by_name(map['name'])

            def cb(pose):
                mono_p = self.path_planner.pose_to_mono(map, pose)
                return (
                    mono_p['x'], mono_p['y']
                )

            mono_path = pydash.map_(path, cb)
            self.draw_path_on_path_map(image, mono_path, color_path='green', radius=1)

        trajectory = self.path_planner.path_to_trajectory(worker_location['pose2d'], path, backward_progress=backward_progress)

        self.rocon_logger.debug('start to bulldozerMoving robot on path')

        disable_moving_simulation = pydash.get(context.worker.multi_client_options, 'disable_moving_simulation')
        if disable_moving_simulation:
            if len(trajectory) > 2:
                new_trajectory = []
                new_trajectory.append(trajectory[0])
                new_trajectory.append(trajectory[len(trajectory) - 1])

                trajectory = new_trajectory

        for point in trajectory:
            worker_content = context.blackboard.get_worker_content()

            #updated_type_specific = worker_content['type_specific']
            updated_type_specific = pydash.get(worker_content, 'type_specific')
            if updated_type_specific:
                if 'theta' in point and point['theta'] != None:
                    pass
                else:
                    point['theta'] = pydash.get(worker_content, 'type_specific.location.pose2d.theta')

                updated_type_specific['location'] = pydash.assign({}, updated_type_specific['location'], {
                    'map': worker_location['map'],
                    'pose2d': point,
                    'semantic_location': None
                })

                context.blackboard.set_worker_content({'type_specific': updated_type_specific})
                await context.blackboard.sync_worker()
            else:
                self.rocon_logger.error('cannot found updated_type_specific : {}'.format(updated_type_specific))

            await asyncio.sleep(UPDATE_SLEEP_INTERVAL/1000)

        updated_type_specific = pydash.get(context.blackboard.get_worker_content(), 'type_specific')
        if updated_type_specific:
            pydash.set_(updated_type_specific, 'location.semantic_location', semantic_location_id)
            context.blackboard.set_worker_content({'type_specific': updated_type_specific})
            await context.blackboard.sync_worker()
        else:
            self.rocon_logger.error('cannot found updated_type_specific : {}'.format(updated_type_specific))

        return True

    def draw_path_on_path_map(self, img, path, color_path='blue', radius=1):
        draw = ImageDraw.Draw(img)

        for i, pos in enumerate(path):
            if i == 0:
                # start point
                point_radius = radius
                color = 'red'

                rect = (pos[0] - point_radius, pos[1] - point_radius, pos[0] + point_radius, pos[1] + point_radius)
                draw.ellipse(rect, fill=color)
            elif i == len(path) - 1:
                # end point
                point_radius = radius
                color = 'red'

                rect = (pos[0] - point_radius, pos[1] - point_radius, pos[0] + point_radius, pos[1] + point_radius)
                draw.ellipse(rect, fill=color)
            else:
                color = color_path
                draw.point((pos[0], pos[1]), fill=color)
