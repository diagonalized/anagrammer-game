from .state import State
from .anagrams import Anagrams


class Title(State):
    def __init__(self, game):
        super().__init__(game)

        self.options = {
                "Preferences": False,
                "Alphagram": False,
                "Exit": False,
                }

    def update(self, delta_time, actions):
        if actions["enter"]:
            new_state = Anagrams(self.game)
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, surface):
        # fill screen with white
        # TODO: add nightmode switch
        surface.fill(self.game.white)
        # draw title text
        self.game.draw_text(
                self.game.screen, "Anagrammer",
                self.game.black,  # black, RGB TEST IT?
                self.game.SCREEN_WIDTH // 2,  # center x
                self.game.SCREEN_HEIGHT // 4,  # fourth of the way down
                "scrabble"
                )


# class for dropdownish menus when you press enter on a menu option
class DropdownInput:
    def __init__(self, game, num_input_boxes: int):
        self.game = game
        self.input_boxes = []

    def render(self):
        for box in self.input_boxes:
            box.render()
