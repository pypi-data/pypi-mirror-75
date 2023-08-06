import chromedriver_binary  # noqa --> Organize imports would remove it, but it's necessary
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def get_driver(headless=False):
    """
    Returns the Selenium Browser driver (using Chrome)
    :param headless: Indicate whether Browser Window should be opened
    :type headless: bool
    :return:
    :rtype: selenium.webdriver.chrome.webdriver.WebDriver
    """
    options = Options()
    if headless:
        options.headless = True
    options.add_argument("--no-sandbox")  # We need this to work for the integration tests on the alpine linux image
    driver = webdriver.Chrome(options=options)
    return driver


def wait(driver, seconds):
    try:
        WebDriverWait(driver, seconds).until(lambda driver: 1 == 0)
    except TimeoutException:
        pass
