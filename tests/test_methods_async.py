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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
