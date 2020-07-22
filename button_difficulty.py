import pygame.font

class ButtonDifficulty:
    def __init__(self, ai_game, difficulty, button_color, coordinates):
        """Initialise button attributes for range of difficulty level buttons"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = button_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx, self.rect.centery = coordinates

        # the button message needs to be prepped only once
        self._prep_msg(difficulty)

    def update_button_color(self, button_color, difficulty):
        self.button_color = button_color
        self._prep_msg(difficulty)

    def _prep_msg(self, difficulty):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(difficulty, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then raw message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
