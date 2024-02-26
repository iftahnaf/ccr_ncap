import pygame
import numpy as np
import cv2


class Visualizer:
    def __init__(self):
        pygame.init()
    
        self.display = pygame.display.set_mode(
            (640, 480),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
    
        self.clock = pygame.time.Clock()

    def draw_image(self, image, blend=False):
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        if blend:
            image_surface.set_alpha(100)
        self.display.blit(image_surface, (0, 0))