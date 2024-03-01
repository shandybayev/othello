import math
import random
import time

import game

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):        
        # generate the list of moves:
        moves = state.generateMoves()

        if not moves:
            return None

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):
    def choose_move(self, state):
        moves = state.generateMoves()
    
        if not moves:
            return None

        return random.choice(moves)


class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def choose_move(self, state):
        _, move = self.minimax(state, self.depth, True)
        return move
    
    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or state.game_over():
            return state.score(), None

        moves = state.generateMoves()
        if maximizing_player:
            best_value = float('-inf')
            best_move = None
            for move in moves:
                new_state = state.applyMoveCloning(move)
                value, _ = self.minimax(new_state, depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = None
            for move in moves:
                new_state = state.applyMoveCloning(move)
                value, _ = self.minimax(new_state, depth - 1, True)
                if value < best_value:
                    best_value = value
                    best_move = move
            return best_value, best_move


class AlphaBeta(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def choose_move(self, state):
        _, move = self.alpha_beta(state, self.depth, float('-inf'), float('inf'), True)
        return move

    def alpha_beta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.game_over():
            return state.score(), None

        moves = state.generateMoves()
        best_value = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in moves:
            new_state = state.applyMoveCloning(move)
            value, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, not maximizing_player)
            
            if maximizing_player:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)

            if beta <= alpha:
                break

        return best_value, best_move
    