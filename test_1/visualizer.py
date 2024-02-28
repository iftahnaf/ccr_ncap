import numpy as np
import cv2
import carla
import pygame

class Visualizer:

    """
    Class for visualizing data from Carla simulation using OpenCV and Pygame.

    This class provides methods to visualize data captured by Carla simulation, such as drawing
    bounding boxes around nearby vehicles in camera images and converting world-space locations
    to image-space coordinates. It uses OpenCV and Pygame for image processing and display.

    Attributes:
        camera (carla.Camera): The camera sensor used for capturing images.
        clock: Pygame clock object for controlling frame rate.
        world_2_camera (np.ndarray): Transformation matrix from world to camera coordinates.

    Methods:
        build_projection_matrix: Build a perspective projection matrix for camera.
        get_image_point: Convert world-space location to image-space coordinates.
        draw_bbox: Draw bounding boxes around nearby vehicles in camera images.
        get_bbox_vertices: Get the bounding box vertices.
        __del__: Destructor method to close OpenCV windows.

    Example:
        # Create a Visualizer instance
        visualizer = Visualizer(camera_sensor, camera_bp)

        # Draw bounding boxes around nearby vehicles in camera images
        visualizer.draw_bbox(image_front, world, ego_vehicle, relative_distance)

        # Get bounding box vertices
        bbox_vertices = visualizer.get_bbox_vertices()
    """

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
        """
        Build a perspective projection matrix for a given image size and field of view.

        Args:
            w (int): Width of the image (in pixels).
            h (int): Height of the image (in pixels).
            fov (int): Field of view angle (in degrees).

        Returns:
            np.ndarray: Perspective projection matrix.

        This method constructs a perspective projection matrix using the specified image width,
        height, and field of view. The matrix is computed based on the pinhole camera model
        and is suitable for transforming 3D points into 2D image coordinates.

        Example:
            w = 1920  # Image width in pixels
            h = 1080  # Image height in pixels
            fov = 90  # Field of view angle in degrees
            projection_matrix = build_projection_matrix(w, h, fov)
            print(projection_matrix)
            # Output:
            # array([[1073.7767415 ,    0.        ,  960.        ],
            #        [   0.        , 1073.7767415 ,  540.        ],
            #        [   0.        ,    0.        ,    1.        ]])

        """
        focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
        K = np.identity(3)
        K[0, 0] = K[1, 1] = focal
        K[0, 2] = w / 2.0
        K[1, 2] = h / 2.0
        return K
    
    @staticmethod
    def get_image_point(loc: carla.Location, K: np.ndarray, w2c: np.ndarray) -> list[float]:
        """
        Convert a world-space location to an image-space point.

        Args:
            loc (carla.Location): The world-space location to convert.
            K (np.ndarray): The camera intrinsic matrix (3x3).
            w2c (np.ndarray): The world-to-camera transformation matrix (4x4).

        Returns:
            list[float]: The image-space coordinates [x, y].

        This method transforms a given world-space location into image-space coordinates
        using the provided camera intrinsic matrix (K) and world-to-camera transformation
        matrix (w2c). It performs the necessary matrix multiplications and normalization
        to map the 3D point onto the 2D image plane.

        Example:
            loc = carla.Location(x=10.0, y=20.0, z=5.0)  # World-space location
            K = np.array([[1073.7767415, 0.0, 960.0],
                        [0.0, 1073.7767415, 540.0],
                        [0.0, 0.0, 1.0]])  # Camera intrinsic matrix
            w2c = np.array([[1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])  # World-to-camera transformation matrix
            img_point = get_image_point(loc, K, w2c)
            print(img_point)
            # Output: [960.0, 540.0]
        """
        point = np.array([loc.x, loc.y, loc.z, 1])
        point_camera = np.dot(w2c, point)
        point_camera = [point_camera[1], -point_camera[2], point_camera[0]]

        point_img = np.dot(K, point_camera)

        point_img[0] /= point_img[2]
        point_img[1] /= point_img[2]

        return point_img[0:2]
    
    def draw_bbox(self, image_front: carla.Image, world: carla.World, vehicle: carla.Vehicle, relative_distance: float) -> None:

        """
        Draw bounding boxes around nearby vehicles in the input image.

        Args:
            image_front (carla.Image): Front-facing camera image.
            world (carla.World): Carla world object.
            vehicle (carla.Vehicle): Ego vehicle.
            relative_distance (float): Relative distance to other vehicles.

        This method draws bounding boxes around nearby vehicles detected in the input image.
        The bounding boxes are drawn only for vehicles within a certain relative distance.
        The method filters out the ego vehicle to avoid drawing its bounding box.

        Example:
            # Assuming 'image_front', 'world', 'vehicle', and 'relative_distance' are defined
            scene.draw_bbox(image_front, world, vehicle, relative_distance)
        """

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

        cv2.imshow('Bounding Box Image',img)
        cv2.waitKey(1)

    def get_bbox_vertices(self) -> list[float]:
        """
        Get the bounding box vertices.

        Returns:
            list[float]: List containing the minimum and maximum x and y coordinates of the bounding box.

        This method retrieves the minimum and maximum x and y coordinates of the bounding box.
        If the attributes `x_min`, `x_max`, `y_min`, and `y_max` are not available, it returns
        [0, 0, 0, 0] as default values.

        Example:
            # Assuming x_min, x_max, y_min, and y_max are defined attributes of the object
            vertices = get_bbox_vertices()
            print(vertices)  # Output: [100, 200, 300, 400]
        """
        try:
            verdicts = [self.x_min, self.x_max, self.y_min, self.y_max]
        except Exception as e:
            if "has no attribute 'x_min'" in str(e):
                return [0, 0, 0, 0]
        return verdicts

    def __del__(self):
        cv2.destroyAllWindows()

    # Bounding box docs: https://carla.readthedocs.io/en/latest/tuto_G_bounding_boxes/
 