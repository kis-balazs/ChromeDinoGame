import base64
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from image_processing import CanvasProcessing
from image_processing import GameCanvasQueue
from player import ActionType
from player import PlayerAgent


class ChromeDinoGame:
    """class for interacting with the game. Uses:
        - image_processing/GameCanvasQueue
        - image_processing/CanvasProcessing
        - player/PlayerAgent"""
    GAME_URL = 'https://chromedino.com/'
    GAME_CANVAS_XPATH = '//*[@id="main-frame-error"]/div[2]/canvas'
    CANVAS_EXTRACT_SCRIPT = 'return arguments[0].toDataURL("image/png").substring(21);'

    def __init__(self):
        # #################################
        # game-related
        self.game_over = False
        self.score = 0

        # #################################
        # options for the driver to clean the log output & disable notifications
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option(
            "prefs",
            prefs
        )
        options.add_experimental_option(
            'excludeSwitches',
            ['enable-logging']
        )

        # the driver which will be assigned to the game to perform operations on it
        self.driver = webdriver.Chrome(
            options=options
        )
        # initialization sequence of navigating to the game
        self.__navigate_game_link()

        # #################################
        # variable to hold the last three canvas images from the game
        self.gcq = GameCanvasQueue()
        # class for image processing on canvas images
        self.cp = CanvasProcessing()
        # class for the player agent
        self.pa = PlayerAgent(
            driver=self.driver
        )

    def __navigate_game_link(self) -> None:
        """function to navigate to the free game link

        :return: None"""
        self.driver.get(
            ChromeDinoGame.GAME_URL
        )

    def __get_game_canvas_object(self) -> WebElement:
        """function to return the WebElement of the canvas

        :return: WebElement object"""
        return self.driver.find_element_by_xpath(
            ChromeDinoGame.GAME_CANVAS_XPATH
        )

    def __get_game_canvas(self) -> Image:
        """create an PIL.Image about the canvas of the t-rex game, and return it as an image object

        :return: Image of the canvas, i.e. a screenshot"""
        canvas = self.__get_game_canvas_object()

        # get the canvas as a PNG base64 string
        canvas_base64 = self.driver.execute_script(
            ChromeDinoGame.CANVAS_EXTRACT_SCRIPT,
            canvas
        )

        # decode
        return Image.open(
            BytesIO(base64.b64decode(canvas_base64))
        )

    def game(self) -> None:
        """function to simulate the actual play of the game by checking the game-over screen and
        performing image processing & using an agent to play based on the state of the canvas

        :return: None"""
        # start game move
        self.pa.action_sequence(
            ActionType.JUMP
        )

        canvas_image = self.__get_game_canvas()
        while not self.game_over:
            canvas_image = self.__get_game_canvas()
            self.gcq.append(canvas_image)

            # verification of game state
            self.game_over = self.cp.is_game_over(
                canvas_image
            )

            if self.game_over:
                break

            # --- uncomment if intermediary score needed ---
            self.score = self.cp.extract_score(
                canvas_image
            )
            print("Intermediary score:", self.score)

            # #######
            # IP & scenario categorization
            action_type = ActionType.SHORT_JUMP

            # #######
            # actions
            self.pa.action_sequence(
                action_type=action_type
            )

        # take final score => TODO make use of the gcq in order to take more score samples!!!
        self.score = self.cp.extract_score(
            canvas_image
        )
        print('You died, score: {}'.format(self.score))
        return

    def close(self) -> None:
        """function to close the driver's window for easy re-usability of the code

        :return: None"""
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    dino = ChromeDinoGame()

    try:
        dino.game()
    except Exception as e:
        print(e)
