"""
Simplified JavaScript utilities for CDP-Base framework.
Contains only essential JavaScript execution methods.
"""

import time
from contextlib import suppress
from ..config import settings


# Define By constants locally for CDP-Base
class By:
    CSS_SELECTOR = "css selector"
    CLASS_NAME = "class name"
    ID = "id"
    NAME = "name"
    LINK_TEXT = "link text"
    XPATH = "xpath"
    TAG_NAME = "tag name"
    PARTIAL_LINK_TEXT = "partial link text"


# Define exception classes locally for CDP-Base
class NoSuchElementException(Exception):
    pass

class WebDriverException(Exception):
    pass


def execute_script(driver, script, *args):
    """Execute JavaScript code"""
    try:
        return driver.execute_script(script, *args)
    except Exception as e:
        raise WebDriverException(f"JavaScript execution failed: {e}")


def execute_async_script(driver, script, timeout=None, *args):
    """Execute asynchronous JavaScript code"""
    if not timeout:
        timeout = settings.LARGE_TIMEOUT
    try:
        return driver.execute_async_script(script, *args)
    except Exception as e:
        raise WebDriverException(f"Async JavaScript execution failed: {e}")


def convert_to_css_selector(selector, by=By.CSS_SELECTOR):
    """Convert selector to CSS selector format"""
    if by == By.CSS_SELECTOR:
        return selector
    elif by == By.ID:
        return f"#{selector}"
    elif by == By.CLASS_NAME:
        return f".{selector}"
    elif by == By.NAME:
        return f'[name="{selector}"]'
    elif by == By.TAG_NAME:
        return selector
    elif by == By.XPATH:
        # For CDP-Base, we'll use a simple conversion
        # More complex XPath conversion would require additional libraries
        if selector.startswith("//"):
            # Simple conversion for common XPath patterns
            if selector.startswith("//div"):
                return "div"
            elif selector.startswith("//span"):
                return "span"
            elif selector.startswith("//input"):
                return "input"
            elif selector.startswith("//button"):
                return "button"
            elif selector.startswith("//a"):
                return "a"
        return selector  # Return as-is if conversion not possible
    elif by == By.LINK_TEXT:
        return f'a:contains("{selector}")'
    elif by == By.PARTIAL_LINK_TEXT:
        return f'a:contains("{selector}")'
    else:
        raise Exception(f"Could not convert {selector}(by={by}) to CSS_SELECTOR!")


def is_valid_by(by):
    """Check if 'by' parameter is valid"""
    return by in [
        "css selector", "class name", "id", "name",
        "link text", "xpath", "tag name", "partial link text",
    ]


def swap_selector_and_by_if_reversed(selector, by):
    """Swap selector and by if they appear to be reversed"""
    if not is_valid_by(by) and is_valid_by(selector):
        selector, by = by, selector
    return (selector, by)


def wait_for_ready_state_complete(driver, timeout=None):
    """Wait for page to be in ready state"""
    if not timeout:
        timeout = settings.LARGE_TIMEOUT

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            ready_state = execute_script(driver, "return document.readyState")
            if ready_state == "complete":
                return True
        except Exception:
            pass
        time.sleep(0.1)
    return False


def wait_for_jquery_active(driver, timeout=None):
    """Wait for jQuery to be active (simplified)"""
    if not timeout:
        timeout = 2

    for _ in range(int(timeout * 10)):
        try:
            execute_script(driver, "return jQuery")
            return True
        except Exception:
            time.sleep(0.1)
    return False


def is_jquery_activated(driver):
    """Check if jQuery is activated"""
    try:
        execute_script(driver, "return jQuery")
        return True
    except Exception:
        return False


def activate_jquery(driver):
    """Activate jQuery (simplified version)"""
    if is_jquery_activated(driver):
        return

    # Simple jQuery injection
    jquery_script = """
    if (typeof jQuery === 'undefined') {
        var script = document.createElement('script');
        script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
        document.head.appendChild(script);
    }
    """
    execute_script(driver, jquery_script)

    # Wait for jQuery to load
    wait_for_jquery_active(driver, timeout=5)


def are_quotes_escaped(string):
    if string.count("\\'") != string.count("'") or (
        string.count('\\"') != string.count('"')
    ):
        return True
    return False


def escape_quotes_if_needed(string):
    """re.escape() works differently in Python 3.7.0 than earlier versions:

    Python 3.6.5:
    >>> import re
    >>> re.escape('"')
    '\\"'

    Python 3.7.0:
    >>> import re
    >>> re.escape('"')
    '"'

    SeleniumBase needs quotes to be properly escaped for Javascript calls.
    """
    if are_quotes_escaped(string):
        if string.count("'") != string.count("\\'"):
            string = string.replace("'", "\\'")
        if string.count('"') != string.count('\\"'):
            string = string.replace('"', '\\"')
    return string


def highlight_element_with_js(driver, element, loops=4, o_bs=""):
    """Highlight element using JavaScript"""
    script = """
    var element = arguments[0];
    var loops = arguments[1];
    var originalBoxShadow = arguments[2];

    for (var i = 0; i < loops; i++) {
        setTimeout(function() {
            element.style.boxShadow = '0px 0px 6px 6px rgba(128, 128, 128, 0.5)';
        }, i * 150);
        setTimeout(function() {
            element.style.boxShadow = originalBoxShadow;
        }, (i * 150) + 75);
    }
    """
    execute_script(driver, script, element, loops, o_bs)


def scroll_to_element(driver, element):
    """Scroll to element using JavaScript"""
    script = "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});"
    execute_script(driver, script, element)


def click_element_with_js(driver, element):
    """Click element using JavaScript"""
    script = "arguments[0].click();"
    execute_script(driver, script, element)


def get_element_text(driver, element):
    """Get element text using JavaScript"""
    script = "return arguments[0].textContent || arguments[0].innerText;"
    return execute_script(driver, script, element)


def set_element_value(driver, element, value):
    """Set element value using JavaScript"""
    script = """
    var element = arguments[0];
    var value = arguments[1];
    element.value = value;
    element.dispatchEvent(new Event('input', {bubbles: true}));
    element.dispatchEvent(new Event('change', {bubbles: true}));
    """
    execute_script(driver, script, element, value)


def remove_element(driver, element):
    """Remove element from DOM using JavaScript"""
    script = "arguments[0].remove();"
    execute_script(driver, script, element)


def get_page_title(driver):
    """Get page title using JavaScript"""
    return execute_script(driver, "return document.title;")


def get_current_url(driver):
    """Get current URL using JavaScript"""
    return execute_script(driver, "return window.location.href;")


def refresh_page(driver):
    """Refresh page using JavaScript"""
    execute_script(driver, "window.location.reload();")


def go_back(driver):
    """Go back in browser history using JavaScript"""
    execute_script(driver, "window.history.back();")


def go_forward(driver):
    """Go forward in browser history using JavaScript"""
    execute_script(driver, "window.history.forward();")


# Simplified method aliases for compatibility
add_js_link = lambda driver, js_link: None  # Simplified - not needed for CDP
add_css_link = lambda driver, css_link: None  # Simplified - not needed for CDP
add_meta_tag = lambda driver, http_equiv=None, content=None: None  # Simplified
