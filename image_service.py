import pygame
import colors

def split_image(_path):
    if _path == None:
        return None
        
    image = pygame.image.load(_path)
    image_list = []
    image_list.append(pygame.Surface((10, 10)))
    image_list[0].fill(colors.WHITE)
    
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            image_list.append(image.subsurface((x, y, image.get_height() / 3, image.get_width() / 3)))
            x += image.get_width() / 3
        x = 0
        y += image.get_height() / 3
    return image_list
