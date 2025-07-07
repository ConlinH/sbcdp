"""
测试异步Chrome接口
"""

from contextlib import suppress

import pytest
from sbcdp import AsyncChrome as Chrome


class TestAsyncChrome:
    """异步Chrome测试类"""

    @pytest.mark.asyncio
    async def test_basic_navigation(self):
        # url = "https://fractal-testnet.unisat.io/explorer"
        url = "https://steamdb.info/"
        # url = "https://cn.airbusan.com/content/individual"
        # url = "https://pastebin.com/login"
        # url = "https://simple.ripley.com.pe/"
        # url = "https://www.e-food.gr/"
        async with Chrome() as chrome:
            await chrome.get(url)
            await chrome.sleep(5)
            with suppress(Exception):
                await chrome.mouse_click('input[type=checkbox]')
            assert 'cf_clearance' in {c.name: c.value for c in await chrome.get_all_cookies()}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
