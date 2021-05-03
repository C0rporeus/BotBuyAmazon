from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from msedge.selenium_tools import Edge, EdgeOptions
from random import randint, randrange
import time
import random

AMAZON_TEST_URL = 'https://www.amazon.com/MSI-GeForce-RTX-3060-12G/dp/B08WPRMVWB'

WAIT_TIME = 5
PRICE_LIMIT = 700.00


class YonaShop:
    def __init__(self, username, password):
        """ Initializes Bot with class-wide variables. """
        self.username = username
        self.password = password
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument('-inprivate')
        self.driver = Edge(
            executable_path='C:/Users/jhony/Downloads/edgedriver/msedgedriver.exe', options=options)

    # Sign into site with the product
    def signIn(self):
        """ Sign into site with the product. """

        driver = self.driver  # Navigate to URL

        # Enter Username
        username_elem = driver.find_element_by_xpath("//input[@name='email']")
        username_elem.clear()
        username_elem.send_keys(self.username)

        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
        username_elem.send_keys(Keys.RETURN)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        # Enter Password
        password_elem = driver.find_element_by_xpath(
            "//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)

        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
        password_elem.send_keys(Keys.RETURN)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

    # Find product under X amount
    def findProduct(self):
        """ Finds the product with global link. """
        driver = self.driver
        driver.get(AMAZON_TEST_URL)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        # If the product is not available, wait until it is available
        isAvailable = self.isProductAvailable()

        if isAvailable == 'No disponible por el momento.':
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
            self.findProduct()
        elif isAvailable <= PRICE_LIMIT:
            # Buy Now
            buy_now = driver.find_element_by_name('submit.buy-now')
            buy_now.click()
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
            self.signIn()
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

            # Place Order
            place_order_text = driver.find_element_by_name(
                'placeYourOrder1').text
            place_order = driver.find_element_by_name('placeYourOrder1')
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
            print(f'***** ORDENADO: {place_order_text}')
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
            place_order.click()
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        else:
            time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))
            self.findProduct()

    def isProductAvailable(self):
        """ Checks if product is available. """
        driver = self.driver
        available = driver.find_element_by_class_name('a-color-price').text
        if available == 'No disponible por el momento.':
            print(f'***** ESTADO - STATUS: {available}')
            return available
        else:
            print(f'***** PRECIO - PRICE: {available}')
            return float(available[6:])  # $123.22 -> 123.22

    def closeBrowser(self):
        """ Closes browser """
        self.driver.close()


if __name__ == '__main__':
    shopBot = YonaShop(username="username_amazon",
                       password="password")
    shopBot.findProduct()
    shopBot.closeBrowser()
