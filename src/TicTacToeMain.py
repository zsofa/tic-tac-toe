import os
from GameGenerator import GameGenerator
from GameProcessor import GameProcessor

def clear_folders():
    """Deletes all files in the games, imgProcessing, and results folders."""
    folders = ["games", "imgProcessing", "results"]
    for folder in folders:
        if os.path.exists(folder):
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"All files in the '{folder}' folder have been deleted.")
        else:
            print(f"The '{folder}' folder does not exist.")

def generate_games():
    while True:
        try:
            num_games = int(input("Enter the number of games to generate (1-100): "))
            if 1 <= num_games <= 100:
                break
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    generator = GameGenerator()
    games_folder = "games"
    os.makedirs(games_folder, exist_ok=True)

    for i in range(1, num_games + 1):
        generator.simulate_game()

    print(f"Generated {num_games} games in the 'games' folder.")
    return num_games

def analyze_games(max_games):
    print("Starting game analysis...")
    processor = GameProcessor(games_folder="games",
                               results_folder="results",
                               image_processing_folder="imgProcessing")

    results_file_path = os.path.join("results", "result.svc")
    os.makedirs("results", exist_ok=True)

    with open(results_file_path, 'w') as results_file:
        results_file.write("Game Name,Status\n")
        for i in range(1, max_games + 1):
            game_file = f"game{i}.png"
            if os.path.exists(os.path.join("games", game_file)):
                print(f"Processing {game_file}...")
                status = processor.analyze_game(game_file)
                print(f"Status for {game_file}: {status}")
                results_file.write(f"{game_file},{status}\n")
            else:
                print(f"File {game_file} does not exist.")

    print(f"Analysis results saved to {results_file_path}.")

def main():
    while True:
        folders = ["games", "imgProcessing", "results"]
        folders_not_empty = any(os.listdir(folder) for folder in folders if os.path.exists(folder))

        if folders_not_empty:
            print("Demo version limitation: If there are existing files in 'games', 'imgProcessing', or 'results', you must clear them first.")
            action = input("Would you like to clear the folders? (c): ").strip().lower()
            if action == "c":
                clear_folders()
                print("Folders cleared. Please run the program again to generate new games.")
                break
            else:
                print("Invalid option. Please type 'c' to clear the folders.")
                continue

        action = input("Would you like to generate new games? (g): ").strip().lower()
        if action == "g":
            max_games = generate_games()
            analyze_games(max_games)
            break
        else:
            print("Invalid option. Please type 'g' to generate.")

if __name__ == "__main__":
    main()
