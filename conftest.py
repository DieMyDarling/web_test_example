import os

import pytest
from dotenv import load_dotenv
from selene.api import *
from selenium import webdriver
from tools import attach


def pytest_addoption(parser):
    parser.addoption(
        '--browser-version',
        help='Версия браузера в которой будут запущены тесты',
        default='100.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version_from_cmd = request.config.getoption('--browser-version')
    browser_version = browser_version_from_cmd or '100.0'
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--enable-automation')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--headless')
    options.browser_version = '100.0'
    selenoid_capability = {
        'browserName': 'chrome',
        'browserVersion': '100.0',
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': True
        }
    }

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    remote_browser_url = os.getenv('REMOTE_BROWSER_URL')

    options.capabilities.update(selenoid_capability)
    driver = webdriver.Remote(
        command_executor=f'https://{login}:{password}@{remote_browser_url}',
        options=options)

    browser.config.driver = driver
    browser.config.window_height = 1920
    browser.config.window_width = 1080
    browser.config.timeout = 4.0
    browser.config.base_url = ''

    yield

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()
