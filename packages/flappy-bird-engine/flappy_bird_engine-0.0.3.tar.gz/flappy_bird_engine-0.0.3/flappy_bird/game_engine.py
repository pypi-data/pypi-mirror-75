from random import randint
from time import time
import pygame
from src.game_object import GameObject
from src.bird import Bird
from src.pipe import Pipe

# Constants
WINDOW_SIZE = (288, 512)
GRAVITY = 1
SCROLL_SPEED = 5


class GameEngine:
    """
    This class is used to store, update, and draw the state of the game.

    Args:
       game.Surface): The window in which to draw the game.

    Attributes:
        window: The window on which to draw the game.
        background: An object displaying the distant background.
        ground_height: The height of the ground in pixels.
        ground: An object for displaying the ground.
        top_pipe: An object representing the top half of the pipe which the player must avoid.
        bottom_pipe: An object representing the bottom half of the pipe which the player must avoid.
        bird: The bird controlled by the player.
        continue_game: Indicates whether or not the game should continue.
        score: The player's score in seconds.
        epoch: The time at which the game began.
    """
    def __init__(self, window, fps):
        self.window = window
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.background = GameObject(pygame.image.load('../assets/bg.png'), [0, 0], window)
        self.ground_height = WINDOW_SIZE[1] - pygame.image.load('../assets/Ground.png').get_height()
        self.ground = GameObject(pygame.image.load('../assets/Ground.png'), [0, self.ground_height], window)
        self.top_pipe = None
        self.bottom_pipe = None
        self.bird = Bird(window)
        self.continue_game = True
        self.score = 0
        self.epoch = 0
        self._initialize_pipes()
 
    def start_game(self):
        """
        Starts the game with an initial countdown.

        Takes no arguments and returns nothing.
        """
        timer = 0
        while timer < (self.fps * 3):
            self.events()
            self.window.fill(pygame.Color('black'))
            self.background.draw()
            self.ground.draw()
            self.top_pipe.draw()
            self.bottom_pipe.draw()

            font = pygame.font.SysFont('Verdana', 80, True)
            surface = font.render(str(3 - (timer // self.fps)), True, pygame.Color('white'))
            self.window.blit(surface, ((self.window.get_width() // 2) - (surface.get_width() // 2), 150))

            self.bird.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            timer += 1
        self.epoch = time()

    def events(self):
        """
        Handle player triggered events.

        Accepts no arguments and returns nothing.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.continue_game = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.bird.jump()

    def update_state(self):
        """
        Updates the state of the game.

        Accepts no arguments and returns nothing.
        """
        # Move Pipes And Bird
        self.bird.fall(GRAVITY)
        self.bird.move()
        self.top_pipe.move()
        self.bottom_pipe.move()

        # Reset Pipes If Off Screen
        if self.top_pipe.off_screen():
            self._initialize_pipes()

        # Detect If Bird Is Colliding With Pipes, Ground, Or Ceiling
        if self.bird.is_colliding(self.top_pipe) or \
            self.bird.is_colliding(self.bottom_pipe) or \
                self.bird.hit_edge(self.ground_height):
            self.continue_game = False
        else:
            self.score = time() - self.epoch

    def draw_frame(self):
        """
        Draws a single game frame to the screen.

        Takes no arguments are returns nothing.
        """
        self.window.fill(pygame.Color('black'))
        self.background.draw()
        self.top_pipe.draw()
        self.bottom_pipe.draw()
        self.ground.draw()
        self._draw_score()
        self.bird.draw()
        pygame.display.update()

    def next_frame(self):
        """
        Waits for time to elapse until the next frame according to the declared FPS.

        Accepts no arguments and returns nothing.
        """
        self.clock.tick(self.fps)

    def _initialize_pipes(self):
        pipe_gap = 160
        pipe_clearance = 10
        center = randint(pipe_clearance + (pipe_gap // 2), self.ground_height - pipe_clearance - (pipe_gap // 2))
        top_pos = [WINDOW_SIZE[0], center - (pipe_gap // 2) - pygame.image.load('../assets/pipe.png').get_height()]
        bottom_pos = [WINDOW_SIZE[0], center + (pipe_gap // 2)]
        self.top_pipe = Pipe("top", top_pos, SCROLL_SPEED, self.window)
        self.bottom_pipe = Pipe("bottom", bottom_pos, SCROLL_SPEED, self.window)
       
    def _draw_score(self):
        offset = 10
        font = pygame.font.SysFont('Verdana', 30, True)
        surface = font.render('Score: ' + str(int(self.score)), True, pygame.Color('white'))
        self.window.blit(surface, (offset, offset))
