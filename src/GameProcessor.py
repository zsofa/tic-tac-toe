class GameProcessor:
    def __init__(self, moves_log, winner):
        self.moves_log = moves_log
        self.winner = winner
        self.positions = {
            (0, 0): "top-left",
            (1, 0): "top-center",
            (2, 0): "top-right",
            (0, 1): "middle-left",
            (1, 1): "center",
            (2, 1): "middle-right",
            (0, 2): "bottom-left",
            (1, 2): "bottom-center",
            (2, 2): "bottom-right",
        }

    def analyze_game(self, step_by_step=False):
        for i, (player, position) in enumerate(self.moves_log, 1):
            pos_description = self.positions[position]
            print(f"Step {i}: Player {player} placed in the {pos_description}.")
            if step_by_step:
                input("Press Enter to see the next step...")

        if self.winner:
            print(f"The winner is {self.winner}!")
        else:
            print("The game is a tie!")