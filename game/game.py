import pygame
from pathlib import Path
from .states.title import Title


class Game:
    def __init__(self, wordfinder):

        pygame.init()

        # initialize window
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                )
        pygame.display.set_caption("Anagrammer")

        # game running when initialized
        self.running = True

        # initialize wordfinder
        self.wf = wordfinder

        # initialize state stack
        self.state_stack = []

        # load assets (font for now)
        self.load_assets()

        # load states (title screen for now)
        self.load_states()

    def game_loop(self):
        while self.running:
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.state_stack[-1].update()

    def render(self):
        self.state_stack[-1].render(self.screen)
        pygame.display.flip()

    def load_assets(self):
        # path to assets directory, going up one directory
        self.assets_dir = Path(__file__).parents[0].with_name("assets")
        # load font
        self.font_dir = self.assets_dir / "Scramble-KVBe.ttf"
        self.font = pygame.font.Font(self.font_dir, 64)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def draw_text(self, surface, text, color, x, y):
        # render text to surface
        text_surface = self.font.render(text, True, color)
        # get rect of text surface
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        # blit text to screen
        surface.blit(text_surface, text_rect)
