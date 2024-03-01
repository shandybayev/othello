import time
import game

class zzs24(game.Player):
    def __init__(self, time_limit_ms=100):
        super().__init__()
        self.time_limit_ms = time_limit_ms

    def choose_move(self, state):
        start_time = time.time()
        best_move = None

        depth = 1
        try:
            while True:
                _, move = self.alpha_beta(state, depth, start_time, True)
                best_move = move
                depth += 1
        except TimeoutError:
            pass

        return best_move

    def alpha_beta(self, state, depth, start_time, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if time.time() - start_time > self.time_limit_ms / 1000:
            raise TimeoutError("Time limit exceeded")

        if depth == 0 or state.game_over():
            return state.score(), None

        moves = state.generateMoves()
        best_value = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for move in moves:
            new_state = state.applyMoveCloning(move)
            value, _ = self.alpha_beta(new_state, depth - 1, start_time, not maximizing_player, alpha, beta)
            
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
