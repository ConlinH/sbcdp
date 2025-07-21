"""
测试方法
"""

import pytest
from gevent.threading import local

from sbcdp import AsyncChrome


class TestMethodsAsync:
    """异步Chrome测试类"""

    # @pytest.mark.asyncio
    # async def test_shadow_root_query_selector(self):
    #     """测试shadow_dom"""
    #     async with AsyncChrome() as ac:
    #         await ac.open("https://seleniumbase.io/other/shadow_dom")
    #         await ac.click("button.tab_1")
    #         ele = await ac.find_element("fancy-tabs")
    #         node = await ele.sr_query_selector('#panels')
    #         assert await node.get_attribute('id') == 'panels'

    @pytest.mark.asyncio
    async def test_request_monitor(self):
        """测试请求监听和拦截"""
        from sbcdp import NetData

        flag = True

        async def cb(data: NetData):
            if data.resource_type == 'Image' and not data.url.startswith('data:image'):
                nonlocal flag
                flag = False

        async def cb2(data: NetData):
            print("intercept: ", data)
            # 拦截所有的图片加载
            if data.resource_type == 'Image':
                return True

        async with AsyncChrome() as sb:
            await sb.request_monitor(monitor_cb=cb, intercept_cb=cb2, delay_response_body=True)

            await sb.open("https://www.baidu.com")
            await sb.sleep(3)

        assert flag is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
