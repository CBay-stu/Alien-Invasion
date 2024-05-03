import sys 

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet
from alien import Alien


class AlienInvasion:

    def __init__(self):

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height


        pygame.display.set_caption("Caleb's Alien Invasion" )


        self.bg_color = (10, 70, 230)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):

        while True:

            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()



    def _check_events(self):
        
        for event in pygame.event.get():
            
            if event.type ==pygame.QUIT:
                sys.exit()
            
            elif event.type ==pygame.KEYDOWN:
                self._check_keydown_events(event) 
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
               

    def _check_keydown_events(self, event):
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True 
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
   
    def _check_keyup_events(self, event):
        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update() 

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet) 
                # Determine how many bullets still exist in the game to verify they're deleted
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Repsond to bullet-alien collisions
        # check for any bullets that have hit aliens. If so get rid of bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # Check to see if the aliens group is empty and if so, create a new fleet 
        if not self.aliens:
            # Destroy any existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
    
    def _update_aliens(self):
        #Update the position of all Aliens
        #Check if fleet is at edge then update
        self._check_fleet_edges()
        self.aliens.update() 

        # Look for alien_ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("WOMP WOMP")

    def _create_fleet(self):
        #Make a single alien
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        # Determine how much space you have on the screen for aliens
        available_space_x = self.settings.screen_width
        number_aliens_x = available_space_x // (2 * alien_width)
       
       # Determine the number of rows of aliens that fit on screen
        ship_height = self.hip.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)
        self.aliens.add(aliens)
    
    def _create_fleet(self):

        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size

        available_space_x = self.settings.screen_width
        number_aliens_x = available_space_x // (2 * alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):

        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        alien_width = aliens.rect.width
        aliens.x = alien_width + 2 * alien_width * alien_number
        aliens.rect.x = aliens.x
        aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
        self.aliens.add(aliens)
    
    def _check_fleet_edges(self):
        # Repsond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        # drop the fleet and change direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_screen(self):
            #Updates images on screen and flips
            self.screen.fill(self.settings.bg_color)
            self.ship.bitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            self.aliens.draw(self.screen)

            pygame.display.flip()



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

quit()