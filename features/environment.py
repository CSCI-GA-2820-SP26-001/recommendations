"""
Environment for Behave Testing
"""

from os import getenv
from selenium import webdriver
import requests

WAIT_SECONDS = int(getenv("WAIT_SECONDS", "30"))
BASE_URL = getenv("BASE_URL", "http://localhost:8000")
DRIVER = getenv("DRIVER", "chrome").lower()


def before_all(context):
    """Executed once before all tests"""
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS
    # Select either Chrome or Firefox
    if "firefox" in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()
    context.driver.implicitly_wait(context.wait_seconds)
    context.driver.set_window_size(1280, 1300)
    context.config.setup_logging()


def after_all(context):
    """Executed after all tests"""
    context.driver.quit()


def before_scenario(context, scenario):
    """Executed before each scenario — clears the database"""
    try:
        response = requests.get(f"{context.base_url}/recommendations")
        if response.status_code == 200:
            recommendations = response.json()
            for rec in recommendations:
                requests.delete(f"{context.base_url}/recommendations/{rec['id']}")
            print(f"\nCleared {len(recommendations)} recommendations before scenario")
        else:
            print(f"\nFailed to get recommendations: {response.status_code}")
    except Exception as e:
        print(f"\nError clearing database: {e}")


######################################################################
# Utility functions to create web drivers
######################################################################


def get_chrome():
    """Creates a headless Chrome driver"""
    print("Running Behave using the Chrome driver...\n")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.binary_location = "/usr/bin/chromium"
    service = webdriver.ChromeService(executable_path="/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)


def get_firefox():
    """Creates a headless Firefox driver"""
    print("Running Behave using the Firefox driver...\n")
    options = webdriver.FirefoxOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)
