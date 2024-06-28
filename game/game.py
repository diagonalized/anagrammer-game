import pygame
from pathlib import Path
from .states.title import Title
from time import time


class Game:
    def __init__(self, wordfinder):

        pygame.init()

        # initialize window
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                )
        pygame.display.set_caption("Anagrammer")

        self.clock = pygame.time.Clock()

        self.FPS = 60

        # game running when initialized
        self.running = True

        # initialize wordfinder
        self.wf = wordfinder

        # initialize actions dictionary
        self.actions = {
                "left": False,
                "right": False,
                "up": False,
                "down": False,
                "enter": False,
                "space": False,
                "escape": False,
                "letter": None,
                "backspace": False,
                "hint": False,
                }

        # initialize dt and prev_time
        self.dt, self.prev_time = 0, 0

        # initialize state stack
        self.state_stack = []

        # load assets
        self.load_assets()

        # load states
        self.load_states()

        # init colors
        self.load_colors()

    def game_loop(self):
        while self.running:
            self.get_events()
            self.update()
            self.render()

        pygame.quit()

    def get_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # use ijkl for movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = True
                # first enter key
                if event.key == pygame.K_RETURN:
                    self.actions["enter"] = True
                # then movement keys, arrow keys
                if event.key == pygame.K_UP:
                    self.actions["up"] = True
                if event.key == pygame.K_DOWN:
                    self.actions["down"] = True
                if event.key == pygame.K_LEFT:
                    self.actions["left"] = True
                if event.key == pygame.K_RIGHT:
                    self.actions["right"] = True
                # shuffle key
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = True
                # handle typing in game
                if event.unicode.isalpha():
                    self.actions["letter"] = event.unicode
                # unstage letter
                if event.key == pygame.K_BACKSPACE:
                    self.actions["backspace"] = True

                if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_h:
                    self.actions["hint"] = True

            # be sure to turn off actions when key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = False
                if event.key == pygame.K_RETURN:
                    self.actions["enter"] = False
                if event.key == pygame.K_UP:
                    self.actions["up"] = False
                if event.key == pygame.K_DOWN:
                    self.actions["down"] = False
                if event.key == pygame.K_LEFT:
                    self.actions["left"] = False
                if event.key == pygame.K_RIGHT:
                    self.actions["right"] = False
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = False
                if event.unicode.isalpha():
                    self.actions["letter"] = None
                if event.key == pygame.K_BACKSPACE:
                    self.actions["backspace"] = False
                if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_h:
                    self.actions["hint"] = False

    def update(self):
        self.clock.tick(self.FPS)
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.screen)
        pygame.display.flip()

    def get_dt(self):
        now = time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def load_assets(self):
        # path to assets directory, going up one directory
        self.assets_dir = Path(__file__).parents[0].with_name("assets")
        # load font
        self.font_dir = self.assets_dir / "Scramble-KVBe.ttf"
        # load scrabble font
        self.scrabble_font_size = 64
        self.scrabble_font = pygame.font.Font(
                self.assets_dir / "Scramble-KVBe.ttf",
                self.scrabble_font_size
                )

        # use open sans for now
        self.anagram_font_size = 48
        self.anagram_font = pygame.font.Font(None, self.anagram_font_size)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def load_colors(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def draw_text(self, surface, text, color, x, y, font):
        # render text to surface
        if font == "scrabble":
            text_surface = self.scrabble_font.render(text, True, color)
        if font == "anagram":
            text_surface = self.anagram_font.render(text, True, color)

        # get rect of text surface
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        # blit text to screen
        surface.blit(text_surface, text_rect)

    def reset_keys(self):
        for key in self.actions:
            self.actions[key] = False
