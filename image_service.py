import pygame
import colors

def split_image(_path, _ratio):
    if _path == None:
        return None
        
    image = pygame.image.load(_path)
    image_list = []
    image_list.append(pygame.Surface((10, 10)))
    image_list[0].fill(colors.WHITE)
    
    x = 0
    y = 0
    for i in range(_ratio):
        for j in range(_ratio):
            image_list.append(image.subsurface((x, y, image.get_height() / _ratio, image.get_width() / _ratio)))
            x += image.get_width() / _ratio
        x = 0
        y += image.get_height() / _ratio
    return image_list
