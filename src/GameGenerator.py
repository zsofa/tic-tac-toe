import os
import numpy as np
import cv2
import random

class GameGenerator:
    def __init__(self):
        self.WIDTH = 300
        self.HEIGHT = 300
        self.GRID_COLOR = (0, 0, 0)
        self.THICKNESS = 3
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.img = np.ones((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8) * 255
        self.games_folder = "games"
        os.makedirs(self.games_folder, exist_ok=True)

    def draw_grid(self):
        cv2.line(self.img, (self.WIDTH // 3, 0), (self.WIDTH // 3, self.HEIGHT), self.GRID_COLOR, self.THICKNESS)
        cv2.line(self.img, (2 * self.WIDTH // 3, 0), (2 * self.WIDTH // 3, self.HEIGHT), self.GRID_COLOR, self.THICKNESS)
        cv2.line(self.img, (0, self.HEIGHT // 3), (self.WIDTH, self.HEIGHT // 3), self.GRID_COLOR, self.THICKNESS)
        cv2.line(self.img, (0, 2 * self.HEIGHT // 3), (self.WIDTH, 2 * self.HEIGHT // 3), self.GRID_COLOR, self.THICKNESS)
        cv2.rectangle(self.img, (0, 0), (self.WIDTH - 1, self.HEIGHT - 1), self.GRID_COLOR, self.THICKNESS)

    def draw_x(self, cell):
        start_x, start_y = cell
        cell_width = self.WIDTH // 3
        offset = int(0.1 * cell_width)

        x1, y1 = (start_x * cell_width + offset + random.randint(0, offset),
                  start_y * cell_width + offset + random.randint(0, offset))
        x2, y2 = ((start_x + 1) * cell_width - offset - random.randint(0, offset),
                  (start_y + 1) * cell_width - offset - random.randint(0, offset))
        x3, y3 = ((start_x + 1) * cell_width - offset - random.randint(0, offset),
                  start_y * cell_width + offset + random.randint(0, offset))
        x4, y4 = (start_x * cell_width + offset + random.randint(0, offset),
                  (start_y + 1) * cell_width - offset - random.randint(0, offset))

        cv2.line(self.img, (x1, y1), (x2, y2), self.GRID_COLOR, self.THICKNESS)
        cv2.line(self.img, (x3, y3), (x4, y4), self.GRID_COLOR, self.THICKNESS)

    def draw_o(self, cell):
        start_x, start_y = cell
        cell_width = self.WIDTH // 3
        center = (start_x * cell_width + cell_width // 2 + random.randint(-10, 10),
                  start_y * cell_width + cell_width // 2 + random.randint(-10, 10))
        radius = cell_width // 3 - 10 + random.randint(-5, 5)
        cv2.circle(self.img, center, radius, self.GRID_COLOR, self.THICKNESS)

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.board[0][2]

        if all(self.board[y][x] != "" for y in range(3) for x in range(3)):
            return "Draw"

        return None

    def save_image(self, positions):
        file_index = 1
        while os.path.exists(f"{self.games_folder}/game{file_index}.png"):
            file_index += 1
        file_name = f"{self.games_folder}/game{file_index}.png"
        cv2.imwrite(file_name, self.img)

        result_file = f"{self.games_folder}/game{file_index}.csv"
        with open(result_file, 'w') as f:
            for position, value in positions.items():
                f.write(f"{position},{value}\n")

        return file_name, result_file

    def simulate_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.img = np.ones((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8) * 255

        players = ["X", "O"]
        self.draw_grid()
        positions = {}
        current_player = random.choice(players)

        while True:
            empty_cells = [(x, y) for y in range(3) for x in range(3) if self.board[y][x] == ""]
            if not empty_cells:
                break

            cell = random.choice(empty_cells)
            self.board[cell[1]][cell[0]] = current_player
            pos_key = ["top", "middle", "bottom"][cell[1]] + "-" + ["left", "center", "right"][cell[0]]
            positions[pos_key] = current_player

            if current_player == "X":
                self.draw_x(cell)
            else:
                self.draw_o(cell)

            winner = self.check_winner()
            if winner:
                if winner == "Draw":
                    print("Game ended in a draw.")
                else:
                    print(f"Player {winner} wins!")
                break

            current_player = "O" if current_player == "X" else "X"

        for y in range(3):
            for x in range(3):
                if self.board[y][x] == "":
                    pos_key = ["top", "middle", "bottom"][y] + "-" + ["left", "center", "right"][x]
                    positions[pos_key] = "empty"

        return self.save_image(positions)
