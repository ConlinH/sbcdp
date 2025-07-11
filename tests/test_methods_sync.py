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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
