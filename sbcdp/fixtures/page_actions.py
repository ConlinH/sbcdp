"""
Simplified page actions for CDP-Base framework.
Contains only essential CDP-compatible methods.
"""

import time

from . import shared_utils
from ..config import settings


# Define exception classes locally for CDP-Base
class ElementNotInteractableException(Exception):
    pass


class NoSuchElementException(Exception):
    pass


class StaleElementReferenceException(Exception):
    pass


# Define Keys class locally for CDP-Base
class Keys:
    ENTER = "\ue007"
    TAB = "\ue004"
    ESCAPE = "\ue00c"
    SPACE = "\ue00d"
    BACKSPACE = "\ue003"
    DELETE = "\ue017"
    ARROW_UP = "\ue013"
    ARROW_DOWN = "\ue015"
    ARROW_LEFT = "\ue012"
    ARROW_RIGHT = "\ue014"


def __is_cdp_swap_needed(driver):
    """Check if CDP swap is needed"""
    return shared_utils.is_cdp_swap_needed(driver)


def click(driver, selector, timeout=settings.SMALL_TIMEOUT):
    """Click an element"""
    if __is_cdp_swap_needed(driver):
        driver.cdp.click(selector)
        return
    # Fallback for non-CDP mode (if needed)
    element = driver.find_element("css selector", selector)
    element.click()


def type_text(driver, selector, text, timeout=settings.LARGE_TIMEOUT):
    """Type text into an element"""
    if __is_cdp_swap_needed(driver):
        driver.cdp.type(selector, text)
        return
    # Fallback for non-CDP mode (if needed)
    element = driver.find_element("css selector", selector)
    element.clear()
    element.send_keys(text)


def get_text(driver, selector, timeout=settings.LARGE_TIMEOUT):
    """Get text from an element"""
    if __is_cdp_swap_needed(driver):
        return driver.cdp.get_text(selector)
    # Fallback for non-CDP mode (if needed)
    element = driver.find_element("css selector", selector)
    return element.text


def is_element_visible(driver, selector):
    """Check if element is visible"""
    if __is_cdp_swap_needed(driver):
        return driver.cdp.is_element_visible(selector)
    # Fallback for non-CDP mode (if needed)
    try:
        element = driver.find_element("css selector", selector)
        return element.is_displayed()
    except Exception:
        return False


def wait_for_element(driver, selector, timeout=settings.LARGE_TIMEOUT):
    """Wait for element to be present"""
    if __is_cdp_swap_needed(driver):
        return driver.cdp.select(selector)
    # Fallback for non-CDP mode (if needed)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = driver.find_element("css selector", selector)
            if element:
                return element
        except Exception:
            pass
        time.sleep(0.1)
    raise NoSuchElementException(f"Element {selector} not found after {timeout} seconds")


def wait_for_text(driver, text, selector="body", timeout=settings.LARGE_TIMEOUT):
    """Wait for text to appear in element"""
    if __is_cdp_swap_needed(driver):
        driver.cdp.wait_for_text(text, selector)
        return
    # Fallback for non-CDP mode (if needed)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = driver.find_element("css selector", selector)
            if text in element.text:
                return
        except Exception:
            pass
        time.sleep(0.1)
    raise Exception(f"Text '{text}' not found in {selector} after {timeout} seconds")


def assert_element_visible(driver, selector, timeout=settings.SMALL_TIMEOUT):
    """Assert that element is visible"""
    if __is_cdp_swap_needed(driver):
        driver.cdp.assert_element(selector)
        return True
    # Fallback for non-CDP mode (if needed)
    wait_for_element(driver, selector, timeout)
    return True


def assert_text(driver, text, selector="body", timeout=settings.SMALL_TIMEOUT):
    """Assert that text is present in element"""
    if __is_cdp_swap_needed(driver):
        driver.cdp.assert_text(text, selector)
        return True
    # Fallback for non-CDP mode (if needed)
    wait_for_text(driver, text, selector, timeout)
    return True


def get_attribute(driver, selector, attribute, timeout=settings.LARGE_TIMEOUT):
    """Get attribute value from element"""
    if __is_cdp_swap_needed(driver):
        return driver.cdp.get_attribute(selector, attribute)
    # Fallback for non-CDP mode (if needed)
    element = wait_for_element(driver, selector, timeout)
    return element.get_attribute(attribute)


def scroll_to_element(driver, selector):
    """Scroll to element"""
    if __is_cdp_swap_needed(driver):
        driver.cdp.scroll_to_element(selector)
        return
    # Fallback for non-CDP mode (if needed)
    element = driver.find_element("css selector", selector)
    driver.execute_script("arguments[0].scrollIntoView();", element)


def sleep(seconds):
    """Sleep for specified seconds"""
    time.sleep(seconds)


# Simplified method aliases for compatibility
send_keys = type_text
update_text = type_text
press_keys = type_text
clear = lambda driver, selector: type_text(driver, selector, "")
