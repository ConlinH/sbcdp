"""
SBCDP - Pure CDP (Chrome DevTools Protocol) Automation Framework
Web Crawling / Scraping / Automation

清晰分离的同步和异步接口：
- sbcdp.api_sync: 纯同步接口
- sbcdp.api_async: 纯异步接口
"""

from contextlib import suppress
from .__version__ import __version__

# 新的清晰接口
from .core.chrome import SyncChrome, AsyncChrome

from .fixtures import shared_utils
from .driver import cdp_util  # noqa

with suppress(Exception):
    import colorama

with suppress(Exception):
    shared_utils.fix_colorama_if_windows()
    colorama.init(autoreset=True)


version_list = [int(i) for i in __version__.split(".") if i.isdigit()]
version_tuple = tuple(version_list)
version_info = version_tuple 

# 导出的公共接口
__all__ = [
    'SyncChrome',    # 推荐：纯同步接口
    'AsyncChrome',   # 推荐：纯异步接口
    'cdp_util',      # 底层驱动
    '__version__',
    'version_info',
]
