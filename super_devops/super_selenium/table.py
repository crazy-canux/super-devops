from .element_locator import BaseElement
from selenium.webdriver.remote.webelement import WebElement


class WebTable(BaseElement):
    def __init__(self, **kwargs):
        super(WebTable, self).__init__(**kwargs)

    def get_raw_list(self):
        return self.object.find_elements_by_tag_name("tr")

    def get_text_list(self,
                      xpath=None, class_name=None, name=None, id=None,
                      tag=None, link=None, partial_link=None, css=None):
        text_list = []
        raw_list = self.get_raw_list()
        if len(raw_list[0].find_elements_by_xpath('td')) <= 1:
            return False
        else:
            if xpath:
                text_list = [raw.find_element_by_xpath(xpath).text
                             for raw in raw_list]
            elif class_name:
                text_list = [raw.find_element_by_class_name(class_name).text
                             for raw in raw_list]
            elif name:
                text_list = [raw.find_element_by_name(name).text
                             for raw in raw_list]
            elif id:
                text_list = [raw.find_element_by_id(id).text
                             for raw in raw_list]
            elif tag:
                text_list = [raw.find_element_by_tag_name(tag).text
                             for raw in raw_list]
            elif link:
                text_list = [raw.find_element_by_link_text(link).text
                             for raw in raw_list]
            elif partial_link:
                text_list = [raw.find_element_by_partial_link_text(
                    partial_link).text for raw in raw_list]
            elif css:
                text_list = [raw.find_element_by_selector(css).text
                             for raw in raw_list]
            return text_list
