.. _selenium:

selenium
========

selenium只有两个包webdriver和common.

install
-------

install from pypi::

    $ pip install selenium

usage
-----

selenium.webdriver::

    from selenium import webdriver

    # 返回WebDriver类型的对象．
    driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    driver = webdriver.Edge()
    driver = webdriver.Ie()
    driver = webdriver.Opera()
    driver = webdriver.Safari()

selenium.webdriver.firefox.webdriver.WebDriver::

    # selenium.webdriver.[browser].webdriver.WebDriver 是 selenium.webdriver.remote.webdriver.WebDriver 的子类.

    # methods:
    context(*args, **kwds)
    quit(self)
    set_context(self, context)
    # data descriptor
    firefox_profile

selenium.webdriver.chrome.webdriver.WebDriver::

    # methods:
    create_options(self)
    launch_app(self, id)
    quit(self)

selenium.webdriver.firefox.webelement.FirefoxWebElement::

    # selenium.webdriver.firefox.webelement.FirefoxWebElement 是 selenium.webdriver.remote.webelement.WebElement 的子类．

    # methods:
    find_anonymous_element_by_attribute(self, name, value)

    # data descriptor:
    anonymous_children

selenium.webdriver.remote.webdriver::

    from selenium.webdriver.remote.webdriver import WebDriver

    # methods:
    add_cookie(self, cookie_dict)
    back()
    create_web_element(element_id)
    delete_all_cookies()
    delete_cookie()
    execute(driver_command, params=None)
    execute_async_script(script, *args)
    execute_script(self, script, *args)
    # execute_script('arguments[0].focus();', elem) # 获取elem的焦点
    file_detector_context(*args, **kwds)
    forward()
    implicitly_wait(self, time_to_wait) # 隐式等待一个元素被找到．
    maximize_window() # 最大化窗口
    close() # 关闭一个标签
    quit() # 退出整个浏览器
    refresh()
    save_screenshot(filename)
    start_client()
    start_session(capabilities, browser_profile=None)
    stop_client()
    switch_to_active_element()
    switch_to_alert()
    switch_to_default_content()
    switch_to_frame(frame_reference)
    switch_to_window(widow_name)

    get("http://www.google.com")
    get_cookie(name)
    get_cookies()
    get_log(log_type)
    get_screenshot_as_base64()
    get_screenshot_as_file(filename)
    get_screenshot_as_png()
    get_window_position(windowHandle='current')
    get_window_rect()
    get_window_size(windowHandle='current')

    set_page_load_timeout(time_to_wait)

    # 定位元素的16个方法
    find_element_by_***()
    elem = driver.find_element_by_id()
    elem = driver.find_element_by_name()
    elem = driver.find_element_by_class_name()
    elem = driver.find_element_by_tag_name
    elem = driver.find_element_by_link_text
    elem = driver.find_element_by_partial_link_text
    elem = driver.find_element_by_xpath()
    elem = driver.find_element_by_css_selector()
    find_elements_by_***()

    # data descriptors:
    application_cache
    current_url
    current_window_handle # 当前窗口的句柄
    desired_capabilities
    file_detector
    log_types
    mobile
    name
    orientation
    page_source
    switch_to
    title
    window_handles

selenium.webdriver.remote.webelement::

    from selenium.webdriver.remote.webelement import WebElement

    # methods:
    elem.click() # 点击按钮．
    elem.clear() # 清空文本输入框．
    elem.send_keys(self, *value) # 给文本框输入内容，比如用户名密码，搜索框等．
    elem.get_attribute(self, name)
    elem.get_property(self, name)
    elem.is_displayed(self) # 元素对用户可见
    elem.is_enabled(self)
    elem.is_selected(self)
    elem.screenshot(self, filename)
    elem.submit(self)
    elem.value_of_css_property(self, property_name)

    # data descriptor:
    id
    location
    location_once_scrolled_into_view
    parent
    rect
    screenshot_as_base64
    screenshot_as_png
    size
    tag_name
    text

selenium.webdriver.support::

    # 处理select标签:
    from selenium.webdriver.support.select import Select
    Select(self, webelement)
    deselect_all(self)
    deselect_by_value(self, value)
    deselect_by_visible_text(self, text)
    select_by_index(self, index)
    select_by_value(self, value)
    select_by_visible_text(self, text)

    # 处理等待页面加载：
    from selenium.webdriver.support.ui import WebDriverWait
    # 用于显示等待, 注意method的参数是driver.
    WebDriverWait(driver, timeout, poll_frequency=0.5, ignored_exceptions=None)
    WebDriverWait.until(self, method, message='') # 调用method(driver)直到返回True, 失败返回message.
    WebDriverWait.until_not(self, method, message='')

selenium.webdriver.common::

    from selenium.webdriver.common.keys import Keys

    from selenium.webdriver.common.action_chains import ActionChains

    from selenium.webdriver.common.by import By

selenium.common::

    common.exception包括了所有的异常．

    from selenium.common.exceptions import TimeoutException # 等待超时
    from selenium.common.exceptions import NoSuchElementException

firefox headless::

    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.add_argument('--headless')
    driver = Firefox(firefox_options=options)

chrome headless::

    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument('--headless')
    driver = Chrome(chrome_options=options)

examples::

    try:
        wait = WebDriverWait(driver, 10, 1.0)
        wait.until(lambda s: s.execute_script(
            'return document.readyState=="complete";'),
            'Fail to wait page full loaded.')
    except TimeoutException as e:
        raise e
    finally:
        driver.quit()


