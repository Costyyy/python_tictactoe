import pygame as pg
import numpy as np
from random import randrange
from button import Button
from minimax import MiniMax, check_end


class TicTacToe:

    def __init__(self, table_size=3):
        self.table_size = table_size
        self.table = np.zeros(shape=(table_size, table_size), dtype='int')
        self.menu_buttons = []
        self.game_buttons = []
        # self.table[0] = 1
        # self.table[-1] = 2
        pg.init()
        self.alg = MiniMax()
        self.smallfont = pg.font.SysFont('Comic Sans MS', 35)
        self.s_width = 800
        self.s_height = 600
        self.screen = pg.display.set_mode((self.s_width, self.s_height))
        self.clock = pg.time.Clock()
        self.tile_size = 100
        self.width, self.height = self.table_size * self.tile_size, self.table_size * self.tile_size
        self.background = pg.Surface((self.s_width, self.s_height))
        self.button_surface_size = (self.s_width / 4, self.s_height / 4)
        self.button_surface = pg.Surface(self.button_surface_size)
        self.offset = ((self.s_width - self.width) / 2, (self.s_height - self.height) / 2)
        self.b_offset = ((self.s_width - self.s_width / 4) / 2, (self.s_height - self.s_height / 8) / 1.1)
        self.current_player = 2
        self.human_player = 2
        self.ai_player = 1
        self.gameover = False
        self.winner = 0
        self.difficulty = 0
        self.board_tiles = []
        self.score = {1: 0, 2: 0}
        self.init_board()

    def init_board(self):
        for y in range(0, self.height, self.tile_size):
            temp = []
            for x in range(0, self.width, self.tile_size):
                temp += [[(x, y), 0]]
            self.board_tiles.append(temp)
        self.update_board()

    def update_board(self):
        for i in range(self.table_size):
            for j in range(self.table_size):
                self.board_tiles[i][j][1] = self.table[i, j]

    def draw_board(self):
        self.background.fill((0, 0, 0))
        self.button_surface.fill((0, 0, 0))
        for line in self.board_tiles:
            for pos, _ in line:
                x, y = pos
                rect = (x, y, self.tile_size, self.tile_size)
                pg.draw.rect(self.background, 'WHITE', rect, width=1)
        if self.gameover:
            score_text = self.smallfont.render(f'H:{self.score[self.human_player]} - C:{self.score[self.ai_player]}',
                                               True, (252, 3, 57))
            self.button_surface.blit(score_text, (0, 0))
            for button in self.game_buttons:
                if button.name == 'replay_button':
                    pg.draw.rect(self.button_surface,
                                 rect=((button.pos_x, button.pos_y), (button.width, button.height)),
                                 color='WHITE')
                    text = self.smallfont.render(button.text, True, (252, 3, 57))
                    self.button_surface.blit(text, (button.pos_x + button.width / 8, button.pos_y))

    def draw_pieces(self):
        for i in range(self.table_size):
            for j in range(self.table_size):
                pos, piece = self.board_tiles[i][j]
                x, y = pos
                if piece == 2:
                    pg.draw.line(self.background, color='WHITE',
                                 start_pos=(x + self.tile_size / 5, y + self.tile_size / 5),
                                 end_pos=(
                                     x + self.tile_size - self.tile_size / 5, y + self.tile_size - self.tile_size / 5),
                                 width=4)
                    pg.draw.line(self.background, color='WHITE',
                                 start_pos=(x - self.tile_size / 5 + self.tile_size, y + self.tile_size / 5),
                                 end_pos=(
                                     x + self.tile_size / 5, y + self.tile_size - self.tile_size / 5),
                                 width=4)
                elif piece == 1:
                    pg.draw.ellipse(self.background, color='WHITE',
                                    rect=((x + self.tile_size / 4, y + self.tile_size / 4),
                                          (self.tile_size / 2, self.tile_size / 2)), width=4)

    def check_box(self, box_pos, click_pos):
        x1, y1 = box_pos
        x2, y2 = x1 + self.tile_size, y1 + self.tile_size
        x, y = click_pos
        if x1 < x < x2 and y1 < y < y2:
            return True
        else:
            return False

    def mouse_select(self, pos):
        for i in range(self.table_size):
            for j in range(self.table_size):
                box_pos, piece = self.board_tiles[i][j]
                if self.check_box(box_pos, pos):
                    return i, j
        return None

    def process_click(self, cell):
        if self.human_player == self.current_player:
            i, j = cell
            if self.table[i, j] == 0:
                self.table[i, j] = self.human_player
                self.current_player = self.ai_player

    def init_menu_buttons(self):
        button_width = 150
        button_height = 50
        button_pos_x = self.s_width / 2 - button_width / 2
        button_pos_y = self.s_height / 2.5 - button_height / 2
        self.menu_buttons.append(Button(button_pos_x, button_pos_y, button_width, button_height, 'play_button', 'PLAY'))

        button_width = 200
        button_pos_x = self.s_width / 1.2 - button_width / 2

        self.menu_buttons.append(Button(button_pos_x, button_pos_y, button_width, button_height, 'dif1_button', 'EASY'))
        button_pos_y += button_height * 1.5
        self.menu_buttons.append(
            Button(button_pos_x, button_pos_y, button_width, button_height, 'dif2_button', 'NORMAL'))
        button_pos_y += button_height * 1.5
        self.menu_buttons.append(
            Button(button_pos_x, button_pos_y, button_width, button_height, 'dif3_button', 'HARD'))

    def init_game_buttons(self):
        button_width = 150
        button_height = 50
        button_pos_x = self.button_surface_size[0] / 2 - button_width / 2
        button_pos_y = self.button_surface_size[1] / 2 - button_height / 2
        self.game_buttons.append(
            Button(button_pos_x, button_pos_y, button_width, button_height, 'replay_button', 'REPLAY'))

    def draw_menu(self):
        dif_buttons = {0: 'dif1_button', 1: 'dif2_button', 2: 'dif3_button'}
        for button in self.menu_buttons:
            pg.draw.rect(self.background, rect=((button.pos_x, button.pos_y), (button.width, button.height)),
                         color='WHITE')
            text = self.smallfont.render(button.text, True, (252, 3, 57))
            self.background.blit(text, (button.pos_x + (button.width / 2 - text.get_width() / 2), button.pos_y))
            if dif_buttons[self.difficulty] == button.name:
                pg.draw.rect(self.background, rect=((button.pos_x, button.pos_y), (button.width, button.height)),
                             color='GREEN', width=3)

    def menu(self):
        self.init_menu_buttons()
        while True:
            self.draw_menu()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    pos = pos[0], pos[1]
                    for button in self.menu_buttons:
                        if button.check_pressed(pos):
                            if button.name == 'play_button':
                                self.run()
                                return
                            if button.name == 'dif1_button':
                                self.difficulty = 0
                            elif button.name == 'dif2_button':
                                self.difficulty = 1
                            elif button.name == 'dif3_button':
                                self.difficulty = 2
                    # click buttons
            self.screen.fill((60, 70, 90))
            self.screen.blit(self.background, (0, 0))
            pg.display.flip()
            self.clock.tick(30)

    def easy_ai(self):
        while True:
            r_i = randrange(0, self.table_size)
            r_j = randrange(0, self.table_size)
            if self.table[r_i, r_j] == 0:
                self.table[r_i, r_j] = self.ai_player
                self.current_player = self.human_player
                break

    def hard_ai(self):
        _, self.table = self.alg.minimax(self.table, 0, False, -float('inf'), float('inf'))
        self.current_player = self.human_player

    def run(self):
        game_exit = False
        self.background = pg.Surface((self.width, self.height))
        self.init_game_buttons()
        ai_dif_turn = 0
        while not game_exit:
            self.update_board()
            self.draw_board()
            self.draw_pieces()
            result = check_end(self.table)
            if not self.gameover:
                if result == self.ai_player:
                    self.score[self.ai_player] += 1
                    self.gameover = True
                elif result == self.human_player:
                    self.score[self.human_player] += 1
                    self.gameover = True
                elif result == -1:
                    self.score[self.ai_player] += 1
                    self.score[self.human_player] += 1
                    self.gameover = True
            if self.current_player == self.ai_player and not self.gameover:
                # do AI thinking
                ai_dif_turn = (ai_dif_turn + 1) % 2
                if self.difficulty == 0:
                    self.easy_ai()
                elif self.difficulty == 1:
                    if ai_dif_turn == 0:
                        self.easy_ai()
                    else:
                        self.hard_ai()
                elif self.difficulty == 2:
                    self.hard_ai()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_exit = True
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    pos_offset = pos[0] - self.offset[0], pos[1] - self.offset[1]
                    pos_b_offset = pos[0] - self.b_offset[0], pos[1] - self.b_offset[1]
                    cell = self.mouse_select(pos_offset)
                    if cell is not None and not self.gameover:
                        # print(cell)
                        self.process_click(cell)

                        # if self.check_final() != 0:
                        #     game_exit = True
                    # check for replay button press
                    if self.gameover:
                        for button in self.game_buttons:
                            if button.name == 'replay_button' and button.check_pressed(pos_b_offset):
                                self.gameover = False
                                self.table = np.zeros(shape=(self.table_size, self.table_size), dtype='int')
            self.screen.fill((60, 70, 90))
            self.screen.blit(self.background, self.offset)
            self.screen.blit(self.button_surface, self.b_offset)
            pg.display.flip()
            self.clock.tick(30)
        pg.quit()


def main():
    obj = TicTacToe()
    obj.menu()


if __name__ == '__main__':
    main()
