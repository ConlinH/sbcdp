"""
SBCDP 导航方法模块
处理页面导航相关的操作
"""

import asyncio

from .base import Base
from ..fixtures import shared_utils, constants


class Navigation(Base):
    """导航方法类"""

    def __init__(self, cdp):
        super().__init__(cdp)

    async def get(self, url, new_tab=False, new_window=False, **kwargs):
        """导航到指定URL"""
        url = shared_utils.fix_url_as_needed(url)
        await self.cdp.page.get(url, new_tab=new_tab, new_window=new_window, **kwargs)
        url_protocol = url.split(":")[0]
        safe_url = True
        if url_protocol not in ["about", "data", "chrome"]:
            safe_url = False
        if not safe_url:
            await asyncio.sleep(constants.UC.CDP_MODE_OPEN_WAIT)
            if shared_utils.is_windows():
                await asyncio.sleep(constants.UC.EXTRA_WINDOWS_WAIT)
        else:
            await asyncio.sleep(0.012)
        await self.cdp.page.wait()

    async def open(self, url, new_tab=False, new_window=False, **kwargs):
        """打开指定URL（get方法的别名）"""
        await self.get(url, new_tab=new_tab, new_window=new_window, **kwargs)

    async def reload(self, ignore_cache=True, script_to_evaluate_on_load=None):
        """重新加载页面"""
        await self.cdp.page.reload(
            ignore_cache=ignore_cache,
            script_to_evaluate_on_load=script_to_evaluate_on_load,
        )

    async def go_back(self):
        """后退"""
        await self.cdp.page.back()

    async def go_forward(self):
        """前进"""
        await self.cdp.page.forward()

    async def get_navigation_history(self):
        """获取导航历史"""
        return await self.cdp.page.get_navigation_history()

    async def open_new_tab(self, url=None, switch_to=True):
        """打开新标签页"""
        if not isinstance(url, str):
            url = "about:blank"
        await self.cdp.page.get(url, new_tab=True)
        if switch_to:
            await self.switch_to_newest_tab()

    async def open_new_window(self, url=None, switch_to=True):
        """打开新窗口（新标签页的别名）"""
        return await self.open_new_tab(url=url, switch_to=switch_to)

    async def switch_to_tab(self, tab):
        """切换到指定标签页"""
        from ..driver import cdp_util  # 延迟导入避免循环依赖
        if isinstance(tab, int):
            self.cdp.page = self.cdp.driver.tabs[tab]
        elif isinstance(tab, cdp_util.Tab):
            self.cdp.page = tab
        else:
            raise Exception("`tab` must be an int or a Tab type!")
        await self.bring_active_window_to_front()

    async def switch_to_newest_tab(self):
        """切换到最新的标签页"""
        await self.switch_to_tab(-1)

    async def switch_to_window(self, window):
        """切换到指定窗口（标签页的别名）"""
        await self.switch_to_tab(window)

    async def switch_to_newest_window(self):
        """切换到最新的窗口"""
        await self.switch_to_tab(-1)

    async def close_active_tab(self):
        """关闭当前活动的标签页"""
        return await self.cdp.page.close()

    async def get_active_tab(self):
        """获取当前活动的标签页"""
        return self.cdp.page

    async def get_tabs(self):
        """获取所有标签页"""
        return self.cdp.driver.tabs

    async def get_window(self):
        """获取窗口信息"""
        return await self.cdp.page.get_window()

    async def bring_active_window_to_front(self):
        """将活动窗口置于前台"""
        await self.cdp.page.bring_to_front()
        await self._add_light_pause()

    async def tile_windows(self, windows=None, max_columns=0):
        """平铺窗口并返回平铺窗口的网格"""
        return await self.cdp.driver.tile_windows(windows, max_columns)

    async def grant_permissions(self, permissions, origin=None):
        """为当前窗口授予特定权限"""
        return await self.cdp.driver.grant_permissions(permissions, origin)

    async def grant_all_permissions(self):
        """为当前窗口授予所有权限"""
        return await self.cdp.driver.grant_all_permissions()

