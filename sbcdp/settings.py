"""
Settings - Simplified configuration for pure CDP automation.
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

# If True, an Exception is raised immediately for invalid proxy string syntax.
# If False, a Warning will appear after the test, with no proxy server used.
# (This applies when using --proxy=[PROXY_STRING] for using a proxy server.)
RAISE_INVALID_PROXY_STRING_EXCEPTION = True


# proxy_list.py
PROXY_LIST = {
    "example1": "98.8.195.160:443",  # (Example) - set your own proxy here
    "example2": "200.174.198.86:8888",  # (Example)
    "example3": "socks5://184.178.172.5:15303",  # (Example)
    "proxy1": None,
    "proxy2": None,
    "proxy3": None,
    "proxy4": None,
    "proxy5": None,
}

# ad_block_list.py
AD_BLOCK_LIST = [
    '[aria-label="Ads"]',
    '[src*="adservice."]',
    '[src*="adclick"]',
    '[src*="doubleclick"]',
    '[src*="snigelweb.com"]',
    '[src*="tagservices.com"]',
    '[src*="adsby"]',
    '[src*="adroll.com"]',
    '[src*="pagead"]',
    '[src*="3lift"]',
    '[src*="smartads."]',
    '[src*="ad_nexus"]',
    '[src*="/ads/"]',
    '[src*="moatads.com"]',
    '[src*="adsystem"]',
    '[src*="connectad"]',
    '[src*="/adservice."]',
    '[src*="syndication.com"]',
    '[src*="/ads."]',
    '[src*="lijit"]',
    '[src*="pagead"]',
    '[src*="adnxs.com"]',
    '[src*="onetag-sys.com"]',
    '[src*="indexww.com"]',
    '[src*="3lift.com"]',
    '[src*="rubiconproject.com"]',
    '[src*="brealtime.com"]',
    '[src*="33across.com"]',
    '[src*="adsrvr"]',
    '[type="data-doubleclick"]',
    "iframe[data-google-container-id]",
    'iframe[src*="doubleclick"]',
    'iframe[src*="/AdServer/"]',
    'iframe[src*="openx.net"]',
    'iframe[onload*="doWithAds"]',
    'iframe[id*="_ads_frame"]',
    'iframe[style="height:0px;width:0px;display:none;"]',
    '[aria-label="Ad"]',
    '[aria-label="Timeline: Trending now"]',
    '[aria-label="Timeline: Carousel"]',
    '[aria-roledescription="carousel"]',
    '[aria-label="Who to follow"]',
    '[class*="sponsored-content"]',
    '[class*="adsbygoogle"]',
    '[class^="adroll"]',
    '[data-ad-details*="Advertisement"]',
    '[data-native_ad*="placement"]',
    '[data-provider="dianomi"]',
    '[data-type="ad"]',
    '[data-track-event-label*="-taboola-"]',
    '[data-ad-feedback-beacon*="AD_"]',
    "[data-ad-feedback-beacon]",
    '[data-dcm-click-tracker*="/adclick."]',
    "[data-google-av-adk]",
    "[data-google-query-id]",
    '[data-ylk*="sponsored_cluster"]',
    "[data-google-av-cxn]",
    "[data-ad-client]",
    "[data-ad-slot]",
    '[href*="doubleclick"]',
    '[href*="amazon-adsystem"]',
    '[alt="Advertisement"]',
    '[alt$=" Ad"]',
    '[id*="-ad-"]',
    '[id*="_ads_"]',
    '[id*="AdFrame"]',
    '[id*="carbonads"]',
    '[id^="ad-"]',
    '[id^="my-ads"]',
    '[id^="outbrain_widget"]',
    '[id^="taboola-"]',
    '[id^="google_ads_frame"]',
    '[id^="google_ads_iframe"]',
    '[id="tryitLeaderboard"]',
    '[id="dianomiRightRail"]',
    '[allow*="advertising.com"]',
    "ins.adsby",
    "li.strm-ad-clusters",
    "li.js-stream-ad",
    "div.after_ad",
    "div.ad-container",
    "div.ad_module",
    "div.ad-subnav-container",
    "div.ad-wrapper",
    "div.adroll-block",
    "div.data-ad-container",
    "div.GoogleActiveViewElement",
    "div.l-ad",
    "div.right-ad",
    "div.wx-adWrapper",
    'div.image > a > img[src*="HomepageAd"]',
    'img[src*="HomepageAd"]',
    "img.img_ad",
    'link[href*="/adservice."]',
    "section.dianomi-ad",
    "ytd-promoted-video-renderer",
    "ytd-video-masthead-ad-v3-renderer",
]
