import pygame
import sys


class Game:
    def __init__(self):
        # initiate pygame
        pygame.init()

        # create attributes of the screen and rocket
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen. get_rect()
        self.rocket = pygame.image.load('images/ship.bmp')
        self.rocket_rect = self.rocket.get_rect()
        self.rocket_rect.center = self.screen_rect.center

        # ship movement flags
        self.moving_rocket_right = False
        self.moving_rocket_left = False
        self.moving_rocket_up = False
        self.moving_rocket_down = False

        # ship speed
        self.rocket_speed = 12

    def run_game(self):
        while True:
            self._check_events()
            self._update_rocket()
            self._update_screen()

    def _check_events(self):
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._event_keydown(event)
            elif event.type == pygame.KEYUP:
                self._event_keyup(event)

    def _event_keydown(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_RIGHT:
            self.moving_rocket_right = True
        if event.key == pygame.K_LEFT:
            self.moving_rocket_left = True
        if event.key == pygame.K_UP:
            self.moving_rocket_up = True
        if event.key == pygame.K_DOWN:
            self.moving_rocket_down = True

    def _event_keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.moving_rocket_right = False
        if event.key == pygame.K_LEFT:
            self.moving_rocket_left = False
        if event.key == pygame.K_UP:
            self.moving_rocket_up = False
        if event.key == pygame.K_DOWN:
            self.moving_rocket_down = False

    def _update_rocket(self):
        # update rocket
        if self.moving_rocket_right and self.rocket_rect.right < self.screen_rect.right:
            self.rocket_rect.x += self.rocket_speed
        if self.moving_rocket_left and self.rocket_rect.left > self.screen_rect.left:
            self.rocket_rect.x -= self.rocket_speed
        if self.moving_rocket_up and self.rocket_rect.top > self.screen_rect.top:
            self.rocket_rect.y -= self.rocket_speed
        if self.moving_rocket_down and self.rocket_rect.bottom < self.screen_rect.bottom:
            self.rocket_rect.y += self.rocket_speed

    def _update_screen(self):
        # Update screen
        self.screen.fill((230, 230, 230))
        self.screen.blit(self.rocket, self.rocket_rect)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game()