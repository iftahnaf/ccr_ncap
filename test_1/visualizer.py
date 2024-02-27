import pygame
from pygame.locals import K_ESCAPE
from pygame.locals import K_SPACE
from pygame.locals import K_a
from pygame.locals import K_d
from pygame.locals import K_s
from pygame.locals import K_w
import numpy as np
import cv2
import carla

VIEW_WIDTH = 1920//2
VIEW_HEIGHT = 1080//2
VIEW_FOV = 90

BB_COLOR = (248, 64, 24)


class Visualizer:
    def __init__(self, camera, camera_bp):
        pygame.init()

        self.camera = camera
    
        self.display = pygame.display.set_mode(
            (640, 480),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
    
        self.clock = pygame.time.Clock()
        self.world_2_camera = np.array(camera.get_transform().get_inverse_matrix())
        
        # Get the attributes from the camera
        image_w = camera_bp.get_attribute("image_size_x").as_int()
        image_h = camera_bp.get_attribute("image_size_y").as_int()
        fov = camera_bp.get_attribute("fov").as_float()

        # Calculate the camera projection matrix to project from 3D -> 2D
        self.K = self.build_projection_matrix(image_w, image_h, fov)

    def draw_image(self, image, blend=False):
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        if blend:
            image_surface.set_alpha(100)
        self.display.blit(image_surface, (0, 0))

    @staticmethod
    def build_projection_matrix(w, h, fov):
        focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
        K = np.identity(3)
        K[0, 0] = K[1, 1] = focal
        K[0, 2] = w / 2.0
        K[1, 2] = h / 2.0
        return K
    
    @staticmethod
    def get_image_point(loc, K, w2c):
        # Calculate 2D projection of 3D coordinate

        # Format the input coordinate (loc is a carla.Position object)
        point = np.array([loc.x, loc.y, loc.z, 1])
        # transform to camera coordinates
        point_camera = np.dot(w2c, point)

        # New we must change from UE4's coordinate system to an "standard"
        # (x, y ,z) -> (y, -z, x)
        # and we remove the fourth componebonent also
        point_camera = [point_camera[1], -point_camera[2], point_camera[0]]

        # now project 3D->2D using the camera matrix
        point_img = np.dot(K, point_camera)
        # normalize
        point_img[0] /= point_img[2]
        point_img[1] /= point_img[2]

        return point_img[0:2]
    
    def draw_bbox(self, img, world, vehicle, relative_distance):
        world_2_camera = np.array(self.camera.get_transform().get_inverse_matrix())

        for npc in world.get_actors().filter('*vehicle*'):

            # Filter out the ego vehicle
            if npc.id != vehicle.id:

                bb = npc.bounding_box
                dist = relative_distance

                # Filter for the vehicles within 50m
                if dist < 100.0:

                # Calculate the dot product between the forward vector
                # of the vehicle and the vector between the vehicle
                # and the other vehicle. We threshold this dot product
                # to limit to drawing bounding boxes IN FRONT OF THE CAMERA
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

    def get_bbox_vertices(self):
        try:
            verdicts = [self.x_min, self.x_max, self.y_min, self.y_max]
        except Exception as e:
            if "has no attribute 'x_min'" in str(e):
                return [0, 0, 0, 0]
        return verdicts

    # Bounding box docs: https://carla.readthedocs.io/en/latest/tuto_G_bounding_boxes/
 