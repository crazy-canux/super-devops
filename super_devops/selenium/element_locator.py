import logging

from selenium.webdriver.remote.webelement import WebElement

from .wait import Wait
from super_devops.robotframework.cache import Cache


logger = logging.getLogger(__name__)
logging.getLogger('selenium').setLevel(logging.WARNING)


class BaseElement(object):

    """Customize element locator for super-devops."""

    strategies = {
        'ID': 'find_element_by_id',
        'NAME': 'find_element_by_name',
        'CLASS': 'find_element_by_class_name',
        'TAG': 'find_element_by_tag_name',
        'LINK': 'find_element_by_link_text',
        'PARTIAL': 'find_element_by_partial_link_text',
        'XPATH': 'find_element_by_xpath',
        'CSS': 'find_element_by_selector'
    }

    def __init__(self, parent=None, element=None, **kwargs):
        self._element = element if element else None
        self._parent = parent if parent else Cache().current
        self._current = None
        self._locators = None

        if self._element:
            if hasattr(self._element, 'parent'):
                self._parent = self._element.parent
            if hasattr(self._element, 'current'):
                self._current = self._element.current

        if not self._current:
            if self._element and isinstance(self._element, WebElement):
                self._current = self._element
            elif not kwargs:
                raise ValueError('Unable to initialize the WebElement.')
            else:
                self._locators = self._parse_kwargs(**kwargs)

    @property
    def current(self):
        if self._locators:
            _elements = self._find_elements()
            self._current = _elements[0] if _elements else None
        else:
            self._current = self._current
        return self._current

    @property
    def parent(self):
        return self._parent

    @property
    def object(self):
        return self._current or self.current

    def activate(self):
        if self._parent and self.exists():
            self._parent.execute_script(
                'arguments[0].focus();', self.object
            )

    def exists(self, timeout=30):
        try:
            Wait(self._parent, timeout).synchronize_animations()
        except Exception:
            pass
        finally:
            _visible = False
            try:
                _visible = self.object.is_displayed() if self.current else \
                    False
            except Exception:
                pass
        return _visible

    def _parse_kwargs(self, **kwargs):
        locators = []
        for key, value in kwargs.iteritems():
            key = str(key).upper().strip()
            value = str(value).strip()
            if key in BaseElement.strategies:
                locators.append([BaseElement.strategies.get(key), value])
        if not locators:
            raise ValueError('WebElement locator error.')
        return locators

    def _find_elements(self):
        _elements = []
        for key, value in self._locators:
            _invoker = None
            if hasattr(self._parent, key):
                _invoker = getattr(self._parent, key)
            if _invoker and callable(_invoker):
                _elements.append(
                    self._normalize_result(_invoker(value))
                )
        return _elements

    def _normalize_result(self, elements):
        if elements is not basestring or elements is not str:
            return elements
        else:
            return []
