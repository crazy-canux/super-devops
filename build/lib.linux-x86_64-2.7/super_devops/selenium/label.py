from .element_locator import BaseElement


class WebLabel(BaseElement):
    def __init__(self, **kwargs):
        super(WebLabel, self).__init__(**kwargs)

    @property
    def value(self):
        if self.exists():
            return self.object.text
        return None
