import duel.window
import duel.gameEngine
from duel.audioEngine import AudioEngine


def main():
    duel.gameEngine.mainMenu(window.startScreen(), AudioEngine())

if __name__ == '__main__':
    main()

