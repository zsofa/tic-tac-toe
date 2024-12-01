from GameGenerator import GameGenerator
from GameProcessor import GameProcessor
if __name__ == "__main__":

    print("Starting the game")
    # Generate game
    generator = GameGenerator()
    winner = generator.simulate_game()

    # Process moves
    processor = GameProcessor(generator.get_moves_log(), winner)
    processor.analyze_game()