"""
CDP-Base Settings - Simplified configuration for pure CDP automation.
"""

# #####>>>>>----- CORE TIMEOUT SETTINGS -----<<<<<#####

# Default maximum time (in seconds) to wait for page elements to appear.
MINI_TIMEOUT = 2
SMALL_TIMEOUT = 7
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30

# Default page load timeout.
PAGE_LOAD_TIMEOUT = 120

# Default page load strategy.
# ["normal", "eager", "none"]
PAGE_LOAD_STRATEGY = "normal"

# #####>>>>>----- BROWSER SETTINGS -----<<<<<#####

# Default browser type
DEFAULT_BROWSER = "chrome"

# Default window size and position
CHROME_START_WIDTH = 1366
CHROME_START_HEIGHT = 768
WINDOW_START_X = 0
WINDOW_START_Y = 0

# Headless mode window size
HEADLESS_START_WIDTH = 1366
HEADLESS_START_HEIGHT = 768

# Default user agent
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# #####>>>>>----- FILE SETTINGS -----<<<<<#####

# Archive settings
ARCHIVE_EXISTING_LOGS = False
ARCHIVE_EXISTING_DOWNLOADS = False
SCREENSHOT_WITH_BACKGROUND = False

# Default screenshot name
SCREENSHOT_NAME = "screenshot.png"

# #####>>>>>----- CDP SETTINGS -----<<<<<#####

# Default CDP port
CDP_PORT = 9222

# CDP connection timeout
CDP_TIMEOUT = 30

# CDP reconnection delay
CDP_RECONNECT_DELAY = 0.1

# #####>>>>>----- AUTOMATION SETTINGS -----<<<<<#####

# Switch to new tabs automatically
SWITCH_TO_NEW_TABS_ON_CLICK = True

# Wait for page ready state
WAIT_FOR_RSC_ON_PAGE_LOADS = True
WAIT_FOR_RSC_ON_CLICKS = False

# Skip JavaScript waits
SKIP_JS_WAITS = False

# #####>>>>>----- SECURITY SETTINGS -----<<<<<#####

# Disable Content Security Policy
DISABLE_CSP_ON_CHROME = False

# Ignore certificate errors
IGNORE_CERTIFICATE_ERRORS = True
