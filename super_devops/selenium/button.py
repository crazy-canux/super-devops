from .element_locator import BaseElement


class WebButton(BaseElement):
    def __init__(self, **kwargs):
        super(WebButton, self).__init__(**kwargs)

    def click(self):
            self.current.click()

    @property
    def enabled(self):
        if self.exists():
            return self.object.is_enabled()
        return False