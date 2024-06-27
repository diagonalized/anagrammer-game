from .state import State
from random import shuffle
import pygame


class Anagrams(State):
    def __init__(self, game):
        super().__init__(game)

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
        # sort word list by length ascending
        # self.word_list.sort(key=len)

        self.rack = Rack(self.game, self.alphagram)
        self.words = Words(self.game, self.word_list)

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
        # reset keys
        self.game.reset_keys()

    def render(self, surface):
        # fill screen with white
        surface.fill((255, 255, 255))
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


class Rack:
    def __init__(self, game, alphagram):
        self.game = game
        self.rack = alphagram
        self.staging = ""

    def render(self):
        # draw rack
        self.game.draw_text(
                self.game.screen, self.rack,
                (0, 0, 0),
                self.game.SCREEN_WIDTH // 2,
                7 * self.game.SCREEN_HEIGHT // 8,
                "scrabble"
                )
        # draw staging
        self.game.draw_text(
                self.game.screen, self.staging,
                (0, 0, 0),
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

    def unstage(self):
        # as long as there is something to unstage
        if self.staging:
            self.rack += self.staging[-1]
            self.staging = self.staging[:-1]


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
        self.gap = 60

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
            self.words.append(
                    Word(
                        # make position dynamic by adding i * 50
                        # but also wrap around after 5 words by using % 5
                        # make x add by the length of word times tile size
                        self.game, self.word_list[i],
                        # this is hellish
                        (100 + self.cumulative_width[i // self.m],
                         self.game.SCREEN_HEIGHT // 16 + (i % self.m) * 75)
                    )
                )

    def render(self):
        for word in self.words:
            word.render()
        # for i in range(len(self.word_list)):
        #     self.game.draw_text(
        #             self.game.screen, self.word_list[i],
        #             (0, 0, 0),
        #             # slightly right of left side
        #             300,
        #             # 1/8 of the way down plus 50 for each word
        #             self.game.SCREEN_HEIGHT // 8 + i * 150,
        #             "anagram"
        #             )

    def fill_word(self, idx):
        # check index in self.Words
        self.words[idx].progress = self.words[idx].letters
        self.words[idx].complete = True
        self.words[idx].update_boxes()


class Word:
    def __init__(self, game, word, position):
        self.letters = word
        self.boxes = []
        self.progress = '_' * len(self.letters)
        self.complete = False

        # position
        self.position = position

        for i in range(len(self.letters)):
            box = BoxWithLetter(
                    game, self.progress[i],
                    (167, 199, 231),  # pastel blue
                    (50, 50),
                    (self.position[0] + i * 60, self.position[1])
                    )
            self.boxes.append(box)

    # update boxes with progress
    def update_boxes(self):
        for i in range(len(self.letters)):
            self.boxes[i].letter = self.progress[i]

    # each letter in word is surrounded by a colored box
    def render(self):
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

    def draw(self):
        # Draw the box
        pygame.draw.rect(self.game.screen, self.box_color, self.box_rect)
        # outline the box
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.box_rect, 1)

        # Render the letter
        letter_surface = self.game.anagram_font.render(
                self.letter, True, (0, 0, 0)
                )
        letter_rect = letter_surface.get_rect(center=self.box_rect.center)

        # Draw the letter
        self.game.screen.blit(letter_surface, letter_rect)