import pygame

class Settings:

    def __init__(self):

        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #Ship settings 
        self.ship_speed = 4.0
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 4.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 3

        #alien settings
        self.alien_speed = 2.2
        self.fleet_drop_speed = 20
        #Fleet direction, 1 = right, -1 = left
        self.fleet_direction = 1

        self.alien_points = 50 

        