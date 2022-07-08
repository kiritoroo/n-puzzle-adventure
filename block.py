import os

try:
    import pygame
except:
    os.system('pip install pygame')
    import pygame
    
import colors
import settings

class Block():
    def __init__(self, _screen, _size, _pos, _value, _color, _image):
        self.screen = _screen
        self.size = _size
        self.pos = pygame.math.Vector2(_pos)
        self.value = _value
        self.color = _color
        self.image = _image
        self.init()

    def init(self):
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect(topleft = self.pos)

        self.value_pos = (self.rect.left + self.surf.get_width() / 2,
                        self.rect.top + self.surf.get_height() / 2)
        self.value_surf = settings.font.render(str(self.value), True, colors.BLACK)
        self.value_rect = self.value_surf.get_rect(center = self.value_pos)
        
        if self.image != None:
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.image_surf = self.image
            self.image_rect = self.image_surf.get_rect(topleft = self.pos)

        self.surf.fill(self.color)

    def draw(self):
        if self.image != None:
            if self.value > 0:
                self.screen.blit(self.image_surf, self.image_rect)
        else:
            if self.value == 0:
                self.set_color(colors.GREEN_DEFAULT)
            self.screen.blit(self.surf, self.rect)
            if self.value > 0:
                self.screen.blit(self.value_surf, self.value_rect)

    def update(self):
        pass

    def set_size(self, _size):
        self.size = _size
        self.init()
    
    def set_pos(self, _pos):
        self.pos = pygame.math.Vector2(_pos)
        self.init()

    def set_color(self, _color):
        self.color = _color
        self.surf.fill(self.color)
    
    def set_image(self, _image):
        self.image = _image
        self.init()
# Final Build