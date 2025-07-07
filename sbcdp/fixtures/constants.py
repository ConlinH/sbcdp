"""CDP-Base constants - simplified version"""


class UC:
    RECONNECT_TIME = 2.4  # Seconds
    CDP_MODE_OPEN_WAIT = 0.9  # Seconds
    EXTRA_WINDOWS_WAIT = 0.3  # Seconds


class Environment:
    """Environment constants for CDP-Base"""
    QA = "qa"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"
    TEST = "test"


class ValidEnvs:
    """Valid environment names"""
    valid_envs = ["qa", "staging", "production", "local", "test"]


class Files:
    """File-related constants"""
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"


class PipInstall:
    # FINDLOCK - Checking to see if a package is installed
    # (Make sure a package isn't installed multiple times)
    FINDLOCK = Files.DOWNLOADS_FOLDER + "/pipfinding.lock"
    # LOCKFILE - Locking before performing any pip install
    # (Make sure that only one package installs at a time)
    LOCKFILE = Files.DOWNLOADS_FOLDER + "/pipinstall.lock"


class Timeouts:
    """Timeout constants for CDP-Base"""
    MINI_TIMEOUT = 2
    SMALL_TIMEOUT = 6
    LARGE_TIMEOUT = 10
    EXTREME_TIMEOUT = 30


class CDP:
    """CDP-specific constants"""
    DEFAULT_PORT = 9222
    RECONNECT_TIME = 0.1
    MAX_RETRIES = 3


class Browser:
    """Browser-related constants"""
    CHROME = "chrome"
    CHROMIUM = "chromium"
    EDGE = "edge"


class MultiBrowser:
    """Multi-browser constants"""
    DRIVER_FIXING_LOCK = "driver_fixing.lock"
    DOWNLOAD_FILE_LOCK = "download_file.lock"
    FILE_IO_LOCK = "file_io.lock"
    PYAUTOGUILOCK = "pyautogui.lock"


class Proxy:
    """Proxy-related constants"""
    DEFAULT_PROXY_PORT = 8899
    PROXY_ZIP_PATH = "proxy.zip"


class UserAgent:
    """User agent constants"""
    CHROME_LINUX = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    CHROME_MAC = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    CHROME_WINDOWS = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )


class PyAutoGUI:
    # The version installed if PyAutoGUI is not installed
    VER = "0.9.54"


class Mobile:
    """Mobile device constants"""
    IPHONE_X = {
        "width": 375,
        "height": 812,
        "pixelRatio": 3,
        "userAgent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 "
            "Mobile/15E148 Safari/604.1"
        )
    }
    IPAD = {
        "width": 768,
        "height": 1024,
        "pixelRatio": 2,
        "userAgent": (
            "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 "
            "Mobile/15E148 Safari/604.1"
        )
    }
    ANDROID = {
        "width": 360,
        "height": 640,
        "pixelRatio": 3,
        "userAgent": (
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Mobile Safari/537.36"
        )
    }


class JavaScript:
    """JavaScript code snippets"""
    SCROLL_TO_TOP = "window.scrollTo(0, 0);"
    SCROLL_TO_BOTTOM = "window.scrollTo(0, document.body.scrollHeight);"
    GET_PAGE_HEIGHT = "return document.body.scrollHeight;"
    GET_VIEWPORT_HEIGHT = "return window.innerHeight;"
    GET_VIEWPORT_WIDTH = "return window.innerWidth;"
    REMOVE_ELEMENT = "arguments[0].remove();"
    CLICK_ELEMENT = "arguments[0].click();"
    FOCUS_ELEMENT = "arguments[0].focus();"


class Selectors:
    """Common CSS selectors"""
    BUTTON = "button"
    INPUT = "input"
    TEXTAREA = "textarea"
    SELECT = "select"
    LINK = "a"
    IMAGE = "img"
    FORM = "form"
    TABLE = "table"
    DIV = "div"
    SPAN = "span"


class Events:
    """DOM event types"""
    CLICK = "click"
    CHANGE = "change"
    INPUT = "input"
    FOCUS = "focus"
    BLUR = "blur"
    SUBMIT = "submit"
    LOAD = "load"
    RESIZE = "resize"


class Keys:
    """Keyboard key constants"""
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
    CTRL = "\ue009"
    ALT = "\ue00a"
    SHIFT = "\ue008"


class Colors:
    """Color constants for styling"""
    RED = "#ff0000"
    GREEN = "#00ff00"
    BLUE = "#0000ff"
    YELLOW = "#ffff00"
    ORANGE = "#ffa500"
    PURPLE = "#800080"
    BLACK = "#000000"
    WHITE = "#ffffff"
    GRAY = "#808080"


# Simplified image constants (empty for CDP-Base)
class Images:
    """Image constants - simplified for CDP-Base"""
    DASH_PIE_PNG_1 = ""
    DASH_PIE_PNG_2 = ""
    DASH_PIE_PNG_3 = ""
    REPORT_FAVICON = ""
    SIDE_BY_SIDE_PNG = ""


# Backward compatibility aliases
MINI_TIMEOUT = Timeouts.MINI_TIMEOUT
SMALL_TIMEOUT = Timeouts.SMALL_TIMEOUT
LARGE_TIMEOUT = Timeouts.LARGE_TIMEOUT
EXTREME_TIMEOUT = Timeouts.EXTREME_TIMEOUT
