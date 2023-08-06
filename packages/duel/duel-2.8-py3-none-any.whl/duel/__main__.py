import duel.window
import duel.gameEngine
from duel.audioEngine import AudioEngine


def main():
    gameEngine.mainMenu(window.startScreen(), AudioEngine())

if __name__ == '__main__':
    main()

