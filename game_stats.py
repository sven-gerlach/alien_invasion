class GameStats:
    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # start Alien Invasion in an active state
        self.game_active = False
        self.game_paused = False

        # player name, high score, and difficulty
        self.high_score = 0
        self.player_name = ''
        self.difficulty_level = ''

    def reset_stats(self):
        """Initialise statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

