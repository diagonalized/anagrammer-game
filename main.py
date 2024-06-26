from wordfinder import WordFinder
from game.game import Game


def main():
    """ TESTING TITLE SCREEN + STATE MANAGER """
    wf = WordFinder()

    game = Game(wf)

    game.game_loop()


if __name__ == "__main__":
    main()
