"""
SBCDP - Pure CDP (Chrome DevTools Protocol) Automation Framework
Web Crawling / Scraping / Automation
"""

from contextlib import suppress

from .__version__ import __version__
from .fixtures import shared_utils
from .driver import cdp_util
from .core.chrome import AsyncChrome
from .core.chrome import AsyncChrome as Chrome
from .core.chrome import SyncChrome

with suppress(Exception):
    import colorama

with suppress(Exception):
    shared_utils.fix_colorama_if_windows()
    colorama.init(autoreset=True)

version = __version__


__all__ = [
    'AsyncChrome',
    'Chrome',
    'SyncChrome',
    'cdp_util',
    '__version__',
    'version',
]
