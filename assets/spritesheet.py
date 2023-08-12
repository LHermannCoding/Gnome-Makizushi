import pygame

class SpriteSheet():
    """
    Class for managing gnome spritesheets to reduce asset load required
    and use animation swaps.
    """
    def __init__(self, image):
        self.sheet = image
        
    def get_image(self,frame,width,height,color,scale=1):
        """
        Get specific image from spritesheet based on given frame.

        """
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image