import sys 
import os
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard

class AlienInvasion:

    def __init__(self):

        pygame.init()
        pygame.font.init()
        self.settings = Settings()

        #Sets Screen
        self.screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #draws caption
        pygame.display.set_caption("Caleb's Alien Invasion" )

        # Initializes classes
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        #sets background color
        self.bg_color = (255, 255, 255)

        
        # Initializes classes
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):

        while True:
            # call a method to check to see if any keybpard events have occured
            self._check_events()
            # check to see if the game is still active
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

            #updates screen
            pygame.display.flip()


    def _check_events(self):
        #Responds to keypresses and events
        for event in pygame.event.get():
            
            if event.type ==pygame.QUIT:
                sys.exit()
            
            elif event.type ==pygame.KEYDOWN:
                self._check_keydown_events(event) 
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
               

    def _check_keydown_events(self, event):
        
        # Responds to events with keys
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
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
        self.sb.prep_score()
            
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
            self._ship_hit()
       
        #Look for aliens hitting the button of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        #Make a single alien
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        # Determine how much space you have on the screen for aliens
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
       
       # Determine the number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    
   
    def _create_alien(self, alien_number, row_number):
        #Creates Alien
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
    
    def _ship_hit(self):
        #respond to the ship being hit by an alien

        if self.stats.ships_left >0:
            # decrement the number of ships left
            self.stats.ships_left -= 1
            self.sb.prep_ship()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

                                              
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause for half a second
            sleep (0.6)
        else:
            self.stats.game_active = False
    
    def _check_aliens_bottom(self):
        #check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
            #Updates images on screen and flips
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            #Draws on Screen
            
            self.aliens.draw(self.screen)

            self.sb.show_score()

            #Updates screen

            pygame.display.flip()
            



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
quit()
