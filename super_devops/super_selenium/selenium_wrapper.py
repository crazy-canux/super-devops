import logging

from selenium import webdriver

from .wait import Wait
from super_devops.robotframework.cache import Cache


logger = logging.getLogger(__name__)
logging.getLogger('selenium').setLevel(logging.WARNING)


class BaseSelenium(object):

    """Create driver by the browser name specify in configuration.

    browser = BaseSelenium(browser_id, browser_type, wait_time_in_sec)
    browser.launch(url)
    browser.maximize_window()
    browser.close()
    """

    BROWSER_NAME = {
        'firefox': '_make_firefox',
        'chrome': '_make_chrome',
        'edge': '_make_edge',
        'ie': '_make_ie',
        'opera': '_make_opera',
        'safari': '_make_safari'
    }

    def __init__(
            self,
            browser_id, browser_type, headless_mode=False,
            wait_time_in_secs=30
    ):
        self.headless_mode = headless_mode

        self._driver = None
        self._cache = Cache(browser_id)

        if not str(wait_time_in_secs).isdigit():
            self._implicit_wait = 30
        else:
            self._implicit_wait = wait_time_in_secs

        self._cache.register(self._make_browser(browser_type))

    @property
    def current(self):
        if not (self._driver or self._cache.current):
            raise RuntimeError('No browser opened.')
        return self._driver or self._cache.current

    def _make_browser(self, browser_type):
        invoker = getattr(
            self,
            BaseSelenium.BROWSER_NAME.get(browser_type.lower())
        )

        if callable(invoker):
            self._driver = invoker()
            self._driver.get('about:blank')
            self._driver.implicitly_wait(self._implicit_wait)
        else:
            raise RuntimeError('Not a valid browser type.')

        return self._driver

    def _make_firefox(self):
        """Make sure the firefox driver in $PATH."""
        if self.headless_mode:
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=options)
        else:
            driver = webdriver.Firefox()
        return driver

    def _make_chrome(self):
        """Make sure the chrome driver in $PATH."""
        if self.headless_mode:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(chrome_options=options)
        else:
            driver = webdriver.Chrome()
        return driver

    def launch(self, url='about:blank'):
        """Recover get method for driver and do a smart wait."""
        self.current.get(url)
        Wait(self._driver, self._implicit_wait).synchronize_page_loading()

    def maximize_window(self):
        self.current.maximize_window()

    def close(self):
        """Close one tag."""
        self._cache.close()
        self._driver = None
