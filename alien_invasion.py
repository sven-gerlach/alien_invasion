"""Arcade Game: Alien Invasion"""
import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from button_difficulty import ButtonDifficulty
from text_input_field import InputBox
from high_score_table import HighScoreTable
from button_generic import ButtonGeneric


class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion", 'AI')

        # instantiate buttons
        self.instantiate_buttons()

        # create an instance to store game statistics, create a scoreboard, and high score table
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def instantiate_buttons(self):
        self.play_button = Button(self, "Let's Play!")
        self.button_easy_difficulty = ButtonDifficulty(self, 'Easy', (128, 128, 128), (self.settings.screen_width
                                                                                       * 1 / 4,
                                                                                       self.settings.screen_height *
                                                                                       1 / 4))
        self.button_medium_difficulty = ButtonDifficulty(self, 'Medium', (128, 128, 128), (self.settings.screen_width
                                                                                           * 2 / 4,
                                                                                           self.settings.screen_height *
                                                                                           1 / 4))
        self.button_hard_difficulty = ButtonDifficulty(self, 'Hard', (128, 128, 128),
                                                       (self.settings.screen_width * 3 / 4,
                                                        self.settings.screen_height *
                                                        1 / 4))
        self.text_input_field = InputBox(self.play_button.rect.left, self.settings.screen_height * 1 / 8, 200, 50,
                                         'Enter Name')
        self.button_main_menue = ButtonGeneric(self, (self.settings.screen_width / 2 - 300,
                                                      self.settings.screen_height / 2), (200, 50), (128, 128, 128),
                                               'Main Menu', (255, 255, 255), 48)
        self.button_continue = ButtonGeneric(self, (self.settings.screen_width / 2 + 100, self.settings.screen_height
                                                    / 2), (200, 50), (128, 128, 128), 'Continue', (255, 255, 255), 48)
        self.button_exit = ButtonGeneric(self, (self.settings.screen_width / 2 - 100, self.settings.screen_height *
                                                9/10), (200, 50), (255, 0, 0), 'Exit', (255, 255, 255), 48)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # watch for keyboard and mouse events.
            self._check_events()
            if self.stats.game_active and not self.stats.game_paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to key strokes and mouse events"""
        for event in pygame.event.get():
            # pass event to text input button
            self.text_input_field.handle_event(event)

            # test for various key and mouse events
            if event.type == pygame.QUIT:
                self.store_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.stats.game_active:
                    self._check_play_button(mouse_pos)
                    self._check_difficulty_button(mouse_pos)
                    self._check_exit_button(mouse_pos)
                if self.stats.game_active and self.stats.game_paused:
                    self._check_main_menu_button(mouse_pos)
                    self._check_continue_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and self.text_input_field.text != 'Enter Name' and self.stats.difficulty_level:
            self.settings.initialise_dynamic_settings()
            self._start_game()

            # reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self._create_fleet()

            # get player name and call high-score
            self.retrieve_high_score()

    def _check_difficulty_button(self, mouse_pos):
        """Highlight button that has been selected in a darker colour"""
        if self.button_easy_difficulty.rect.collidepoint(mouse_pos):
            self._button_easy()
            self.stats.difficulty_level = 'Easy'
        elif self.button_medium_difficulty.rect.collidepoint(mouse_pos):
            self._button_medium()
            self.stats.difficulty_level = 'Medium'
        elif self.button_hard_difficulty.rect.collidepoint(mouse_pos):
            self._button_hard()
            self.stats.difficulty_level = 'Hard'

    def _check_exit_button(self, mouse_pos):
        if self.button_exit.rect.collidepoint(mouse_pos):
            self.store_high_score()
            sys.exit()

    def _check_main_menu_button(self, mouse_pos):
        if self.button_main_menue.rect.collidepoint(mouse_pos):
            self.stats.game_active = not self.stats.game_active
            self.stats.game_paused = not self.stats.game_paused

    def _check_continue_button(self, mouse_pos):
        if self.button_continue.rect.collidepoint(mouse_pos):
            self.stats.game_paused = not self.stats.game_paused
            pygame.mouse.set_visible(not pygame.mouse.get_visible())

    def retrieve_high_score(self):
        """Reading out high score file for player name"""
        # obtain player name and store in game stats
        self.stats.player_name = self.text_input_field.get_player_name()

        # open high score file
        with open('high_scores/high_scores.txt') as fo:
            high_scores = fo.readlines()

        # build dictionary from saved txt data
        self.high_scores_dict = dict()
        if high_scores:
            for line in high_scores:
                player, difficulty, score = line.strip().split(';')
                if player in self.high_scores_dict:
                    self.high_scores_dict[player][difficulty] = score
                else:
                    self.high_scores_dict[player] = dict({difficulty: score})

        # search for player name and difficulty; if found, set high-score in game stats
        try:
            self.stats.high_score = int(self.high_scores_dict[self.stats.player_name][self.stats.difficulty_level])

        except KeyError:
            pass

        else:
            self.sb.prep_high_score()

    def store_high_score(self):
        """store player name and high-score in txt file"""

        # update high score dictionary with player name and high_score
        if self.stats.high_score > 0:
            try:
                if self.stats.player_name in self.high_scores_dict:
                    self.high_scores_dict[self.stats.player_name][self.stats.difficulty_level] = self.stats.high_score
                else:
                    self.high_scores_dict[self.stats.player_name] = dict({self.stats.difficulty_level: self.stats.high_score})

            except AttributeError:
                pass

            # write high score dictionary to txt file
            try:
                with open('high_scores/high_scores.txt', 'w') as fo:
                    for player_name, values in self.high_scores_dict.items():
                        for difficulty, score in values.items():
                            fo.writelines(f'{player_name};{difficulty};{score}\n')

            except AttributeError:
                pass

    def _button_easy(self):
        self.button_easy_difficulty.update_button_color((63, 176, 20), 'Easy')
        self.button_medium_difficulty.update_button_color((128, 128, 128), 'Medium')
        self.button_hard_difficulty.update_button_color((128, 128, 128), 'Hard')
        self.settings.speedup_scale = 1.1

    def _button_medium(self):
        self.button_easy_difficulty.update_button_color((128, 128, 128), 'Easy')
        self.button_medium_difficulty.update_button_color((244, 97, 8), 'Medium')
        self.button_hard_difficulty.update_button_color((128, 128, 128), 'Hard')
        self.settings.speedup_scale = 1.2

    def _button_hard(self):
        self.button_easy_difficulty.update_button_color((128, 128, 128), 'Easy')
        self.button_medium_difficulty.update_button_color((128, 128, 128), 'Medium')
        self.button_hard_difficulty.update_button_color((215, 0, 5), 'Hard')
        self.settings.speedup_scale = 1.3

    def _start_game(self):
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # hide the moues cursor
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.store_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_ESCAPE and self.stats.game_active:
            self.stats.game_paused = not self.stats.game_paused
            pygame.mouse.set_visible(not pygame.mouse.get_visible())

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old ones"""

        # update bullet positions
        self.bullets.update()

        # get rid of bullets that have disappeared off the top of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for any bullets that have hit aliens.
        # if so, get rid of the bullet and the alien.
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that collided
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens,
                                                True,
                                                True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of
        all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        """create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # determine the number of aliens that fit in one row
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows that fit onto the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) -
                             ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height * 1.5) + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            self.store_high_score()
            self.aliens.empty()
            self.text_input_field.reset_text_input_field()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _draw_buttons(self):
        self.play_button.draw_button()
        self.button_easy_difficulty.draw_button()
        self.button_medium_difficulty.draw_button()
        self.button_hard_difficulty.draw_button()
        self.text_input_field.draw(self.screen)
        self.text_input_field.update()
        self.button_exit.draw_button()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        if self.stats.game_active:
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)

            # Draw the score information
            self.sb.show_score()

        # draw two buttons, Reset and Continue, when the game is active but paused
        if self.stats.game_active and self.stats.game_paused:
            self.button_main_menue.draw_button()
            self.button_continue.draw_button()

        # draw the play button if the game is inactive
        if not self.stats.game_active:
            self._draw_buttons()
            self.high_score_table = HighScoreTable(self)

        pygame.display.flip()
        self.fpsClock.tick(60)


if __name__ == '__main__':
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()