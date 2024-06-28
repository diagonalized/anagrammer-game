from .state import State
from random import shuffle
import pygame


class Anagrams(State):
    def __init__(self, game):
        super().__init__(game)

        """ INPUT CURRENTLY HARD CODED """
        length = 5
        num_anagrams = 1
        self.word_list = self.game.wf.search_by_preference(
                length, num_anagrams
                )

        # for some reason doing search by alphagram doesn't work the 2nd time?
        # self.word_list = self.game.wf.search_by_alphagram("pain")
        # print(self.word_list)
        self.alphagram = self.game.wf.get_alphagram(self.word_list)
        self.word_list = self.game.wf.extend_subanagrams(self.word_list)
        # alphabetize and sort by length
        self.word_list.sort()
        self.word_list.sort(key=len)

        self.rack = Rack(self.game, self.alphagram)
        self.words = Words(self.game, self.word_list)

        # start with first word selected
        self.idx = 0
        self.prev_idx = self.idx
        self.move_selected()

    def update(self, delta_time, actions):
        # exit
        if actions["escape"]:
            self.exit_state()
        # shuffle
        if actions["space"]:
            self.rack.shuffle()
        # stage letter
        if actions["letter"]:
            self.rack.stage(actions["letter"])
        # unstage letter
        if actions["backspace"]:
            self.rack.unstage()
        # validate
        if actions["enter"]:
            self.validate()
        # select word
        if actions["up"]:
            self.idx -= 1
            self.idx %= len(self.word_list)
            self.move_selected()
        if actions["down"]:
            self.idx += 1
            self.idx %= len(self.word_list)
            self.move_selected()
        if actions["left"]:
            self.idx -= self.words.m
            self.idx %= len(self.word_list)
            self.move_selected()
        if actions["right"]:
            self.idx += self.words.m
            self.idx %= len(self.word_list)
            self.move_selected()
        # hint
        if actions["hint"]:
            self.words.hint()
        # reset keys
        self.game.reset_keys()

    def render(self, surface):
        # fill screen with white
        surface.fill(self.game.white)
        # draw rack
        self.rack.render()
        # draw words
        self.words.render()

    def validate(self):
        # check if staging is a word in perfs
        if self.rack.staging in self.word_list:
            # update blank word to filled word
            print("correct!")
            self.words.fill_word(self.word_list.index(self.rack.staging))
            # clear staging
            self.rack.staging = ""
            # refill rack
            self.rack.rack = self.alphagram

    def move_selected(self):
        # unselect previous word
        self.words.words[self.prev_idx].selected = False
        # select next word
        self.words.words[self.idx].selected = True
        self.prev_idx = self.idx


class Rack:
    def __init__(self, game, alphagram):
        self.game = game
        self.rack = alphagram
        self.staging = ""

    def render(self):
        # draw rack
        self.game.draw_text(
                self.game.screen, self.rack,
                self.game.black,
                self.game.SCREEN_WIDTH // 2,
                7 * self.game.SCREEN_HEIGHT // 8,
                "scrabble"
                )
        # draw staging
        self.game.draw_text(
                self.game.screen, self.staging,
                self.game.black,
                self.game.SCREEN_WIDTH // 2,
                6 * self.game.SCREEN_HEIGHT // 8,
                "scrabble"
                )

    def shuffle(self):
        rack = list(self.rack)
        shuffle(rack)
        self.rack = "".join(rack)

    def stage(self, letter):
        # letter must be in rack to stage it
        if letter in self.rack:
            self.staging += letter
            self.rack = self.rack.replace(letter, "", 1)

    # return staged letter back in order of the alphagram
    def unstage(self):
        # as long as there is something to unstage
        if self.staging:
            # self.rack += self.staging[-1]
            # self.staging = self.staging[:-1]
            last = self.staging[-1]
            self.rack = self._insert_letter(self.rack, last)
            self.staging = self.staging[:-1]

    def _insert_letter(self, string, letter):
        for i, char in enumerate(string):
            if char > letter:
                return string[:i] + letter + string[i:]
        return string + letter


class Words:
    def __init__(self, game, word_list):
        self.game = game
        self.word_list = word_list
        self.words = []
        # print(self.word_list)
        self.init_words()

    def init_words(self):
        """ LORD SAVE US FROM THIS CODE """

        # words in row and column?? my stuff jank
        self.m = 6
        # words in column
        # n = 5
        self.gap = 50

        # for i in range(len(word_list)):
        #     print(len(max(word_list[i // 5: i // 5 + 5], key=len)))
        # Number of columns
        self.num_columns = (len(self.word_list) + self.m - 1) // self.m

        # Find the length of the longest word in each column
        self.longest_per_column = [
            len(max(
                self.word_list[col * self.m: (col + 1) * self.m], key=len
                    )
                )
            for col in range(self.num_columns)
        ]

        # Calculate cumulative width for each column
        self.cumulative_width = [0] * self.num_columns
        for col in range(1, self.num_columns):
            self.cumulative_width[col] = (
                    self.cumulative_width[col - 1]
                    + (self.longest_per_column[col - 1] + 1) * self.gap
                    )
        # adds the words to the list of words, their object
        for i in range(len(self.word_list)):
            # this is hellish
            word_x = self.game.SCREEN_WIDTH // 32 + self.cumulative_width[i // self.m]
            word_y = self.game.SCREEN_HEIGHT // 16 + (i % self.m) * 75
            # make position dynamic by adding i * 50
            # but also wrap around after 5 words by using % 5
            # make x add by the length of word times tile size
            self.words.append(
                    Word(self.game, self.word_list[i], (word_x, word_y))
                )

    def render(self):
        for word in self.words:
            word.render()
        # for i in range(len(self.word_list)):
        #     self.game.draw_text(
        #             self.game.screen, self.word_list[i],
        #             self.game.black,
        #             # slightly right of left side
        #             300,
        #             # 1/8 of the way down plus 50 for each word
        #             self.game.SCREEN_HEIGHT // 8 + i * 150,
        #             "anagram"
        #             )

    def fill_word(self, idx):
        # check index in self.Words
        self.words[idx].progress = self.words[idx].letters
        for letter in self.words[idx].boxes:
            letter.shown = True
        self.words[idx].complete = True
        self.words[idx].update_boxes()

    def hint(self):
        """ JANKY AS HELL"""
        # make sure word is selected
        for word in self.words:
            if word.selected:

                # add next letter
                for i in range(len(word.progress)):
                    if word.progress[i] == "_":
                        word.progress = word.progress[:i] + word.letters[i] + word.progress[i + 1:]
                        print(word.progress)
                        break

                # show letter
                for i in range(len(word.letters)):
                    if word.progress[i] != "_":
                        word.boxes[i].shown = True

                if "_" not in word.progress:
                    word.complete = True

                word.update_boxes()

                print("hello")


class Word:
    def __init__(self, game, word, position):
        self.game = game
        self.letters = word
        self.boxes = []
        self.progress = '_' * len(self.letters)
        self.complete = False
        self.selected = False
        self.box_length = 50
        self.gap = 10

        # position
        self.position = position

        for i in range(len(self.letters)):
            box = BoxWithLetter(
                    game, self.progress[i],
                    (167, 199, 231),  # pastel blue
                    (self.box_length, self.box_length),
                    (self.position[0] + i * (self.box_length + self.gap),
                     self.position[1])
                    )
            self.boxes.append(box)

    # update boxes with progress
    def update_boxes(self):
        for i in range(len(self.letters)):
            self.boxes[i].letter = self.progress[i]

    # each letter in word is surrounded by a colored box
    def render(self):
        # if selected have a low opacity pastel blue
        # outline is around the whole word
        if self.selected:
            outline = pygame.Surface(
                        (
                            len(self.letters) * (self.box_length + self.gap),
                            self.box_length + self.gap)
                        )
            outline.set_alpha(128)
            outline.fill((193, 205, 151))  # test
            # center it around the word
            self.game.screen.blit(
                    outline,
                    (self.position[0] - self.gap // 2,
                     self.position[1] - self.gap // 2)
                    )

        for box in self.boxes:
            box.draw()


class BoxWithLetter:
    def __init__(self, game, letter, box_color, box_size, position):
        self.game = game
        self.letter = letter
        self.box_color = box_color
        self.box_size = box_size
        self.position = position
        self.box_rect = pygame.Rect(position, box_size)
        self.shown = False

    def draw(self):
        # Draw the box
        pygame.draw.rect(self.game.screen, self.box_color, self.box_rect)
        # outline the box
        pygame.draw.rect(self.game.screen, self.game.black, self.box_rect, 1)

        # Render the letter
        if self.shown:
            letter_surface = self.game.anagram_font.render(
                    self.letter, True, self.game.black
                    )
            letter_rect = letter_surface.get_rect(center=self.box_rect.center)

            # Draw the letter
            self.game.screen.blit(letter_surface, letter_rect)
