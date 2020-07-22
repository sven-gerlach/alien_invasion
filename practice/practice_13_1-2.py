import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        self.figure = Image(self)

    def run_game(self):
        a = True
        while a:
            self._check_game()
            self._update_screen()

    def _check_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        self.screen.fill((0, 0, 255))
        self.screen.blit(self.figure.image, self.figure.image_rect)
        pygame.display.flip()

class Image:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load('images/ship.bmp')
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.screen_rect.center


if __name__ == '__main__':
    simple_game = Game()
    simple_game.run_game()


"""
import sys, pygame
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("images/ship.bmp")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
"""