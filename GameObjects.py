import pygame


class GameObject(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class Bullet(GameObject):
    def __init__(self, x, y, width, height, accel):
        super(Bullet, self).__init__(x, y, width, height)
        self.accel = accel

    def update(self):
        self.rect.y += self.accel
        return 0


class Character(GameObject):
    def __init__(self, x, y, width, height, hit_points):
        super(Character, self).__init__(x, y, width, height)
        self.hit_points = hit_points
        self.last_time_shoot = 0

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        return 0
