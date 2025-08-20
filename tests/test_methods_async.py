"""
测试方法
"""

import pytest

from sbcdp import AsyncChrome


class TestMethodsAsync:
    """异步Chrome测试类"""

    @pytest.mark.asyncio
    async def test_shadow_root_query_selector(self):
        """测试shadow_dom"""
        async with AsyncChrome() as ac:
            await ac.open("https://seleniumbase.io/other/shadow_dom")
            await ac.click("button.tab_1")
            ele = await ac.find_element("fancy-tabs")
            node = await ele.sr_query_selector('#panels')
            assert await node.get_attribute('id') == 'panels'

    @pytest.mark.asyncio
    async def test_http_monitor(self):
        """测试请求监听和拦截"""
        from sbcdp import NetHttp

        flag = True

        async def cb(data: NetHttp):
            # print("response body: ", await data.get_response_body())
            if data.resource_type == 'Image' and not data.url.startswith('data:image'):
                nonlocal flag
                flag = False

        async def cb2(data: NetHttp):
            print("intercept: ", data)
            # 拦截所有的图片加载
            if data.resource_type == 'Image':
                return True

        async with AsyncChrome() as sb:
            sb.http_monitor(monitor_cb=cb, intercept_cb=cb2, delay_response_body=True)

            await sb.open("https://www.baidu.com")
            await sb.sleep(3)

        assert flag is True

    @pytest.mark.asyncio
    async def test_ws_monitor(self):
        """测试websocket监听"""
        from sbcdp import NetWebsocket

        ws_msg = ''

        async def ws_cb(msg: str, type_: str, ws: NetWebsocket):
            print(f"{type_}: {msg} ws: {ws}")
            nonlocal ws_msg
            ws_msg = msg

        async with AsyncChrome() as sb:
            sb.ws_monitor(ws_cb)
            url = "https://toolin.cn/ws"
            await sb.open(url)
            ele = await sb.find_element_by_text('连接Websocket')
            await ele.click()
            await sb.sleep(.5)
            await sb.send_keys("input[placeholder='输入消息']", 'test msg')
            await sb.sleep(1)
            ele = await sb.find_element_by_text('发 送')
            await ele.click()
            await sb.sleep(1)

        assert ws_msg == 'received：test msg'

    @pytest.mark.asyncio
    async def test_http_monitor_all_tabs(self):
        """测试所有标签页的请求监听和拦截"""
        from sbcdp import NetHttp

        flag = True

        async def cb(data: NetHttp):
            if data.resource_type == 'Image' and not data.url.startswith('data:image'):
                nonlocal flag
                flag = False

        async def cb2(data: NetHttp):
            print("intercept: ", data)
            # 拦截所有的图片加载
            if data.resource_type == 'Image':
                return True

        async with AsyncChrome() as sb:
            sb.http_monitor_all_tabs(monitor_cb=cb, intercept_cb=cb2, delay_response_body=True)

            await sb.open("https://www.baidu.com")
            await sb.sleep(3)

        assert flag is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
