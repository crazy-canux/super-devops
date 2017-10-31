from selenium.webdriver.support.select import Select

from .element_locator import BaseElement


class WebCombo(BaseElement):

    """Customize for html-select tag."""

    def __init__(self, **kwargs):
        super(WebCombo, self).__init__(**kwargs)
        self._list = None

    def select(self, index=None, value='', visible_text=''):
        if not self.exists():
            raise RuntimeError('Failed to locate the webcombo')
        if index:
            self._list.select_by_index(index)
        elif value.strip():
            self._list.select_by_value(value.strip())
        elif visible_text.strip():
            self._list.select_by_visible_text(visible_text.strip())
        else:
            raise ValueError('Failed to select the tag.')

    @property
    def current(self):
        if super(WebCombo, self).current:
            self._list = Select(self._current)
        return self._current

    @property
    def can_select_multiple(self):
        if self.exists():
            return self.object.is_multiple
        return False

    def items(self):
        __selection_items = []
        if self.exists():
            __selection_items = self._list.options
        return __selection_items

    def get_items_count(self):
        if self.items():
            return len(self.items())
        return 0
