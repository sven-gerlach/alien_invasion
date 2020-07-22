import pygame
import sys
from time import sleep

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        # instantiate ship
        self.ship = Ship(self)
        self.ship_speed = self.ship.ship_speed

        # sprites for bullets and aliens
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # create fleet
        self._create_fleet()

        # Game Stats
        self.life = 3
        self.game_active = True

    def game_loop(self):
        while True:
            self._check_user_inputs()
            if self.game_active:
                self.ship.update()
                self._bullet_update()
                self._alien_update()
                self._collision_update()
            self._screen_update()

    def _check_user_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_event_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_event_keyup(event)

    def _check_event_keydown(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_UP:
            self.ship.ship_moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.ship_moving_down = True
        elif event.key == pygame.K_SPACE:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_event_keyup(self, event):
        if event.key == pygame.K_UP:
            self.ship.ship_moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.ship_moving_down = False

    def _bullet_update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.screen_rect.right:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        alien = Alien(self)
        # find max number of aliens in a column
        number_aliens_y = (self.screen_height -
                           alien.rect.height) // (2 * alien.rect.height)

        # find max number of columns
        number_columns = (self.screen_width - self.ship.rect.width - alien.rect.width * 3) // \
                         (alien.rect.width * 2)

        # generate fleet of aliens
        for column_number in range(number_columns):
            for alien_number in range(number_aliens_y):
                self._generate_alien(alien_number, column_number)

    def _generate_alien(self, alien_number, column_number):
        alien = Alien(self)
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * alien_number
        alien.rect.x = self.screen_width - (2 * alien.rect.width * (column_number + 1))
        self.aliens.add(alien)

    def _alien_update(self):
        self._check_alien_fleet_edges()
        self.aliens.update()
        self._check_life_event()

    def _check_alien_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                Alien.alien_speed_y_direction *= -1
                for alien in self.aliens.sprites():
                    alien.rect.x += alien.alien_speed_x
                break

    def _check_life_event(self):
        self._check_alien_collision_with_ship()
        self._check_alien_collision_with_screenbottom()

    def _check_alien_collision_with_ship(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._loss_of_life_event()

    def _check_alien_collision_with_screenbottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.left <= self.screen_rect.left:
                self._loss_of_life_event()
                break

    def _loss_of_life_event(self):
        if self.life > 1:
            self.life -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.re_center()
            sleep(1)
        else:
            self.game_active = False

    def _collision_update(self):
        collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _screen_update(self):
        self.screen.fill((230, 230, 230))
        self.screen.blit(self.ship.image, self.ship.rect)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()


class Ship:
    def __init__(self, ai_game):
        self.screen_rect = ai_game.screen_rect
        self.ship = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.rotate(self.ship, -90)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        # Ship movement glags and settings
        self.ship_moving_up = False
        self.ship_moving_down = False
        self.ship_speed = 12

    def update(self):
        if self.ship_moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.ship_speed
        if self.ship_moving_up and self.rect.top > self.screen_rect.top:
            self.rect.y -= self.ship_speed

    def re_center(self):
        self.rect.midleft = self.screen_rect.midleft


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.ship_rect = ai_game.ship.rect
        self.rect = pygame.Rect(0, 0, 15, 3)
        self.rect.midleft = self.ship_rect.midright

    def update(self):
        self.rect.x += 5

    def draw_bullet(self):
        pygame.draw.rect(self.screen, (60, 60, 60), self.rect)


class Alien(pygame.sprite.Sprite):
    # alien movement settings
    alien_speed_y = 10
    alien_speed_x = -10
    alien_speed_y_direction = 1

    def __init__(self, ai_game):
        super().__init__()
        self.screen_rect = ai_game.screen_rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.right - 2 * self.rect.width
        self.rect.y = self.rect.height
        self.ship_speed = ai_game.ship_speed

    def check_edges(self):
        """Return True if alien is beyond edge of screen"""
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top < 0:
            return True

    def update(self):
        """move alien up or down"""
        self.rect.y += self.alien_speed_y * self.alien_speed_y_direction

    def center_ship(self):
        self.rect.midleft = self.screen_rect.midleft


if __name__ == '__main__':
    game = Game()
    game.game_loop()

