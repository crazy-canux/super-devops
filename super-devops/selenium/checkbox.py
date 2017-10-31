from .element_locator import BaseElement


class WebCheckbox(BaseElement):
    def __init__(self, **kwargs):
        super(WebCheckbox, self).__init__(**kwargs)

    @property
    def state(self):
        if self.exists():
            return self.object.is_enabled() and bool(
                self.object.get_attribute('checked')
            )
        return False

    def toggle(self):
        self.current.click()

    def tick(self):
        self.__set()

    def untick(self):
        self.__set(on=False)

    def __set(self, on=True):
        if self.exists(5) and (self.state != on):
            self.toggle()
