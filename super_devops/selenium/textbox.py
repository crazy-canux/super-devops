from .element_locator import BaseElement


class WebTextbox(BaseElement):

    """Customize for html-input tag."""

    def __init__(self, **kwargs):
        super(WebTextbox, self).__init__(**kwargs)

    def set(self, value=None):
        if not self.exists():
            raise RuntimeError('WebTextbox is not displayed')
        self.object.clear()
        self.object.send_keys(value)
        return self.object.get_attribute('value')

    @property
    def value(self):
        if self.exists():
            return self.object.text
        return None

    @property
    def is_read_only(self):
        if self.exists():
            return not self.object.is_enabled()
        return False
