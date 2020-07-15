import pygame
import sys


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.ship = pygame.image.load('images/ship.bmp')
        self.ship_rotated = pygame.transform.rotate(self.ship, -90)
        self.ship_rect = self.ship_rotated.get_rect()
        # Ship movement flags
        self.ship_moving_up = False
        self.ship_moving_down = False
        self.ship_speed = 12
        self.bullets = pygame.sprite.Group()

    def game_loop(self):
        while True:
            self._check_user_inputs()
            self._ship_update()
            self._bullet_update()
            self._screen_update()

    def _check_user_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_UP:
                    self.ship_moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship_moving_down = True
                elif event.key == pygame.K_SPACE:
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship_moving_up = False
                if event.key == pygame.K_DOWN:
                    self.ship_moving_down = False

    def _ship_update(self):
        if self.ship_moving_down and self.ship_rect.bottom < self.screen_rect.bottom:
            self.ship_rect.y += self.ship_speed
        if self.ship_moving_up and self.ship_rect.top > self.screen_rect.top:
            self.ship_rect.y -= self.ship_speed

    def _bullet_update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.bullet_rect.left > self.screen_rect.right:
                self.bullets.remove(bullet)

    def _screen_update(self):
        self.screen.fill((230, 230, 230))
        self.screen.blit(self.ship_rotated, self.ship_rect)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.ship_rect = ai_game.ship_rect
        self.bullet_rect = pygame.Rect(0, 0, 15, 3)
        self.bullet_rect.midleft = self.ship_rect.midright

    def update(self):
        self.bullet_rect.x += 5

    def draw_bullet(self):
        pygame.draw.rect(self.screen, (60, 60, 60), self.bullet_rect)


if __name__ == '__main__':
    game = Game()
    game.game_loop()

