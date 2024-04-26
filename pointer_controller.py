import pyautogui
import numpy as np


class PointerController:
    # Refrence documentation: https://pyautogui.readthedocs.io/en/latest/
    def __init__(self, image_shape: tuple, fps: float = 30.0):
        """
        Functions to control mouse pointer
        :param image_shape: Input image shape
        :param fps: fps
        """
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
        """
        Perform right short click
        :return:
        """
        pyautogui.rightClick()
        return

    def left_doubleclick(self):
        """
        Perform left double click
        :return:
        """
        pyautogui.doubleClick()
        return

    def get_position(self):
        """
        Get current position
        :return:
        """
        return pyautogui.position()

    def vscroll(self, len: float):
        """
        Perform vertical scroll
        :param len: lenght of scroll
        :return:
        """
        scroll_len = -len * self.height_multiplier * self.scroll_multiplier
        self.scroll_v = (self.scroll_v * self.scroll_moment) + ((1.0 - self.scroll_moment) * scroll_len)
        if abs(scroll_len) > self.scroll_thresh:
            pyautogui.vscroll(int(self.scroll_v))

    def hscroll(self, len: float):
        """
        Perform horizontal scroll
        :param len:
        :return:
        """
        scroll_len = -len * self.width_multiplier * self.scroll_multiplier
        self.scroll_h = (self.scroll_h * self.scroll_moment) + ((1.0 - self.scroll_moment) * scroll_len)
        if abs(scroll_len) > self.scroll_thresh:
            pyautogui.hscroll(int(self.scroll_h))

    def left_click_hold(self):
        """
        Perform left click hold
        :return:
        """
        pyautogui.mouseDown(button='left')

    def left_click_release(self):
        """
        Perform left click release
        :return:
        """
        pyautogui.mouseUp(button='left')

    def move_rel_pos(self, width: float, height:float):
        """
        Relative movement of pointer position
        :param width:
        :param height:
        :return:
        """
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
        """
        Reset pointer positions
        :return:
        """
        self.move_x = 0.0
        self.move_y = 0.0

    def reset_scroll(self):
        """
        Reset scroll positions
        :return:
        """
        self.scroll_h = 0.0
        self.scroll_v = 0.0