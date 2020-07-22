import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()

        # initialise the screen surface
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Shooter', 'Shoot')

        # instantiate all classes
        self.settings = Settings(self)
        self.ship = Ship(self)
        self.target = Target(self)
        self.targets = pygame.sprite.Group()
        self.targets.add(self.target)
        self.bullet = Bullet(self)
        self.bullets = pygame.sprite.Group()
        self.play_button = Button(self, 'PLAY?')

    def run_game(self):
        while True:
            self._check_events()
            if self.settings.active_game:
                self.ship.update_ship()
                self._update_bullet()
                self._update_target()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.ship.move_up = True
                if event.key == pygame.K_DOWN:
                    self.ship.move_down = True
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.move_up = False
                if event.key == pygame.K_DOWN:
                    self.ship.move_down = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)

    def _check_play_button(self, mouse_position):
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked and not self.settings.active_game:
            self._game_reset()
            self.settings.increase_speed()

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullet(self):
        # update bullet sprites
        self.bullets.update()

        # remove sprites that have gone off screen
        for bullet in self.bullets.sprites():
            if bullet.rect.left > self.screen.get_rect().right:
                self._target_missed(bullet)

        # check for collision with target
        self._check_bullet_target_collision()

    def _check_bullet_target_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.targets, True, True)
        if not self.targets:
            self.settings.remaining_tries = 3
            self.bullets.empty()
            self.ship.center_ship()
            self.target = Target(self)
            self.targets.add(self.target)
            self.target.center_target()
            self.settings.increase_speed()

    def _target_missed(self, bullet):
        self.bullets.remove(bullet)
        if self.settings.remaining_tries > 0:
            self.settings.remaining_tries -= 1
        else:
            self.settings.active_game = False
            pygame.mouse.set_visible(True)

    def _update_target(self):
        self.targets.update()

    def _game_reset(self):
        # reset game stats
        self.settings.remaining_tries = 3
        self.settings.active_game = True

        # get rid of remaining bullets
        self.bullets.empty()

        # re-center ship and target
        self.ship.center_ship()
        self.target.center_target()

        # reset game speed
        self.settings.initiate_dynamic_settings()

        pygame.mouse.set_visible(False)

    def _update_screen(self):
        self.screen.fill(self.settings.screen_colour)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for target in self.targets.sprites():
            target.draw_target()
        if not self.settings.active_game:
            self.play_button.draw_button()
        pygame.display.flip()


class Ship:
    def __init__(self, ai_game):
        # bring screen into local namespace
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # create image, image_rect, and align image_rect with screen_rect
        self.image = pygame.image.load('/Users/svengerlach/PycharmProjects/AlienInvasion/images/ship.bmp')
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.left = self.rect.width
        self.rect.centery = self.screen_rect.centery

        # movement flags
        self.move_up = False
        self.move_down = False

    def update_ship(self):
        if self.move_up and self.rect.y >= 0:
            self.rect.y -= self.settings.ship_speed
        if self.move_down and self.rect.y <= self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.centery = self.screen_rect.centery


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.ship_rect = ai_game.ship.rect
        self.rect = pygame.Rect((0, 0), self.settings.bullet_size)
        self.rect.midleft = self.ship_rect.midright

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)

    def update(self):
        self.rect.x += self.settings.bullet_speed

class Target(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ship_rect = ai_game.ship.rect
        self.rect = pygame.Rect((0, 0), self.settings.target_size)
        self.rect.centerx = self.screen_rect.right - self.ship_rect.width
        self.rect.centery = self.screen_rect.centery
        self.direction_y = 1

    def update(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_rect.bottom:
            self.direction_y *= -1
        self.rect.centery += self.settings.target_speed * self.direction_y

    def draw_target(self):
        pygame.draw.rect(self.screen, self.settings.target_color, self.rect)

    def center_target(self):
        self.rect.centery = self.screen_rect.centery


class Button:
    def __init__(self, ai_game, message):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.message = message

        # set dimensions and properties of button
        self.width, self.height = self.settings.button_width, self.settings.button_height
        self.button_colour = self.settings.button_color
        self.text_colour = self.settings.text_color
        self.font = pygame.font.SysFont(None, self.settings.font_size, True)

        # positioning the button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # preparing the button message
        self._prepare_message(message)

    def _prepare_message(self, message):
        self.message_image = self.font.render(message, True, self.text_colour, self.button_colour)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)


class Settings:
    def __init__(self, ai_game):
        # screen settings
        self.screen_colour = (230, 230, 230)

        # Game settings
        self.active_game = False
        self.remaining_tries = 3

        # ship settings
        self.ship_speed = 5

        # bullet settings
        self.bullet_size = (8, 2)
        self.bullet_color = (255, 0, 0)
        self.bullet_speed = 10

        # target settings
        self.target_size = (5, 40)
        self.target_color = (0, 0, 255)

        # text box settings
        self.button_width = 16 * 8
        self.button_height = 9 * 8
        self.button_color = (0, 100, 0)
        self.text_color = (0, 255, 0)
        self.font_size = 40

        # dynamic settings
        self.target_speed_increase = 2

    def initiate_dynamic_settings(self):
        self.target_speed = 5

    def increase_speed(self):
        self.target_speed += self.target_speed_increase


if __name__ == '__main__':
    game = Game()
    game.run_game()