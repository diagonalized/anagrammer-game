'''
TODO: Make extend_subanagrams() more intuitive, it changes the original list
yet it returns a new list. I'll have to sleep on it.
'''
from pathlib import Path
from random import choice
from itertools import combinations


class WordFinder:
    def __init__(self):
        # initalize database of words sorted alphagram by anagram
        self.db = {}

        # guaranteed path to nwl20.txt
        assets_dir = Path(__file__).parents[0].with_name('assets')
        lexicon = assets_dir / 'nwl20.txt'

        # load words from nwl20.txt
        # read only first word, definitions can be added later for word lookup
        with lexicon.open('r') as f:
            for line in f:
                # make sure its lower for case-insensitive search
                word = line.split()[0].lower()
                # sort the word into its alphagram
                alphagram = "".join(sorted(word))
                # add the word to the list of anagrams
                if alphagram in self.db:
                    self.db[alphagram].append(word)
                else:
                    self.db[alphagram] = [word]

    def search_by_preference(self, length: int, num_of_anagrams: int) -> list:
        """ takes user input for perfect anagram search

        Args:
            num_of_anagrams: number of perfect anagrams
            length: length of alphagram that is to be found


        Returns:
            list of perfect anagrams
            TODO: might change this if we want to return alphagram too
            although, it might be useful for bingos only in scrabble...

        """

        # find all alphagrams of given length
        candidates = [k for k in self.db.keys() if len(k) == length]

        # if no alphagram of that length, return empty list
        if not candidates:
            return []

        # find all alphagrams with given number of anagrams
        candidates = [
                self.db[k]
                for k in candidates if len(self.db[k]) == num_of_anagrams
                ]

        # return random choice from the list of candidates, if any
        return choice(candidates) if candidates else []

    def search_by_alphagram(self, alphagram: str) -> list:
        """ search for perfect anagrams of a given alphagram

        Args:
            alphagram: alphagram to search for, could be sorted or unsorted

        Returns:
            list of perfect anagrams of the alphagram

        """

        # make sure string is sorted and lower for case-insensitive search
        alphagram = "".join(sorted(alphagram)).lower()
        # benefits of alphagrams
        return self.db.get(alphagram, [])

    # keep code consistent by extending a list of perfect anagrams
    def extend_subanagrams(self, anagrams: list) -> list:
        """ extend list of anagrams with sub-anagrams

        Args:
            anagrams: list of perfect anagrams

        Returns:
            list of perfect anagrams and sub-anagrams

        """

        # first word should already be lower-case, only alphagramize it
        alphagram = "".join(sorted(anagrams[0]))
        """
        since a list of anagrams that are not perfect anagrams
        does not make sense in the scope of this program,
        return early if each word in the list is not a perfect anagram

        note: no need for lower-case conversion, as it should already be done
        """
        if not all(
                "".join(sorted(word)) == alphagram
                for word in anagrams
                ):
            return []

        # initialize list of combinations of alphagram
        combs = []
        # check every combination of alphagram where length is 2 to n-1
        # note that len(alphagram) is n-1 and not n
        # i wish i knew why, but i don't
        for length in range(2, len(alphagram)):
            # permutations of each length
            for combination in combinations(alphagram, length):
                combs.append("".join(combination))

        # extend the list of anagrams with sub-anagrams
        for comb in combs:
            if comb in self.db:
                anagrams.extend(self.db[comb])

        # return list of anagrams
        return list(set(anagrams))
