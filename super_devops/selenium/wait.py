import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from super_devops.robotframework.cache import Cache


logger = logging.getLogger(__name__)
logging.getLogger('selenium').setLevel(logging.WARNING)


class Wait(object):

    """Customize wait action based on WebDriverWait for super-devops."""

    def __init__(self, driver=None, timeout=30.0, poll_frequency=1.0):
        self._driver = driver or Cache().current

        try:
            self._timeout = float(timeout)
            self._poll_frequency = float(poll_frequency)
        except Exception:
            self._timeout = 30.0
            self._poll_frequency = 1.0

    def synchronize_page_loading(self):
        try:
            WebDriverWait(
                self._driver, self._timeout, self._poll_frequency
            ).until(
                lambda s: s.execute_script(
                    'return document.readyState=="complete";'
                ),
                'Fail to wait until page fully loaded in {}'.format(
                    self._timeout
                )
            )
        except TimeoutException as e:
            raise e

    def synchronize_animations(self):
        """
        Waits until the asynchronous ajax animation complete

        Fails if `timeout_in_secs` expires before the element is enabled. See
        `introduction` for more information about `timeout_in_secs` and its
        default value.
        """
        xmlhttp_animation_script = 'return (window.xmlhttp.readyState == 4 && window.xmlhttp.status == 200);'
        jquery_animation_script = 'return (window.jQuery.active==0);'
        prototype_animation_script = 'return (window.Ajax.activeRequestCount==0);'
        dojo_animation_script = 'return (window.dojo.io.XMLHTTPTransport.inFlight.length==0);'
        angular_animation_script = 'return window.angular.element(document.body)' \
                                   '.injector().get("$http").pendingRequests.length==0;'

        animation_script_pairs = {
            'xmlhttp': xmlhttp_animation_script,
            'jQuery': jquery_animation_script,
            'Ajax': prototype_animation_script,
            'dojo': dojo_animation_script,
            'angular': angular_animation_script
        }

        for key, value in animation_script_pairs.iteritems():
            result = bool(
                self._driver.execute_script(
                    'if(window.{}) return true; else return false;'.format(key)
                )
            )

            if result:
                try:
                    WebDriverWait(
                        self._driver, self._timeout, self._poll_frequency
                    ).until(
                        lambda exp: exp.execute_script(value),
                        'Fail to wait until animation complete in {} seconds'.format(
                            self._timeout
                        )
                    )
                except TimeoutException as ex:
                    raise ex
