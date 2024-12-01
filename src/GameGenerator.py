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
        self.moves_log = []  # store moves for processing
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
        offset = int(20 * random.uniform(0.8, 1.2))
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)
        top_left = (start_x * cell_width + offset + offset_x, start_y * cell_width + offset + offset_y)
        bottom_right = ((start_x + 1) * cell_width - offset + offset_x, (start_y + 1) * cell_width - offset + offset_y)
        top_right = ((start_x + 1) * cell_width - offset + offset_x, start_y * cell_width + offset + offset_y)
        bottom_left = (start_x * cell_width + offset + offset_x, (start_y + 1) * cell_width - offset + offset_y)
        cv2.line(self.img, top_left, bottom_right, self.GRID_COLOR, self.THICKNESS)
        cv2.line(self.img, top_right, bottom_left, self.GRID_COLOR, self.THICKNESS)

    def draw_o(self, cell):
        start_x, start_y = cell
        cell_width = self.WIDTH // 3
        center = (
            start_x * cell_width + cell_width // 2 + random.randint(-10, 10),
            start_y * cell_width + cell_width // 2 + random.randint(-10, 10),
        )
        radius = int((cell_width // 3 - 10) * random.uniform(0.8, 1.2))
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
        return None

    def save_image(self):
        file_index = 1
        while os.path.exists(f"{self.games_folder}/game{file_index}.png"):
            file_index += 1
        file_name = f"{self.games_folder}/game{file_index}.png"
        cv2.imwrite(file_name, self.img)
        return file_name

    def simulate_game(self):
        players = ["X", "O"]
        turn = 0
        self.draw_grid()

        while True:
            empty_cells = [(x, y) for y in range(3) for x in range(3) if self.board[y][x] == ""]
            if not empty_cells:
                break

            position = random.choice(empty_cells)
            player = players[turn % 2]
            self.moves_log.append((player, position))
            self.board[position[1]][position[0]] = player

            if player == "X":
                self.draw_x(position)
            else:
                self.draw_o(position)

            cv2.imshow("Tic Tac Toe", self.img)
            cv2.waitKey(1000)

            if self.check_winner():
                break

            turn += 1

        winner = self.check_winner()
        saved_file = self.save_image()
        print(f"Game saved as {saved_file}")
        return winner

    def get_moves_log(self):
        return self.moves_log
