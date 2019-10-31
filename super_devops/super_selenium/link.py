from .element_locator import BaseElement


class WebLink(BaseElement):
    def __init__(self, **kwargs):
        super(WebLink, self).__init__(**kwargs)

    def click(self):
        self.current.click()

    @property
    def text(self):
        if self.exists():
            return self.object.text
        return None

    @property
    def enabled(self):
        if self.exists():
            return self.object.is_enabled()
        return False

    @property
    def is_read_only(self):
        if self.exists():
            return not self.object.is_enabled()
        return False