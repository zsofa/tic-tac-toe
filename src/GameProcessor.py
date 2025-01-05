import cv2
import numpy as np
import os

class GameProcessor:
    def __init__(self, games_folder, results_folder, image_processing_folder):
        self.games_folder = games_folder
        self.image_processing_folder = image_processing_folder
        self.results_folder = results_folder
        self.WIDTH = 300
        self.HEIGHT = 300
        os.makedirs(self.results_folder, exist_ok=True)

    def analyze_game(self, game_file):
        img_path = os.path.join(self.games_folder, game_file)
        result_file = os.path.join(self.image_processing_folder, f"processed_{game_file.replace('.png', '.csv')}")
        print(f"Analyzing: {img_path}")

        try:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

            kernel = np.ones((2, 2), np.uint8)
            grid_removed = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

            debug_binary_path = os.path.join(self.image_processing_folder, f"binary_{game_file}")
            cv2.imwrite(debug_binary_path, grid_removed)
            print(f"Binary image saved to {debug_binary_path}")

            contours, _ = cv2.findContours(grid_removed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            positions = {f"{row}-{col}": "empty" for row in ["top", "middle", "bottom"] for col in
                         ["left", "center", "right"]}

            debug_contours_image = img.copy()
            cv2.drawContours(debug_contours_image, contours, -1, (255, 0, 0), 2)
            debug_contours_path = os.path.join(self.image_processing_folder, f"contours_{game_file}")
            cv2.imwrite(debug_contours_path, debug_contours_image)
            print(f"Contours image saved to {debug_contours_path}")

            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w // 2, y + h // 2
                area = cv2.contourArea(cnt)
                aspect_ratio = float(w) / h

                #print(f"Contour: x={x}, y={y}, w={w}, h={h}, area={area}, aspect_ratio={aspect_ratio}")

                if w == self.WIDTH and h == self.HEIGHT:
                    #print(f"Skipping contour at x={x}, y={y} because it covers the full grid.")
                    continue

                row = min(max(cy // (self.HEIGHT // 3), 0), 2)
                col = min(max(cx // (self.WIDTH // 3), 0), 2)

                pos_key = ["top", "middle", "bottom"][row] + "-" + ["left", "center", "right"][col]

                if pos_key == "middle-center":
                    #print(f"Processing potential middle-center contour at x={x}, y={y}.")
                    if area < 50 or area > 6000:
                        #print(f"Skipping contour at x={x}, y={y} for middle-center due to area ({area}).")
                        continue
                    if aspect_ratio < 0.7 or aspect_ratio > 1.3:
                        #print(f"Skipping contour at x={x}, y={y} for middle-center due to aspect ratio ({aspect_ratio:.2f}).")
                        continue

                else:
                    if area < 50 or area > 5000:
                        #print(f"Skipping contour at x={x}, y={y} due to area ({area}).")
                        continue
                    if aspect_ratio < 0.6 or aspect_ratio > 1.5:
                        #print(f"Skipping contour at x={x}, y={y} due to aspect ratio ({aspect_ratio:.2f}).")
                        continue

                if positions[pos_key] != "empty":
                    #print(f"Skipping contour at x={x}, y={y} because position {pos_key} is already occupied.")
                    continue

                circularity = 4 * np.pi * cv2.contourArea(cnt) / (cv2.arcLength(cnt, True) ** 2)
                if circularity > 0.6:
                    positions[pos_key] = "O"
                    #print(f"Detected 'O' at position {pos_key} (circularity: {circularity:.2f})")
                else:
                    positions[pos_key] = "X"
                    #print(f"Detected 'X' at position {pos_key} (circularity: {circularity:.2f})")

            debug_overlay = img.copy()
            for cnt in contours:
                cv2.drawContours(debug_overlay, [cnt], -1, (0, 255, 0), 2)
            debug_overlay_path = os.path.join(self.image_processing_folder, f"overlay_{game_file}")
            cv2.imwrite(debug_overlay_path, debug_overlay)
            print(f"Debug overlay saved to {debug_overlay_path}")

            with open(os.path.join(self.games_folder, game_file.replace('.png', '.csv')), 'r') as f:
                original_positions = {line.split(',')[0]: line.split(',')[1].strip() for line in f.readlines()}

            print("Analyzed positions:")
            print(positions)
            print("Original positions:")
            print(original_positions)

            # Compare positions
            if positions == original_positions:
                analysis_status = "Success"
            else:
                analysis_status = "Failed"

            with open(result_file, 'w') as f:
                f.write("Position,Value\n")
                for position, value in positions.items():
                    f.write(f"{position},{value}\n")
            print(f"Saved analyzed positions to {result_file}")

            return analysis_status

        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            return "Error"
