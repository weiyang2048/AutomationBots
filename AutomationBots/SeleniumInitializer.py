from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from loguru import logger


def initialize_selenium_driver(
    username, password, url="https://www.linkedin.com/login"
):
    """
        Initialize Chrome driver and log in to LinkedIn.

        Args:
            username (str): LinkedIn username/email
            password (str): LinkedIn password
            url (str): LinkedIn login page URL

        Returns:
            webdriver: Selenium webdriver instance with active LinkedIn session

    # Examples:
    driver = initialize_selenium_driver(os.getenv("linkedin_user"), os.getenv("linkedin_pass"))

    driver = initialize_selenium_driver(
        os.getenv("robinhood_user"),
        os.getenv("robinhood_pass"),
        url="https://www.robinhood.com/login",
    )
    """
    logger.info("Initializing Chrome driver")

    # Set up Chrome options
    options = Options()
    options.add_argument("--start-maximized")

    # Initialize Chrome with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Log in to LinkedIn
    logger.info(f"Navigating to {url}")
    driver.get(url)

    # Wait for page to load
    time.sleep(2)

    # Find and fill login form
    try:
        username_field = driver.find_element(By.ID, "username")
    except:
        username_field = driver.find_element(By.NAME, "username")
    try:
        password_field = driver.find_element(By.ID, "password")
    except:
        password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit login
    logger.info("Submitting login credentials")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for login to complete
    time.sleep(5)
    logger.info("Login completed")

    return driver
