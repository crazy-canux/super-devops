from .element_locator import BaseElement


class WebFrame(BaseElement):
    def __init__(self, **kwargs):
        super(WebFrame, self).__init__(**{'tag': 'iframe'})
        self._kwargs = kwargs

    def activate(self):
        if self._parent and self.exists():
            self._parent.switch_to.frame(self.object)

    def deactivate(self):
        if self._parent:
            self._parent.switch_to_default_content()

    @property
    def current(self):
        if self._locators:
            self._current = None
            _elements = self._find_elements()
            for element in _elements:
                for key, value in self._kwargs.iteritems():
                    if element.get_attribute(key) != value:
                        break
        return self._current

    @property
    def title(self):
        self.deactivate()
        if self.exists():
            return self.object.get_attribute('title')
        return None

    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deactivate()

