"""
测试Cloudflare
"""

from contextlib import suppress

import pytest
from sbcdp import AsyncChrome as Chrome


class TestCloudflare:
    """测试5s盾"""

    @pytest.mark.asyncio
    async def test_cloudflare(self):
        # url = "https://fractal-testnet.unisat.io/explorer"
        url = "https://steamdb.info/"
        # url = "https://cn.airbusan.com/content/individual"
        # url = "https://pastebin.com/login"
        # url = "https://simple.ripley.com.pe/"
        # url = "https://www.e-food.gr/"
        async with Chrome() as chrome:
            await chrome.get(url)
            with suppress(Exception):
                await chrome.verify_cf("确认您是真人")
            await chrome.sleep(4)
            assert 'cf_clearance' in {c.name: c.value for c in await chrome.get_all_cookies()}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
