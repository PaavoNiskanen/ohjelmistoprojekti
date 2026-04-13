import pygame
from States.GameStateManager import GameStateManager
from States.MainMenuState import MainMenuState

def main():
    pygame.init()

    manager = GameStateManager(MainMenuState(None))

    manager.run()

if __name__ == "__main__":
<<<<<<< HEAD
    
    main()wd
=======
    main()
>>>>>>> e9524f2544706ff13f5d52d371a8291caddfe43c
