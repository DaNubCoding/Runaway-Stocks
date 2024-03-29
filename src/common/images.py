import pygame

from src.common.exe import pathof

pygame.init()
pygame.display.set_mode()

flip_power = pygame.image.load(pathof("res/images/flip.png")).convert_alpha()
angle_power = pygame.image.load(pathof("res/images/angle.png")).convert_alpha()
speed_power = pygame.image.load(pathof("res/images/speed.png")).convert_alpha()

power_images = {
    "flip": flip_power,
    "angle": angle_power,
    "speed": speed_power
}

pygame.display.quit()