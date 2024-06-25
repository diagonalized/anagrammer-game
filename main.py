from wordfinder import WordFinder


def main():
    """ current test for github i come back tmrw """
    wf = WordFinder()

    unique_bingo = wf.search_by_preference(7, 1)

    print(unique_bingo)

    anagrams = wf.extend_subanagrams(unique_bingo)

    print(anagrams)

    # for comparison against other wordfinders

    count = 0
    for length in range(len(unique_bingo[0]), 1, -1):
        for a in anagrams:
            if len(a) == length:
                print(a)
                count += 1
        # print length and count of anagrams
        print(length, count)
        count = 0


if __name__ == "__main__":
    main()
