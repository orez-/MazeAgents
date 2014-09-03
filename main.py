import agent.right_agent as right
import board.labyrinth as labyrinth
import game


if __name__ == "__main__":
    game.Game(right.RightAgent, labyrinth.CirclesLabyrinth, 2, 56, 56).game_loop()
