from collections import deque
from configparser import ConfigParser

import matplotlib.pyplot as plt
import pytesseract
from PIL import Image


class GameCanvasQueue:
    """data structure class holding the last 3 canvas images from the game"""

    def __init__(self, max_len=3):
        # queue keeping only the last <max_len> elements => short term memory
        self.q = deque(
            maxlen=max_len
        )

    def append(self, val: Image) -> None:
        """append an image to the queue while keeping the constant length based on the queue data strucutre

        :param val: an image object
        :return: None"""
        self.q.append(val)


class CanvasProcessing:
    """class for working with the IP part of the canvas image in order to extract information from
    the game"""

    def __init__(self):
        config = ConfigParser()
        config.read('env_config.ini')

        pytesseract.pytesseract.tesseract_cmd = config['ENV']['tesseract_path']

    @staticmethod
    def __extract_region(canvas: Image, roi: tuple) -> Image:
        """function to crop the canvas image in the given region of interest in the format
        (top-left_X, top-left_Y, bottom-right_X, bottom-right_Y) and return items

        :param canvas: Image of the game
        :param roi: tuple giving the region of interest
        :return: cropped region of interest"""
        # CanvasProcessing.visualize(canvas.crop(roi))
        return canvas.crop(
            roi
        )

    def extract_score(self, canvas: Image) -> int:
        """function to use the region extraction and OCR\tesseract in order to extract the
        player score as a number, and if not possible, return 0

        :param canvas: Image of the game
        :return: integer score"""
        score_roi = self.__extract_region(
            canvas,
            roi=(530, 5, 590, 25)
        )
        score_text = pytesseract.image_to_string(
            score_roi,
            lang='eng'
        )

        try:
            score = int(score_text)
        except ValueError:
            score = 0
        return score

    def is_game_over(self, canvas: Image) -> bool:
        """function to use the region extraction and OCR\tesseract in order to determine
        whether the game over screen is present by checking a desired region for game over
        text and looking for at least half of the letters present in the text from the region

        :param canvas: Image of the game
        :return: truth value of the game over screen being presented on the canvas"""
        game_over_roi = self.__extract_region(
            canvas,
            roi=(200, 40, 400, 55)
        )
        game_over_text = pytesseract.image_to_string(
            game_over_roi,
            lang='eng',
            config='--psm 10 --oem 3 -c tessedit_char_whitelist=GAMEOVER'
        )
        # print(game_over_text)
        game_over = 'GAMEOVER'
        return sum([ch in game_over_text for ch in list(game_over)]) > len(game_over) // 2

    @staticmethod
    def visualize(img: Image):
        """helper function to show the given image using matplotlib.pyplot

        :param img: any image
        :return: None"""
        plt.imshow(img)
        plt.show()
