"""
测试Chrome参数
"""

import pytest
import asyncio
from sbcdp import Chrome


test_html = "<html><head><title>Test Page</title></head><body><h1>Hello World</h1></body></html>"


class TestArgs:
    """异步Chrome测试类"""

    @pytest.mark.asyncio
    async def test_args_ua(self):
        """测试user-agent"""
        ua1 = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
              "Safari/537.36")
        ua2 = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 "
              "Safari/537.36")
        async with Chrome(user_agent=ua1) as chrome:
            await chrome.open(f"data:text/html,{test_html}")
            user_agent = await chrome.get_user_agent()
            assert ua1 == user_agent

            await chrome.open(f"data:text/html,{test_html}", user_agent=ua2)
            user_agent = await chrome.get_user_agent()
            assert ua2 == user_agent

    # @pytest.mark.asyncio
    # async def test_args_proxy(self):
    #     """测试代理"""
    #     proxy = 'socks5://127.0.0.1:18080'
    #     # proxy = 'https://127.0.0.1:18080'
    #     async with Chrome() as chrome:
    #         await chrome.open("https://httpbin.org/ip")
    #         origin = await chrome.get_text("pre")
    #
    #     async with Chrome(proxy=proxy) as chrome:
    #         await chrome.open("https://httpbin.org/ip")
    #         new = await chrome.get_text("pre")
    #
    #     assert origin != new

    @pytest.mark.asyncio
    async def test_args_user_data_dir(self):
        """测试user-data"""
        import os
        import shutil

        user_data_dir = 'test_user_data'
        shutil.rmtree(user_data_dir, ignore_errors=True)
        async with Chrome(user_data_dir='test_user_data') as chrome:
            await chrome.open(f"data:text/html,{test_html}")

        try:
            assert os.path.exists(user_data_dir)
        finally:
            await asyncio.sleep(1)
            shutil.rmtree(user_data_dir)

    @pytest.mark.asyncio
    async def test_args_guest(self):
        """测试浏览器的访客模式"""
        async with Chrome(guest=True) as chrome:
            await chrome.open(f"data:text/html,{test_html}")

    @pytest.mark.asyncio
    async def test_args_locale(self):
        """测试浏览器的语言"""
        async with Chrome(locale='en-US') as chrome:
            await chrome.open(f"data:text/html,{test_html}")
            assert await chrome.get_locale_code() == 'en-US'

            await chrome.open(f"data:text/html,{test_html}", locale='zh-CN')
            assert await chrome.get_locale_code() == 'zh-CN'

    @pytest.mark.asyncio
    async def test_args_timezone(self):
        """测试浏览器的时区"""
        async with Chrome(timezone="America/New_York") as chrome:
            await chrome.open(f"data:text/html,{test_html}")
            assert await chrome.evaluate('Intl.DateTimeFormat().resolvedOptions().timeZone'), "America/New_York"

            await chrome.open(f"data:text/html,{test_html}", timezone="Asia/Shanghai")
            assert await chrome.evaluate('Intl.DateTimeFormat().resolvedOptions().timeZone'), "Asia/Shanghai"

    @pytest.mark.asyncio
    async def test_args_platform(self):
        """测试浏览器的platform"""
        async with Chrome(platform="Win32") as chrome:
            await chrome.open(f"data:text/html,{test_html}")
            assert await chrome.evaluate('navigator.platform'), "Win32"

            await chrome.open(f"data:text/html,{test_html}", platform="Win64")
            assert await chrome.evaluate('navigator.platform'), "Win64"

    @pytest.mark.asyncio
    async def test_args_chrome_type(self):
        """测试浏览器的类型"""
        async with Chrome() as chrome:
            ua = await chrome.evaluate('navigator.userAgent')
            assert 'Edg/' not in ua and 'Chrome/' in ua

        async with Chrome(chrome_type="edge") as chrome:
            ua = await chrome.evaluate('navigator.userAgent')
            assert 'Edg/' in ua


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
