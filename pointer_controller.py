import pyautogui
import numpy as np


class PointerController:
    # Refrence documentation: https://pyautogui.readthedocs.io/en/latest/
    def __init__(self, image_shape, fps=30.0):
        pyautogui.FAILSAFE = False
        self.movement_speed = 1.0/fps
        self.screen_width, self.screen_height = pyautogui.size()
        self.width_multiplier = self.screen_width / image_shape[1]
        self.height_multiplier = self.screen_height / image_shape[0]
        self.scroll_multiplier = 10.0
        self.scroll_thresh = 100.0
        self.move_moment = 0.5
        self.scroll_moment = 0.7
        self.move_x = 0.0
        self.move_y = 0.0
        self.scroll_h = 0.0
        self.scroll_v = 0.0

    def right_click(self):
        pyautogui.rightClick()
        return

    def left_doubleclick(self):
        pyautogui.doubleClick()
        return

    def get_position(self):
        return pyautogui.position()

    def vscroll(self, len):
        scroll_len = -len * self.height_multiplier * self.scroll_multiplier
        self.scroll_v = (self.scroll_v * self.scroll_moment) + ((1.0 - self.scroll_moment) * scroll_len)
        if abs(scroll_len) > self.scroll_thresh:
            pyautogui.vscroll(int(self.scroll_v))

    def hscroll(self, len):
        scroll_len = -len * self.width_multiplier * self.scroll_multiplier
        self.scroll_h = (self.scroll_h * self.scroll_moment) + ((1.0 - self.scroll_moment) * scroll_len)
        if abs(scroll_len) > self.scroll_thresh:
            pyautogui.hscroll(int(self.scroll_h))

    def left_click_hold(self):
        pyautogui.mouseDown(button='left')

    def left_click_release(self):
        pyautogui.mouseUp(button='left')

    def move_rel_pos(self, width, height):
        if abs(width) < (self.width_multiplier + 7.0):
            move_x = width
        else:
            move_x = width * (self.width_multiplier + 3.0)

        if abs(height) < (self.height_multiplier + 7.0):
            move_y = height
        else:
            move_y = height * (self.height_multiplier + 3.0)

        self.move_x = (self.move_x * self.move_moment) + ((1.0 - self.move_moment) * move_x)
        self.move_y = (self.move_y * self.move_moment) + ((1.0 - self.move_moment) * move_y)
        pyautogui.move(self.move_x, self.move_y)
        return

    def reset_move(self):
        self.move_x = 0.0
        self.move_y = 0.0

    def reset_scroll(self):
        self.scroll_h = 0.0
        self.scroll_v = 0.0