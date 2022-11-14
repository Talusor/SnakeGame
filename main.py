from PlayableGame import PlayableGame
from SimGame import SimGame
import arcade

def main():
    game = PlayableGame(640, 480, "Snake Game", record=True)
    # game = SimGame("record.simData", game_speed=30)
    arcade.enable_timings()
    arcade.run()

if __name__ == "__main__":
    main()