from os import path
from abc import ABC, abstractmethod

import pygame as pg  # type: ignore
import math
from typing import Tuple, Dict, Any, List

# GLOBALS #

# SIZES
PIXEL_SIZE = 10
BALL_SIZE = (2 * PIXEL_SIZE, 2 * PIXEL_SIZE)
PAD_SIZE = (2 * PIXEL_SIZE, 16 * PIXEL_SIZE)
SCREEN_SIZE = (1600, 900)
SCORE_IMAGE_SIZE = (64, 64)

# COORDINATES
PAD_START_Y = SCREEN_SIZE[1] / 2 - PAD_SIZE[1] / 2
PAD_X_OFFSET = 6 * PIXEL_SIZE
LEFT_PAD_X = PAD_X_OFFSET
RIGHT_PAD_X = SCREEN_SIZE[0] - PAD_X_OFFSET - PAD_SIZE[0]
RIGHT_PAD_START = [RIGHT_PAD_X, PAD_START_Y]
LEFT_PAD_START = [LEFT_PAD_X, PAD_START_Y]
BALL_START = [SCREEN_SIZE[0] / 2 - BALL_SIZE[0] / 2,
              SCREEN_SIZE[1] / 2 - BALL_SIZE[1] / 2]
SCREEN_CORNER = (0, 0)
LEFT_SCORE_CORNER = ((SCREEN_SIZE[0] / 2) - 1.5 * SCORE_IMAGE_SIZE[0], SCREEN_SIZE[1] / 10)
COLON_CORNER = ((SCREEN_SIZE[0] / 2) - 0.5 * SCORE_IMAGE_SIZE[0], SCREEN_SIZE[1] / 10)
RIGHT_SCORE_CORNER = ((SCREEN_SIZE[0] / 2) + 0.5 * SCORE_IMAGE_SIZE[0], SCREEN_SIZE[1] / 10)
RIGHT_TEXT_LOCATION = (SCREEN_SIZE[0] * 0.8, SCREEN_SIZE[1] / 3)
LEFT_TEXT_LOCATION = (SCREEN_SIZE[0] * 0.2, SCREEN_SIZE[1] / 3)
PAUSE_TEXT_LOCATION = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 4)
WIN_TEXT_LOCATION = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 3)

# COLORS
LEFT_PAD_COLOR = (0, 255, 64)
RIGHT_PAD_COLOR = (255, 64, 0)
BALL_COLOR = (255, 255, 255)
RIGHT_WIN_COLOR = (255, 0, 0)
LEFT_WIN_COLOR = (0, 255, 0)
BLACK_COLOR = (0, 0, 0)

# KEYS
LEFT_PAD_UP = pg.K_w
LEFT_PAD_DOWN = pg.K_s
RIGHT_PAD_UP = pg.K_UP
RIGHT_PAD_DOWN = pg.K_DOWN
PAUSE = pg.K_SPACE
EXIT = pg.K_ESCAPE

# TIMING
FPS = 120
BALL_SPEED = 7.5
PAD_SPEED = 6

# DIRECTIONS
EPSILON = 0.01
RIGHT_UPPER_LIMIT = math.pi * 4 / 12
RIGHT_LOWER_LIMIT = math.pi * -4 / 12
LEFT_UPPER_LIMIT = math.pi * 8 / 12
LEFT_LOWER_LIMIT = math.pi * 16 / 12
RIGHT_DIRECTION = 0
LEFT_DIRECTION = math.pi

# IMAGES
MY_DIR = path.dirname(__file__)
ZERO = path.join(MY_DIR, "sprites", "0.png")
ONE = path.join(MY_DIR, "sprites", "1.png")
TWO = path.join(MY_DIR, "sprites", "2.png")
THREE = path.join(MY_DIR, "sprites", "3.png")
COLON = path.join(MY_DIR, "sprites", "colon.png")

# SOUNDS
RIGHT_PAD_SOUND = path.join(MY_DIR, "sfx", "ting.wav")
LEFT_PAD_SOUND = path.join(MY_DIR, "sfx", "tong.wav")

# TEXT
SANS = path.join(MY_DIR, "fonts", "comic.ttf")
WIN_FONT_SIZE = 69
INSTRUCTIONS_FONT_SIZE = 32
LEFT_WIN_TEXT = "left pad wins!"
RIGHT_WIN_TEXT = "right pad wins!"
LEFT_INSTRUCTIONS = "left pad:\nW - go up\nS - go down\nSPACE - pause/start\nESC - exit"
RIGHT_INSTRUCTIONS = "right pad:\nUP - go up\nDOWN - go down\nSPACE - pause/start\nESC - exit"
PAUSE_TEXT = "    game paused.\npress space to continue"

# ETC
MAX_SCORE = 3


def get_images() -> Dict:
    big_sans = pg.font.Font(SANS, WIN_FONT_SIZE)
    small_sans = pg.font.Font(SANS, INSTRUCTIONS_FONT_SIZE)

    left_wins_text = [big_sans.render(LEFT_WIN_TEXT, True, LEFT_WIN_COLOR)]
    right_wins_text = [big_sans.render(RIGHT_WIN_TEXT, True, RIGHT_WIN_COLOR)]

    left_instructions_texts = []
    for t in LEFT_INSTRUCTIONS.splitlines():
        left_instructions_texts.append(small_sans.render(t, True, LEFT_WIN_COLOR))

    right_instructions_texts = []
    for t in RIGHT_INSTRUCTIONS.splitlines():
        right_instructions_texts.append(small_sans.render(t, True, RIGHT_WIN_COLOR))

    pause_texts = []
    for t in PAUSE_TEXT.splitlines():
        pause_texts.append(small_sans.render(t, True, BALL_COLOR))

    d = {0: pg.image.load(ZERO), 1: pg.image.load(ONE), 2: pg.image.load(TWO),
         3: pg.image.load(THREE), "colon": pg.image.load(COLON), "left win": left_wins_text,
         "right win": right_wins_text, "left instructions": left_instructions_texts,
         "right instructions": right_instructions_texts, "pause": pause_texts}

    return d


def blit_text(screen, images: Dict, location_above: Tuple) -> None:
    assert len(images) > 0, "bad input to blit_text"

    height = images[0].get_height()
    max_width = max(i.get_width() for i in images)
    corner = (location_above[0] - max_width / 2, location_above[1])

    for i, text in enumerate(images):
        my_corner = (corner[0], corner[1] + i * height)
        screen.blit(text, my_corner)


def get_sounds() -> Dict:
    d = {"left_pad": pg.mixer.Sound(LEFT_PAD_SOUND),
         "right_pad": pg.mixer.Sound(RIGHT_PAD_SOUND), }
    return d


class Game:
    def __init__(self, screen, image_dict, sound_dict) -> None:
        # reset stuff
        self.right_pad = Pad(RIGHT_PAD_START, RIGHT_PAD_UP, RIGHT_PAD_DOWN, RIGHT_PAD_COLOR)
        self.left_pad = Pad(LEFT_PAD_START, LEFT_PAD_UP, LEFT_PAD_DOWN, LEFT_PAD_COLOR)
        self.ball = Ball()
        self.done = False
        self.paused = True
        self.game_over = False
        self.left_score = 0
        self.right_score = 0

        # get static objects
        self.screen = screen
        self.images = image_dict
        self.sounds = sound_dict

        # do cool tingz
        self.render()
        self.draw_pause()
        pg.display.flip()

    def reset(self):
        self.right_pad = Pad(RIGHT_PAD_START, RIGHT_PAD_UP, RIGHT_PAD_DOWN, RIGHT_PAD_COLOR)
        self.left_pad = Pad(LEFT_PAD_START, LEFT_PAD_UP, LEFT_PAD_DOWN, LEFT_PAD_COLOR)
        self.ball = Ball()
        self.done = False
        self.paused = True
        self.game_over = False
        self.left_score = 0
        self.right_score = 0

    def render(self):
        self.empty_screen()
        self.right_pad.draw(self.screen)
        self.left_pad.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_score()

    def empty_screen(self) -> None:
        rectangle = pg.Rect(*SCREEN_CORNER, *SCREEN_SIZE)
        pg.draw.rect(self.screen, BLACK_COLOR, rectangle)

    def draw_score(self) -> None:
        left = self.left_score
        right = self.right_score
        assert (left in self.images and right in self.images), "bad input to draw_score"

        self.screen.blit(self.images[left], LEFT_SCORE_CORNER)
        self.screen.blit(self.images["colon"], COLON_CORNER)
        self.screen.blit(self.images[right], RIGHT_SCORE_CORNER)

    def draw_pause(self) -> None:
        blit_text(self.screen, self.images["right instructions"], RIGHT_TEXT_LOCATION)
        blit_text(self.screen, self.images["left instructions"], LEFT_TEXT_LOCATION)
        blit_text(self.screen, self.images["pause"], PAUSE_TEXT_LOCATION)

    def check_pause(self, events: List) -> None:
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.paused = not self.paused
                self.draw_pause()
                pg.display.flip()

                if self.game_over:
                    # reset game after game over
                    self.reset()

    def check_winner(self) -> None:
        if self.left_score == MAX_SCORE:
            self.paused = self.game_over = True
            blit_text(self.screen, self.images["left win"], WIN_TEXT_LOCATION)
            pg.display.flip()

        elif self.right_score == MAX_SCORE:
            self.paused = self.game_over = True
            blit_text(self.screen, self.images["right win"], WIN_TEXT_LOCATION)
            pg.display.flip()

    def check_exit(self, events: List) -> None:
        for event in events:
            if event.type == pg.QUIT:
                # X button clicked
                self.done = True

        mod_bits = pg.key.get_mods()
        pressed = pg.key.get_pressed()
        if (mod_bits & pg.KMOD_ALT and pressed[pg.K_F4]) or pressed[pg.K_ESCAPE]:
            # alt-f4 or esc
            self.done = True

    def tick(self) -> None:
        pressed = pg.key.get_pressed()
        self.ball.move(self.right_pad, self.left_pad, self, self.sounds)
        self.right_pad.move(pressed)
        self.left_pad.move(pressed)


class DrawableComponent(ABC):

    @abstractmethod
    def draw(self, screen) -> None:
        pass


class Ball(DrawableComponent):
    def __init__(self):
        self.corner = BALL_START
        self.angle_in_radians = RIGHT_DIRECTION

    def get_next_corner(self) -> Tuple[float, float]:
        next_ball_x = self.corner[0] + (math.cos(self.angle_in_radians) * BALL_SPEED)
        next_ball_y = self.corner[1] - (math.sin(self.angle_in_radians) * BALL_SPEED)

        return next_ball_x, next_ball_y

    def move(self, right_pad, left_pad, nong, sound_dict) -> None:
        next_corner = self.get_next_corner()
        # ball touches right pad
        if (right_pad.corner[0] + PAD_SIZE[0] > next_corner[0] + BALL_SIZE[0] - EPSILON >
                right_pad.corner[0]
                and right_pad.corner[1] - BALL_SIZE[1] < self.corner[1] < right_pad.corner[1] + PAD_SIZE[1]):
            sound_dict["right_pad"].play()
            ball_location_on_pad_percentage = ((self.corner[1] + BALL_SIZE[1] / 2) - right_pad.corner[1]) / float(
                (PAD_SIZE[1]))
            if ball_location_on_pad_percentage < 0:
                new_ball_direction = LEFT_UPPER_LIMIT
            elif ball_location_on_pad_percentage > 1:
                new_ball_direction = LEFT_LOWER_LIMIT
            else:
                new_ball_direction = LEFT_UPPER_LIMIT + ball_location_on_pad_percentage * (
                        LEFT_LOWER_LIMIT - LEFT_UPPER_LIMIT)
            self.angle_in_radians = new_ball_direction

        # ball touches left pad
        elif (left_pad.corner[0] < next_corner[0] + EPSILON < left_pad.corner[0] + PAD_SIZE[0]
              and left_pad.corner[1] - BALL_SIZE[1] < self.corner[1] < left_pad.corner[1] + PAD_SIZE[1]):
            sound_dict["left_pad"].play()
            ball_location_on_pad_percentage = ((self.corner[1] + BALL_SIZE[1] / 2) - left_pad.corner[1]) / float(
                (PAD_SIZE[1]))
            if ball_location_on_pad_percentage < 0:
                new_ball_direction = RIGHT_UPPER_LIMIT
            elif ball_location_on_pad_percentage > 1:
                new_ball_direction = RIGHT_LOWER_LIMIT
            else:
                new_ball_direction = RIGHT_UPPER_LIMIT + ball_location_on_pad_percentage * (
                        RIGHT_LOWER_LIMIT - RIGHT_UPPER_LIMIT)
            self.angle_in_radians = new_ball_direction

        # ball touches top or bottom edge
        if next_corner[1] < 0 or next_corner[1] + BALL_SIZE[1] > SCREEN_SIZE[1]:
            self.angle_in_radians = -self.angle_in_radians

        # ball touches left edge
        if next_corner[0] + BALL_SIZE[0] < 0:
            nong.right_score += 1
            if nong.right_score < MAX_SCORE:
                self.corner = BALL_START
                self.angle_in_radians = RIGHT_DIRECTION

        # ball touches right edge
        elif next_corner[0] > SCREEN_SIZE[0]:
            nong.left_score += 1
            if nong.left_score < MAX_SCORE:
                self.corner = BALL_START
                self.angle_in_radians = LEFT_DIRECTION

        # move ball after changing
        # i use `self.get_next_corner` again because the parameters it looks at changed
        self.corner = self.get_next_corner()

    def draw(self, screen) -> None:
        rectangle = pg.Rect(*self.corner, *BALL_SIZE)
        pg.draw.rect(screen, BALL_COLOR, rectangle)


class Pad(DrawableComponent):
    def __init__(self, corner: List, up_key, down_key, color):
        self.corner = corner
        self.up_key = up_key
        self.down_key = down_key
        self.color = color

    def move(self, pressed) -> None:
        if pressed[self.up_key] and self.corner[1] > 0:
            self.corner[1] -= PAD_SPEED
        if pressed[self.down_key] and self.corner[1] < (SCREEN_SIZE[1] - PAD_SIZE[1]):
            self.corner[1] += PAD_SPEED

    def draw(self, screen) -> None:
        rectangle = pg.Rect(*self.corner, *PAD_SIZE)
        pg.draw.rect(screen, self.color, rectangle)


def main() -> None:
    """
    play the nong game.
    :return:
    """

    pg.mixer.pre_init(22050, -16, 2, 1024)  # no idea why this works
    pg.init()
    pg.display.set_caption("nong")
    pg.mixer.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(SCREEN_SIZE)
    image_dict = get_images()
    sound_dict = get_sounds()
    nong = Game(screen, image_dict, sound_dict)

    while not nong.done:
        # event stuff
        events = pg.event.get()
        nong.check_exit(events)
        nong.check_pause(events)
        nong.check_winner()

        # update state
        clock.tick(FPS)
        if not nong.paused:
            nong.tick()
            nong.render()
            pg.display.flip()

    print("goodbye")


if __name__ == "__main__":
    main()
