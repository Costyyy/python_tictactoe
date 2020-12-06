import numpy as np


def check_end(board):
    cells = ((0, 0), (0, 1), (0, 2), (1, 0), (2, 0))
    for player in (1, 2):
        for cell in cells:
            i, j = cell
            if (board[i] == player).all():
                return player

            if (board.transpose()[j] == player).all():
                return player

            if (board.diagonal() == player).all():
                return player

            if (np.fliplr(board).diagonal() == player).all():
                return player
    if not np.any(board == 0):
        return -1
    return False


def evaluate(board, depth):
    res = check_end(board)
    if res == 2:
        return 10 - depth
    elif res == 1:
        return depth - 10

    return 0


class MiniMax:

    def get_moves(self, board, player):
        res = []
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    new_board = board.copy()
                    new_board[i, j] = player
                    res.append(new_board)
        return res

    def minimax(self, board, depth, maximizing, alpha, beta):

        if check_end(board) is not False:
            return evaluate(board, depth), board

        if maximizing:
            best_val = -float('inf')
            best_move = None
            for move in self.get_moves(board, 2):
                value = self.minimax(move, depth + 1, False, alpha, beta)[0]
                best_val = max(best_val, value)
                if best_val < value:
                    best_val = value
                    best_move = move
                if best_val >= beta:
                    break
                if best_val > alpha:
                    alpha = best_val
            return best_val, best_move

        else:
            best_val = float('inf')
            best_move = None
            for move in self.get_moves(board, 1):
                value = self.minimax(move, depth + 1, True, alpha, beta)[0]
                if best_val > value:
                    best_val = value
                    best_move = move
                if best_val <= alpha:
                    break
                if best_val < beta:
                    beta = best_val
            return best_val, best_move
