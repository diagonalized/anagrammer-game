from .state import State


class Title(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        pass

    def render(self, surface):
        # fill screen with white
        surface.fill((255, 255, 255))
        # draw title text
        self.game.draw_text(
                self.game.screen, "Anagrammer", (0, 0, 0),
                self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 4
                )
