import copy
import sys
from PIL import ImageDraw
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.best_first import BestFirst
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from rocon_client_sdk_py.utils.prohibit_util import *
from rocon_client_sdk_py.utils.util import *
from rocon_client_sdk_py.core_logic.context import Context
from rocon_client_sdk_py.logger.rocon_logger import rocon_logger
from rocon_client_sdk_py.const import *

# mono chrome color range 0 ~ 16777215
THRESHOLD_BLACK_VALUE = 16000000
VALID_MIN_ACCUMULATED_DISTANCE_METER = 0.4 # 최소 0.4미터 이동시 위치 기록
DIRECTION_CHANGING_ROTATION_MIN_DEGREE = 30 # 초기위치에서 첫 이동 전까지 방향전환을 위한 최소 회전각

FIRST_CHECK_DIRECTION = 1
FIRST_CHECK_DISTANCE = 2
# path의 주요 포인트 resampling 과정에서 방식
TYPE_RECORD_POSITION = FIRST_CHECK_DISTANCE

class PathPlanner(metaclass=SingletonMetaClass):
    def __init__(self, context:Context):
        self._context = context
        self._maps = None
        self.rocon_logger = rocon_logger

        self._current_path_map_id = ''
        self._current_path_map = None

        self.init_map()

    def init_map(self):
        start_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())

        self.rocon_logger.debug('pathPlanner initiating...')
        self._maps = self._context.map_manager.get_map_info_list()

        end_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
        gap = end_time_ms - start_time_ms
        self.rocon_logger.debug('Required time msec of init_map : {}'.format(gap))
        self.rocon_logger.debug('pathPlanner initialized')

    def get_path(self, map, pose_a, pose_b):
        self.rocon_logger.debug('\n')

        if isinstance(map, str):
            map = pydash.find(self._maps, {'id':map}) or map
        else:
            #TODO 이 경우 없는지 다시 확인 후 삭제
            map = pydash.find(self._maps, {'id': map['id']}) or map

        map_id = map['id']

        path_map = self.get_current_path_map(map)
        path_map.cleanup()

        #grid_map_image = self._grid_map_images[map_id]
        #grid_map_image.show()

        mono_point_a = self.pose_to_mono(map, pose_a)
        mono_point_b = self.pose_to_mono(map, pose_b)

        valid = True
        if path_map is None:
            self.rocon_logger.debug('getPath() : pathMap was not loaded for map')
            valid = False

        gpx_a = self.get_monochrome_pixel(map, mono_point_a['x'], mono_point_a['y'])
        if gpx_a:
            if gpx_a.walkable is False:
                self.rocon_logger.debug('[pathPlanner]: getPath(): departure point({},{}) on map:{} is located in nonwalkable position'.format(gpx_a.x, gpx_a.y, map_id))
                valid = False

        else:
            self.rocon_logger.debug('[pathPlanner]: getPath(): departure point is out of gridmap range')
            valid = False

        gpx_b = self.get_monochrome_pixel(map, mono_point_b['x'], mono_point_b['y'])
        if gpx_b is None:
            valid = False

        else:
            if gpx_b.walkable is False:
                self.rocon_logger.debug('[pathPlanner]: getPath(): destination point({},{}) on map:{} is out of gridmap range'.format(gpx_b.x, gpx_b.y, map_id))
                valid = False

        if valid is False:
            return []

        finder = self.get_finder_algorithm(DEFAULT_FINDER_ALGORITHM)

        path = None
        try:
            self.rocon_logger.debug('** find_path : ({},{}) -> ({},{})'.format(gpx_a.x, gpx_a.y, gpx_b.x, gpx_b.y))

            path, runs = finder.find_path(gpx_a, gpx_b, path_map)
            self.rocon_logger.debug('operations : {}, path points length : {}'.format(str(runs), len(path)))

        except Exception as err:
            self.rocon_logger.error('Exception occurred', exception=err)
            self.rocon_logger.error('[check here.. path_planner] exception error')

        path_map.cleanup()
        del path_map

        if path and len(path) > 0:
            path3 = pydash.map_(path, lambda point: {'x':point[0], 'y':point[1]})
            pose_path = self.grid_path_to_pose_path(map, path3)

            return pose_path
        else:
            self.rocon_logger.debug('[check here.. path_planner] Not found path')
            return []

    def get_map_by_id(self, map_id):
        map = pydash.find(self._maps, {'id': map_id})
        return map

    def get_finder_algorithm(self, using_algorithm=ASTAR_FINDER):
        if using_algorithm is ASTAR_FINDER:
            self.rocon_logger.debug('using finder algorithm : AStarFinder')
            return AStarFinder(diagonal_movement=DiagonalMovement.always, weight=1)
        elif using_algorithm is BEST_FIRST_FINDER:
            self.rocon_logger.debug('using finder algorithm : BestFirst')
            return BestFirst(diagonal_movement=DiagonalMovement.always,weight=1)
        elif using_algorithm is DIJKSTRA_FINDER:
            self.rocon_logger.debug('using finder algorithm : Dijkstara')
            return DijkstraFinder(diagonal_movement=DiagonalMovement.always, weight=1)
        else:
            self.rocon_logger.error('using finder algorithm : Not defined')
            return None

    def draw_path(self, img, path, color_path='blue', radius=1):
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

        #img.show()

    def get_monochrome_pixel(self, map, x, y):
        map_id = map['id']
        path_map = self.get_current_path_map(map)
        if path_map is None:
            self.rocon_logger.debug('pathMap is not loaded')
            return None

        if x > path_map.width or y > path_map.height:
            self.rocon_logger.debug('get_monochrome_pixel: Coordinates must be smaller than gridmap size')
            return None
        elif x < 0 or y < 0:
            self.rocon_logger.debug('get_monochrome_pixel: Coordinates must be positive')
            return None

        return path_map.node(x,y)

    def get_current_path_map(self, map):
        map_id = map['id']
        if map_id == self._current_path_map_id:
            return self._current_path_map
        else:
            if self._current_path_map is not None:
                self._current_path_map.cleanup()

            self._current_path_map = None
            self._current_path_map_id = None

        self._current_path_map_id = map_id
        self._current_path_map = self.load_path_map(map)
        return self._current_path_map

    def path_to_trajectory(self, worker_pose, path, backward_progress=False):

        if path is None or len(path) == 0:
            return []

        #출발전 방향 전환 포인트 추가
        if backward_progress is False:
            trajectory = self.prepare_changing_direction_before_trajectory(worker_pose['theta'], path)
        else:
            trajectory = []

        before = path[0]

        last_idx = len(path)-1
        valid_point = False
        valid_accumulated_dist = 0

        prev_direction = 0
        if len(trajectory) > 0:
            prev_direction = trajectory[-1]['theta']

        current = None
        for idx in range(1, len(path)):

            current = path[idx]
            distance = self.get_distance_pose_to_pose(before, current)
            valid_accumulated_dist += distance
            direction = self.get_angle_positive_rad(before, current)
            if backward_progress:
                direction += math.pi
                if direction >= math.pi*2:
                    direction -= math.pi*2


            modified_direct = direction

            diff_direct = self.get_diff_rad(prev_direction, direction)
            diff_degree = self.get_degree_by_rad(diff_direct)

            # 3포인트 전방으로의 방향성 구하기
            if idx < last_idx - 3:
                modified_direct = self.get_angle_positive_rad(path[idx], path[idx+3])
                if backward_progress:
                    modified_direct += math.pi
                    if modified_direct >= math.pi * 2:
                        modified_direct -= math.pi * 2

            if TYPE_RECORD_POSITION == FIRST_CHECK_DIRECTION:
                # 변경 각도 우선 포인트 기록 방식
                if abs(diff_degree) >= 15:
                    #15도 이상 방향 변경시 항상 기록
                    valid_point = True
                else:
                    if valid_accumulated_dist >= VALID_MIN_ACCUMULATED_DISTANCE_METER:
                        # 누적 이동 거리가 유효 범위 이상이면 기록
                        valid_point = True
            elif TYPE_RECORD_POSITION == FIRST_CHECK_DISTANCE:
                # 누적 이동 거리 우선 포인트 기록 방식
                if valid_accumulated_dist >= VALID_MIN_ACCUMULATED_DISTANCE_METER:
                    # 누적 이동 거리가 유효 범위 이상이면 기록
                    valid_point = True


            current = pydash.assign(current, {'theta': modified_direct})
            before = current

            if idx > 0:
                prev_direction = modified_direct

            if idx == last_idx:
                # 마지막 포인트 항상 기록
                trajectory.append(path[idx])
            else:

                if valid_point is True:
                    trajectory.append(current)
                    valid_accumulated_dist = 0

            valid_point = False

        #print('trajectory len : {}'.format(len(trajectory)))
        #마지막 위치로의 이동 보장위해 n개의 마지막 위치 복사본 추가
        if current is not None:
            for i in range(1):
                trajectory.append(current)

        return trajectory

    #두 양의 rad 사이의 차이 rad 반환, 부호는 +는 ccw, -는 cw
    def get_diff_rad(self, rad1, rad2):
        r1 = rad1 if rad1 <= math.pi else rad1 - math.pi
        r2 = rad2 if rad2 <= math.pi else rad2 - math.pi

        return r2 - r1

    # worker_location (초기 위치)에서 path의 진행 방향으로 회전 전환하는 포인트 추가해서 리턴
    def prepare_changing_direction_before_trajectory(self, init_theta, path):
        pre_trajectory = []

        try:

            init_direction = init_theta
            target_idx = 0
            # 초기 위치에서 전방 3포인트로의 방향 계산
            if len(path) >= 4: target_idx = 3
            elif len(path) > 0: target_idx = -1

            direction = self.get_angle_positive_rad(path[0], path[target_idx])

            max_direct = max(init_direction, direction)
            min_direct = min(init_direction, direction)
            diff_direct = abs(max_direct - min_direct)
            if diff_direct > math.pi: diff_direct = math.pi*2 - diff_direct

            diff_degree = self.get_degree_by_rad(diff_direct)

            if diff_degree > DIRECTION_CHANGING_ROTATION_MIN_DEGREE:
                step = 0
                step_rad = self.get_rad_by_degree(DIRECTION_CHANGING_ROTATION_MIN_DEGREE)
                # CCW(+) or CW(-) 결정
                step_rad = step_rad if init_direction + diff_direct == direction else -step_rad

                last_theta = -100
                for i in range(0, int(diff_degree/DIRECTION_CHANGING_ROTATION_MIN_DEGREE)):
                    step += step_rad
                    rotate_path = copy.copy(path[0])
                    last_theta = init_direction + step
                    rotate_path = pydash.assign(rotate_path, {'theta': last_theta})
                    pre_trajectory.append(rotate_path)

                if last_theta is not -100:
                    path[0]['theta'] = last_theta


        except Exception as err:
            self.rocon_logger.debug('something wrong, check here')
            pre_trajectory = []

        return pre_trajectory

    def mono_to_pose(self, map, point_on_monochrome):
        mono = self.get_monochrome_metadata(map)
        grid = self.get_gridmap_metadata(map)
        map_point = {
            'x': (point_on_monochrome['x']*grid['width'])/mono['width'],
            'y': (point_on_monochrome['y']*grid['height'])/mono['height']
        }
        return self.map_to_pose(map, map_point)

    def pose_to_mono(self, map, pose):
        map_point = self.pose_to_map(map, pose)
        mono = self.get_monochrome_metadata(map)
        grid = self.get_gridmap_metadata(map)
        return{
            'x': round((map_point['x']*mono['width'])/grid['width']),
            'y': round((map_point['y']*mono['height'])/grid['height'])
        }

    def pose_to_map(self, map, pose):
        origin = self.get_origin_coordinate(map)
        scale = self.get_scale_meter_to_pixel(map)
        return {
            'x': origin['x'] + pose['x']*scale,
            'y': origin['y'] - pose['y']*scale
        }

    def map_to_pose(self, map, map_point):
        origin = self.get_origin_coordinate(map)
        scale = self.get_scale_meter_to_pixel(map)
        return{
            'x': (map_point['x'] - origin['x'])/scale,
            'y': (origin['y'] - map_point['y']) / scale
        }

    def get_monochrome_metadata(self, map):
        monochrome = pydash.get(map, 'metadata.monochrome')
        if monochrome is None:
            self.rocon_logger.debug('map record is malformed "metadata.monochrome" is undefined')

        return monochrome

    def get_origin_coordinate(self, map):
        origin = pydash.get(map, 'metadata.gridmap.origin')
        if origin is None:
            self.rocon_logger.debug('map record is malformed "metadata.gridmap.origin" is undefined')

        return origin

    def get_gridmap_metadata(self, map):
        gridmap = pydash.get(map, 'metadata.gridmap')
        if gridmap is None:
            self.rocon_logger.debug('map record is malformed "metadata.gridmap" is undefined')

        return gridmap

    def get_scale_meter_to_pixel(self, map):
        scale = pydash.get(map, 'metadata.gridmap.scale_m2px')
        if scale is None:
            self.rocon_logger.debug('map record is malformed "metadata.gridmap.scale_m2px" is undefined')

        return scale

    def get_distance_pose_to_pose(self, pose_a, pose_b):
        dx = pose_a['x'] - pose_b['x']
        dy = pose_a['y'] - pose_b['y']
        return math.sqrt(dx*dx + dy*dy)

    def get_distance(self, path):
        if len(path) == 0:
            return sys.maxsize

        distance = 0
        for i in range(len(path)-1):
            distance += self.get_distance_pose_to_pose(path[i+1], path[i])

        return distance

    def get_degree_by_rad(self, rad):
        deg = (rad*180)/math.pi
        return deg

    def get_rad_by_degree(self, degree):
        rad = degree*math.pi/180
        return rad

    def get_angle_rad(self, pose_a, pose_b):
        radian = math.atan2(pose_b['y'] - pose_a['y'], pose_b['x'] - pose_a['x'])
        return radian

    def get_angle_positive_rad(self, pose_a, pose_b):
        radian = math.atan2(pose_b['y'] - pose_a['y'], pose_b['x'] - pose_a['x'])
        if radian < 0:
            radian = (2*math.pi) + radian

        return radian

    def grid_path_to_pose_path(self, map, path):
        return pydash.map_(path, lambda point: self.mono_to_pose(map, point))

    def direction(self, point_a, point_b, point_c):

        dir = 1
        dx_ab = point_b['x'] - point_a['x']
        dy_ab = point_b['y'] - point_a['y']
        dx_ac = point_c['x'] - point_a['x']
        dy_ac = point_c['y'] - point_a['y']
        if dx_ab * dy_ac < dy_ab * dx_ac: dir = 1 # 시계방향
        if dx_ab * dy_ac > dy_ab * dx_ac: dir = -1 # 반시계방향
        if dx_ab * dy_ac == dy_ab * dx_ac: # 일직선 상에 있는 경우
            if dx_ab == 0 and dy_ab == 0: dir = 0 # A = B
            elif (dx_ab * dx_ac < 0) or (dy_ab * dy_ac < 0): dir = -1; # A가 가운데
            elif (dx_ab * dx_ab + dy_ab * dy_ab >= dx_ac * dx_ac + dy_ac * dy_ac): dir = 0; # C가 가운데
            else: dir = 1; # B가 가운데

        return dir

    def is_cross(self, pa, pb, pc, pd):
        condition_a = (self.direction(pa, pb, pc) * self.direction(pa, pb, pd) <= 0)
        condition_b = (self.direction(pc, pd, pa) * self.direction(pc, pd, pb) <= 0)

        return condition_a and condition_b

    def is_pass_through(self, paths, area):

        p1 = {
            'x': -1 * area.width / 2,
            'y': area.height / 2,
        }

        p2 = {
            'x': area.width / 2,
            'y': -1 * area.height / 2,
        }

        p3 = {
            'x': -1 * area.width / 2,
            'y': -1 * area.height / 2,
        }

        p4 = {
            'x': area.width / 2,
            'y': area.height / 2,
        }

        def rotate(point, theta):
            output = {}
            output['x'] = point['x'] * math.cos(theta) - point['y'] * math.sin(theta)
            output['y'] = point['y'] * math.cos(theta) + point['x'] * math.sin(theta)
            return output


        def shift(point, width, height):
            point['x'] += width
            point['y'] += height
            return point

        p1 = rotate(p1, area.theta)
        p2 = rotate(p2, area.theta)
        p3 = rotate(p3, area.theta)
        p4 = rotate(p4, area.theta)

        p1 = shift(p1, area.x, area.y)
        p2 = shift(p2, area.x, area.y)
        p3 = shift(p3, area.x, area.y)
        p4 = shift(p4, area.x, area.y)

        for i in range(len(paths)-1):

            point_path_1 = paths[i]
            point_path_2 = paths[i + 1]

            if self.is_cross(p1, p2, point_path_1, point_path_2) or self.is_cross(p2, p3, point_path_1, point_path_2) or self.is_cross(p3, p4, point_path_1, point_path_2) or self.is_cross(p4, p1, point_path_1, point_path_2):
                xgap = paths[0].x - area.x
                ygap = paths[0].y - area.y
                return math.sqrt(xgap * xgap + ygap * ygap)

        return -1

    async def is_pass_through_area(self, paths, areas):
        for area in areas:
            distance = self.is_pass_through(paths, area)

            if distance >= 0:
                return True

        return False

    def load_path_map(self, map):

        map_id = map['id']
        grid_map_image = self._context.map_manager.load_map_image(map_id)

        w = grid_map_image.width
        h = grid_map_image.height

        new_grid_map = Grid(w, h)
        non_walkable = 0

        prohibit_zones = self._context.map_manager.get_prohibit_zones(map['id'])
        prohibits_mono_rects = []
        rects = []

        for zone in prohibit_zones:
            rect = area_to_rect(map, zone['areas'][0])
            rects.append(rect)
            mono_rect = rect_to_mono_rect(map, rect)
            prohibits_mono_rects.append(mono_rect)

        self.rocon_logger.debug('prohibit_zones ({}) prohibits_rects : {}'.format(map['name'], rects))
        self.rocon_logger.debug('prohibit_zones ({}) prohibits_mono_rects : {}'.format(map['name'], prohibits_mono_rects))

        px = grid_map_image.load()
        self.rocon_logger.debug('map ({}) image width :{}, height :{}'.format(map['name'], grid_map_image.size[0], grid_map_image.size[1]))

        start_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())

        # 금지구역은 별도로 non_walkable처리한다.
        for_check_map = False

        draw = ImageDraw.Draw(grid_map_image)
        for rect in prohibits_mono_rects:
            poly = [(int(rect['lt']['x']), int(rect['lt']['y'])), (int(rect['rt']['x']), int(rect['rt']['y'])),
                    (int(rect['rb']['x']), int(rect['rb']['y'])), (int(rect['lb']['x']), int(rect['lb']['y']))]

            draw.polygon(poly, fill="#000000")

        if for_check_map:
            self.rocon_logger.info('for_check_map flag is True')
            grid_map_image.show()

        try:
            width = grid_map_image.size[0]
            height = grid_map_image.size[1]

            for y in range(height):
                for x in range(width):
                    rgb_tuple = px[x, y]

                    pixel_value = self.rgb_to_int(rgb_tuple)
                    node = new_grid_map.node(x, y)

                    if pixel_value <= THRESHOLD_BLACK_VALUE:
                        # THRESHOLD_BLACK_VALUE 이하의 값은 검정색으로 간주하여 non walkable 영역으로 처리한다.
                        node.walkable = False
                        non_walkable += 1

                    else:
                        node.walkable = True

        except Exception as err:
            err.with_traceback()

        end_time_ms = get_time_milliseconds(current_datetime_utc_iso_format())
        gap = end_time_ms - start_time_ms
        self.rocon_logger.debug('Required time msec of load_map loop : {}'.format(gap))

        #grid_map_image.show()
        #self.rocon_logger.debug('end')

        del px
        grid_map_image.close()
        del grid_map_image


        return new_grid_map

    def rgb_to_int(self, rgb_tuple):
        rgb_int = rgb_tuple[0] << 16 | rgb_tuple[1] << 8 | rgb_tuple[2]
        return rgb_int

    def get_map_path_by_trajectory(self, map, trajectory):
        origin = self.get_origin_coordinate(map)
        scale = self.get_scale_meter_to_pixel(map)

        def cb(pose):
            return (
                origin['x'] + pose['x'] * scale,
                origin['y'] - pose['y'] * scale
            )

        path = pydash.map_(trajectory, cb)
        return path

    def get_least_diff_degree_direction(self, pose_a, pose_b):
        '''
        두 지점간의 최소 각도 및 방향 구하기
        :param pose_a:
        :param pose_b:
        :return: degree, direction ('cw' or 'ccw)
        '''
        degree = 0
        direction = 'ccw'

        theta_a = pydash.get(pose_a, 'theta')
        theta_b = pydash.get(pose_b, 'theta')
        rad = theta_b - theta_a
        degree = math.fabs(self.get_degree_by_rad(rad))

        if theta_a >= 0 and theta_b >= 0:
            direction = 'ccw' if rad > 0 else 'cw'
        elif theta_a >= 0 and theta_b < 0:
            if degree <= 180:
                direction = 'cw'
            else:
                degree = degree - 180
                direction = 'ccw'
        elif theta_a < 0 and theta_b >= 0:
            if degree <= -180:
                direction = 'ccw'
            else:
                degree = degree - 180
                direction = 'cw'
        elif theta_a < 0 and theta_b < 0:
            direction = 'cw' if rad <0 else 'ccw'


        return degree, direction

    def get_pose_by_distance(self, current_pose, distance):
        '''
        현재 current_pose 에서 distance 만큼 떨어진 거리에 있는 pose 리턴
        :param current_pose:
        :param distance:
        :return:
        '''

        x = pydash.get(current_pose, 'x')
        y = pydash.get(current_pose, 'y')
        theta = pydash.get(current_pose, 'theta')

        target_x = x + distance*math.cos(theta)
        target_y = y + distance*math.sin(theta)

        pose={
            'x': target_x,
            'y': target_y,
            'theta':theta
        }

        return pose

    def get_theta_by_pose(self, start_pose, end_pose):
        '''
        두점을 일직선 상에 놓았을때의 시작점에서 끝점쪽으로의 방향 theta값 리턴
        '''

        try:

            theta = 0

            dy = end_pose['y'] - start_pose['y']
            dx = end_pose['x'] - start_pose['x']

            theta = math.atan2(dy, dx)

        except Exception as err:
            print(err)

        return theta

    def get_trans_direction(self, current_theta, target_theta):
        '''
        현재 theta에서 target_theta로의 방향 전환의 최소 각도와 회전 방향을 리턴
        return rdegree, 'cw' or 'ccw'
        '''

        diff_theta = math.fabs(target_theta - current_theta)
        if diff_theta > math.pi:
            rdegree = self.get_degree_by_rad(math.pi - diff_theta)
        else:
            rdegree = self.get_degree_by_rad(diff_theta)

        if current_theta >= target_theta + math.pi:
            return rdegree, 'ccw'
        else:
            return rdegree, 'cw'
