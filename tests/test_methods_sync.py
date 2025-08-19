"""
测试方法
"""

import pytest
from sbcdp import SyncChrome


class TestMethodsAsync:
    """异步Chrome测试类"""

    def test_shadow_root_query_selector(self):
        """测试shadow_dom"""

        with SyncChrome() as c:
            c.open("https://seleniumbase.io/other/shadow_dom")
            c.click("button.tab_1")
            ele = c.find_element("fancy-tabs")
            node = ele.sr_query_selector('#panels')
            assert node.get_attribute('id') == 'panels'

    def test_http_monitor(self):
        """测试请求监听和拦截"""
        from sbcdp import NetHttp

        flag = True

        def cb(data: NetHttp):
            if data.resource_type == 'Image' and not data.url.startswith('data:image'):
                nonlocal flag
                flag = False

        def cb2(data: NetHttp):
            print("intercept: ", data)
            # 拦截所有的图片加载
            if data.resource_type == 'Image':
                return True

        with SyncChrome() as sb:
            sb.http_monitor(monitor_cb=cb, intercept_cb=cb2, delay_response_body=True)

            sb.open("https://www.baidu.com")
            sb.sleep(3)

        assert flag is True

    def test_ws_monitor(self):
        """测试websocket监听"""
        from sbcdp import NetWebsocket

        ws_msg = ''

        async def ws_cb(msg: str, type_: str, ws: NetWebsocket):
            print(f"{type_}: {msg} ws: {ws}")
            nonlocal ws_msg
            ws_msg = msg

        with SyncChrome() as sb:
            sb.ws_monitor(ws_cb)
            url = "https://toolin.cn/ws"
            sb.open(url)
            ele = sb.find_element_by_text('连接Websocket')
            ele.click()
            sb.sleep(.5)
            sb.send_keys("input[placeholder='输入消息']", 'test msg')
            sb.sleep(1)
            ele = sb.find_element_by_text('发 送')
            ele.click()
            sb.sleep(1)

        assert ws_msg == 'received：test msg'

    def test_http_monitor_all_tabs(self):
        """测试请求监听和拦截"""
        from sbcdp import NetHttp

        flag = True

        def cb(data: NetHttp):
            if data.resource_type == 'Image' and not data.url.startswith('data:image'):
                nonlocal flag
                flag = False

        def cb2(data: NetHttp):
            print("intercept: ", data)
            # 拦截所有的图片加载
            if data.resource_type == 'Image':
                return True

        with SyncChrome() as sb:
            sb.http_monitor_all_tabs(monitor_cb=cb, intercept_cb=cb2, delay_response_body=True)

            sb.open("https://www.baidu.com")
            sb.sleep(3)

        assert flag is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
