import enum
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class ActionType(enum.Enum):
    JUMP = 1
    DUCK = 2
    SHORT_JUMP = 3


class PlayerAgent:
    """class for keeping the canvas element and perform actions and sequences of actions
    on it based on stimulus from the IP and game environment"""

    def __init__(self, driver):
        self.driver = driver

    def hold_key(self, key: Keys, duration: float) -> None:
        """function to hold down a specific key until the duration (in seconds) is not elapsed

        :param key: Keys type object from selenium
        :param duration: time in seconds
        :return None"""
        kd = ActionChains(self.driver).key_down(key)
        ku = ActionChains(self.driver).key_up(key)

        end_time = time.time() + duration
        while True:
            kd.perform()

            if time.time() > end_time:
                ku.perform()
                return

    def __jump(self, duration: float) -> None:
        """function to call the hold_key function for the ARROW_UP key for given amount of time
        which translates in a duck in the game

        :param duration: duration in seconds
        :return: None"""
        self.hold_key(
            key=Keys.ARROW_UP,
            duration=duration
        )

    def __duck(self, duration: float) -> None:
        """function to call the hold_key function for the ARROW_DOWN key for given amount of time
        which translates in a duck in the game

        :param duration: duration in seconds
        :return: None"""
        self.hold_key(
            key=Keys.ARROW_DOWN,
            duration=duration
        )

    def action_sequence(self, action_type: ActionType, duration=0.1) -> None:
        """public function to be used for the agent to interact with the game based on the input from
        the image processing step

        :param action_type: enum which gives action options to the agent
        :param duration: duration in seconds
        :return: None"""
        if action_type == ActionType.JUMP:
            self.__jump(
                duration=duration
            )
        elif action_type == ActionType.DUCK:
            self.__duck(
                duration=duration
            )
        elif action_type == ActionType.SHORT_JUMP:
            self.__jump(
                duration=duration
            )
            self.hold_key(
                key=Keys.NULL,
                duration=0.05
            )
            self.__duck(
                duration=duration
            )
        else:
            pass
