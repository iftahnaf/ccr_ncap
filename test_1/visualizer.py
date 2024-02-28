import numpy as np
import cv2
import carla
import pygame

class Visualizer:
    def __init__(self, camera, camera_bp):
        pygame.init()
        self.camera = camera
        self.clock = pygame.time.Clock()
        self.world_2_camera = np.array(camera.get_transform().get_inverse_matrix())
        
        image_w = camera_bp.get_attribute("image_size_x").as_int()
        image_h = camera_bp.get_attribute("image_size_y").as_int()
        fov = camera_bp.get_attribute("fov").as_float()

        self.K = self.build_projection_matrix(image_w, image_h, fov)

    @staticmethod
    def build_projection_matrix(w: int, h: int, fov: int) -> np.ndarray:
        focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
        K = np.identity(3)
        K[0, 0] = K[1, 1] = focal
        K[0, 2] = w / 2.0
        K[1, 2] = h / 2.0
        return K
    
    @staticmethod
    def get_image_point(loc: carla.Location, K: np.ndarray, w2c: np.ndarray) -> list[float]:
        point = np.array([loc.x, loc.y, loc.z, 1])
        point_camera = np.dot(w2c, point)
        point_camera = [point_camera[1], -point_camera[2], point_camera[0]]

        point_img = np.dot(K, point_camera)

        point_img[0] /= point_img[2]
        point_img[1] /= point_img[2]

        return point_img[0:2]
    
    def draw_bbox(self, image_front: carla.Image, world: carla.World, vehicle: carla.Vehicle, relative_distance: float) -> None:

        img = np.reshape(np.copy(image_front.raw_data), (image_front.height, image_front.width, 4))
        world_2_camera = np.array(self.camera.get_transform().get_inverse_matrix())

        for npc in world.get_actors().filter('*vehicle*'):

            # Filter out the ego vehicle
            if npc.id != vehicle.id:

                bb = npc.bounding_box
                dist = relative_distance

                if dist < 100.0:

                    forward_vec = vehicle.get_transform().get_forward_vector()
                    ray = npc.get_transform().location - vehicle.get_transform().location

                    if forward_vec.dot(ray) > 1:
                        # p1 = self.get_image_point(bb.location, self.K, world_2_camera) #http://host.robots.ox.ac.uk/pascal/VOC/
                        verts = [v for v in bb.get_world_vertices(npc.get_transform())]
                        self.x_max = -10000
                        self.x_min = 10000
                        self.y_max = -10000
                        self.y_min = 10000

                        for vert in verts:
                            p = self.get_image_point(vert, self.K, world_2_camera)
                            # Find the rightmost vertex
                            if p[0] > self.x_max:
                                self.x_max = p[0]
                            # Find the leftmost vertex
                            if p[0] < self.x_min:
                                self.x_min = p[0]
                            # Find the highest vertex
                            if p[1] > self.y_max:
                                self.y_max = p[1]
                            # Find the lowest  vertex
                            if p[1] < self.y_min:
                                self.y_min = p[1]

                        cv2.line(img, (int(self.x_min),int(self.y_min)), (int(self.x_max),int(self.y_min)), (0,0,255, 255), 1)
                        cv2.line(img, (int(self.x_min),int(self.y_max)), (int(self.x_max),int(self.y_max)), (0,0,255, 255), 1)
                        cv2.line(img, (int(self.x_min),int(self.y_min)), (int(self.x_min),int(self.y_max)), (0,0,255, 255), 1)
                        cv2.line(img, (int(self.x_max),int(self.y_min)), (int(self.x_max),int(self.y_max)), (0,0,255, 255), 1)


        cv2.imshow('ImageWindowName',img)
        cv2.waitKey(1)

    def get_bbox_vertices(self) -> list[float]:
        try:
            verdicts = [self.x_min, self.x_max, self.y_min, self.y_max]
        except Exception as e:
            if "has no attribute 'x_min'" in str(e):
                return [0, 0, 0, 0]
        return verdicts

    # Bounding box docs: https://carla.readthedocs.io/en/latest/tuto_G_bounding_boxes/
 