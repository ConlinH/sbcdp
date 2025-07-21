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

    def test_request_monitor(self):
        """测试请求监听和拦截"""
        from sbcdp import NetData

        flag = True

        def cb(data: NetData):
            if data.resource_type == 'Image' and not data.url.startswith('data:image'):
                nonlocal flag
                flag = False

        def cb2(data: NetData):
            print("intercept: ", data)
            # 拦截所有的图片加载
            if data.resource_type == 'Image':
                return True

        with SyncChrome() as sb:
            sb.request_monitor(monitor_cb=cb, intercept_cb=cb2, delay_response_body=True)

            sb.open("https://www.baidu.com")
            sb.sleep(3)

        assert flag is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
