from wordfinder.wordfinder import WordFinder
from game.game import Game


def main():
    """ TESTING TITLE SCREEN + STATE MANAGER """
    wf = WordFinder()

    badland = wf.search_by_alphagram("badland")
    anagrams = wf.extend_subanagrams(badland)

    # weird behavior i'll fix tommorow
    # look at TODO in wordfinder.py
    print(badland)
    print(len(badland))
    # however, anagrams are correct
    print(anagrams)
    print(len(anagrams))

    # game looks good tho
    # title is clean as a whistle
    game = Game(wf)

    game.game_loop()


if __name__ == "__main__":
    main()
