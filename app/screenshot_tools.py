import pyautogui
import os
import datetime
from typing import Tuple
from dataclasses import dataclass


@dataclass()
class SnipRectangle:
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """calculates the top-left and bottom-right coordinates of the rectangle along with its width and height"""
        x1, x2 = sorted([self.x1, self.x2])
        y1, y2 = sorted([self.y1, self.y2])
        return x1, y1, (x2 - x1), (y2 - y1)


def bounded_screenshot(bounds: Tuple[int, int, int, int]) -> None:
    # Check if the folder exists, create it if not
    snips_directory = "snips"
    if not os.path.exists(snips_directory):
        os.makedirs(snips_directory)

    # Take the screenshot and save it to the folder
    image = pyautogui.screenshot(region=(bounds))
    file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    image.save(os.path.join(snips_directory, f"{file_name}.png"))
