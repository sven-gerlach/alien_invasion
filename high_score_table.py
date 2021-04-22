import pandas as pd
import pygame


class HighScoreTable:

    def __init__(self, ai_game):
        # game parameters needed to draw relevant high-score table
        self.screen = ai_game.screen
        self.difficulty = ai_game.stats.difficulty_level

        # high score data dictionaries
        self.high_score_txt_dict = {}
        self.high_score_table_dict = {'Player': [], 'Difficulty': [], 'High Score': []}
        self.high_score_table_dict_filtered = {}

        # text settings
        self.text_colour = (0, 0, 0)
        self.box_colour = (230, 230, 230)
        self.font_title = pygame.font.SysFont(None, 40, True)
        self.font_body = pygame.font.SysFont(None, 30)

        # draw table
        self.open_high_scores_file()
        self.reformat_dict()
        self.create_pandas()
        self.draw_high_score_table()

    def open_high_scores_file(self):
        # opening and reading file
        with open('high_scores/high_scores.txt') as fo:
            file_content = fo.readlines()

        # compiling file content and storing it in dictionary
        for line in file_content:
            player_name, difficulty, high_score = line.strip().split(';')
            if player_name in self.high_score_txt_dict:
                self.high_score_txt_dict[player_name][difficulty] = int(high_score)
            else:
                self.high_score_txt_dict[player_name] = dict({difficulty: int(high_score)})

    def reformat_dict(self):
        # reformat dictionary to make it usable for pandas
        for player_name, values in self.high_score_txt_dict.items():
            for difficulty, high_score in values.items():
                self.high_score_table_dict['Player'].append(player_name)
                self.high_score_table_dict['Difficulty'].append(difficulty)
                self.high_score_table_dict['High Score'].append(high_score)

    def create_pandas(self):
        # length of complete data set from 1 to n
        index_range = list(range(1, len(self.high_score_table_dict['Player']) + 1))

        # create pandas data frame of entire data set with row index from 1 to n
        df = pd.DataFrame(self.high_score_table_dict, index=index_range)

        # sorting the data frame (in place) by score column
        df.sort_values(by='High Score', ascending=False, inplace=True, ignore_index=True)

        # renaming index to start from 1
        df.rename(lambda x: x + 1, inplace=True)

        if self.difficulty:
            # filter for difficulty
            df_filtered = df[df['Difficulty'] == self.difficulty]
            # convert from data frame to dictionary
            self.high_score_table_dict_filtered = df_filtered.head(10).to_dict('list')

        else:
            # if no difficulty selected then don't filter
            self.high_score_table_dict_filtered = df.head(10)

    def draw_high_score_table(self):
        column_counter = 320
        for key, values in self.high_score_table_dict_filtered.items():
            column_counter += 200
            row_counter = 450

            # blitting column titles
            text_surface = self.font_title.render(str(key), True, self.text_colour, self.box_colour)
            text_rect = text_surface.get_rect(center=(column_counter, row_counter))
            self.screen.blit(text_surface, text_rect)
            row_counter += 30
            for value in values:
                # blitting column data
                text_surface = self.font_body.render(str(value), True, self.text_colour, self.box_colour)
                text_rect = text_surface.get_rect(center=(column_counter, row_counter))
                self.screen.blit(text_surface, text_rect)
                row_counter += 30
