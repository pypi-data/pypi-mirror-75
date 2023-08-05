import pygame
import logging
from typing import Callable
from coopstructs.vectors import Vector2
from coopgame.colors import Color
import functools
from coopgame.pygbutton import PygButton


def try_handler(func):
    @functools.wraps(func)
    def wrapper_handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NotImplementedError as e:
            error = f"Inherited class should implement logic for {func.__name__}"
            logging.error(error)
        except Exception as e:
            logging.error(e)
    return wrapper_handler


class GameTemplate:

    def __init__(self, screen_width:int=1600, screen_height:int=1000, max_fps:int = 60):
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.ticks = 0
        self.frame_times = []
        self.fps = None
        self.max_fps = max_fps
        self.clock = pygame.time.Clock()

        self.buttons = {}

        self.running = False

        pygame.init()


    def initialize_game(self):
        pass

    def register_button(self, id, text, callback, postion_rect):
        self.buttons[id] = PygButton(postion_rect, caption=text, callback=callback)


    def main(self):

        self.initialize_game()

        self.running = True
        ii = 0
        while self.running:
            self.update()
            self._draw(frames=ii)
            self.clock.tick(self.max_fps)
            ii += 1

        pygame.quit()

    def calculate_fps(self, ticks_last_frame: int):
        if len(self.frame_times) > 20:
            self.frame_times.pop(0)

        self.frame_times.append(ticks_last_frame)

        avg_sec_per_frame = sum(self.frame_times) / len(self.frame_times) / 1000.0
        self.fps = 1 / avg_sec_per_frame if avg_sec_per_frame > 0 else 0

    def update(self, model_updater: Callable[[int], bool] = None, sprite_updater: Callable = None):
        """:return
            Update environment based on time delta and any input
        """

        ''' Calculate the ticks between update calls so that the update functions can handle correct time deltas '''
        t = pygame.time.get_ticks()
        deltaTime = (t - self.ticks)
        self.ticks = t
        self.calculate_fps(deltaTime)

        '''Update Model'''
        if model_updater:
            model_updater(deltaTime)

        '''Update Sprites'''
        if sprite_updater:
            sprite_updater()

        '''Handle Events'''
        self.handle_events()

    def handle_events(self):
        """:return
            handle all of the registered events that have been captured since last iteration
        """

        '''Get next event'''
        event = pygame.event.poll()

        '''Check and handle button press'''
        self.handle_buttons(event)

        '''Debug Printer'''
        if event.type not in (0, 1, 4, 6):
            logging.debug(f"Pygame EventType: {event.type}")

        '''Event Type Switch'''
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.handle_key_pressed(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_left_click()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.handle_right_click()

        '''Handle hover over'''
        self._handle_hover_over()

    @try_handler
    def handle_buttons(self, event):
        for id, button in self.buttons:
            if 'click' in button.handleEvent(event):
                button.callback()

    @try_handler
    def handle_left_click(self):
        raise NotImplementedError()

    @try_handler
    def handle_right_click(self):
        raise NotImplementedError()

    @try_handler
    def handle_key_pressed(self, pressed_key):
        raise NotImplementedError()

    @try_handler
    def handle_hover_over(self, mouse_pos_as_vector: Vector2):
        raise NotImplementedError()

    def _handle_hover_over(self):
        mouse_pos_as_vector = self.mouse_pos_as_vector()
        if mouse_pos_as_vector:
            self.handle_hover_over(mouse_pos_as_vector)

    @try_handler
    def draw(self, frames:int):
        raise NotImplementedError()

    def _draw(self, frames:int):
        self.screen.fill(Color.BLACK.value)
        self.draw(frames)
        # Update the display
        pygame.display.flip()

    def mouse_pos_as_vector(self) -> Vector2:
        """ Get the global coords of the mouse position and convert them to a Vector2 object"""
        pos = pygame.mouse.get_pos()
        return Vector2(pos[0], pos[1])

    def draw_mouse_coord(self, hud: pygame.Surface, font: pygame.font.Font = None):
        if font is None:
            font = pygame.font.Font(None, 30)

        mouse_pos_as_vector = self.mouse_pos_as_vector()

        txt = f"G:{str(mouse_pos_as_vector)}"
        rendered_txt = font.render(txt, True, Color.BLUE.value)
        display1 = hud.subsurface(0, hud.get_height() - 50, hud.get_width(), 16)
        display1.blit(rendered_txt, display1.get_rect())

