import pygame as pg
import numpy as np


class TicTacToe:

    def __init__(self, table_size=3):
        self.table_size = table_size
        self.table = np.zeros(shape=(table_size, table_size), dtype='int')
        self.table[0] = 1
        self.table[-1] = 2
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.tile_size = 100
        self.width, self.height = self.table_size * self.tile_size, self.table_size * self.tile_size
        self.background = pg.Surface((self.width, self.height))
        self.offset = ((800 - self.width) / 2, (600 - self.height) / 2)
        self.current_player = 2
        self.human_player = 2
        self.board_tiles = []
        self.player_colors = {1: 'red', 2: 'green'}
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
        for line in self.board_tiles:
            for pos, _ in line:
                x, y = pos
                rect = (x, y, self.tile_size, self.tile_size)
                pg.draw.rect(self.background, 'WHITE', rect, width=1)

    def run(self):
        game_exit = False
        while not game_exit:
            self.draw_board()
            if self.current_player == 1:
                # do AI thinking
                pass
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_exit = True
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    pos = pos[0] - self.offset[0], pos[1] - self.offset[1]
                    # cell = self.mouse_select(pos)
                    # if cell is not None:
                    #     self.process_click(cell)
                    #     if self.check_final() != 0:
                    #         game_exit = True
            self.screen.fill((60, 70, 90))
            self.screen.blit(self.background, self.offset)
            pg.display.flip()
            self.clock.tick(30)
        pg.quit()


def main():
    obj = TicTacToe()
    obj.run()

main()