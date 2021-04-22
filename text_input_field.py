import pygame


class InputBox:
    """A class to create a text-based input field so that players can record their name"""

    def __init__(self, x, y, w, h, welcome_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.welcome_text = welcome_text
        self.text = self.welcome_text
        self.font = pygame.font.Font(None, 48)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.text = ''
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
            self.txt_surface = self.font.render(self.text, True, self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        text_width = self.txt_surface.get_width() + 10
        if text_width > self.rect.width:
            self.rect.inflate_ip(text_width - self.rect.w, 0)

        """
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        """

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.left + 5, self.rect.y + 10))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_player_name(self):
        return self.text

    def reset_text_input_field(self):
        self.text = self.welcome_text
        self.txt_surface = self.font.render(self.text, True, self.color)