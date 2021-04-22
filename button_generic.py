import pygame


class ButtonGeneric:
    """Class to create generic button"""

    def __init__(self, ai_game, position, size, colour, text, font_colour, font_size):
        # key screen parameters
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set key button parameters
        self.position = position
        self.size = size
        self.colour = colour
        self.text = text
        self.font_colour = font_colour
        self.font_size = font_size

        # initialise font
        self.font = pygame.font.SysFont(None, self.font_size)

        # create button and text image
        self.rect = pygame.Rect(self.position, self.size)
        self._prep_text()

    def _prep_text(self):
        self.text_image = self.font.render(self.text, True, self.font_colour, self.colour)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.colour, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)

