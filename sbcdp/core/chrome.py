"""
SBCDP 同步Chrome类
提供同步的Chrome自动化接口
"""

import asyncio
from ..driver import cdp_util
from .methods import SyncCDPMethods, AsyncCDPMethods


class SyncChrome(SyncCDPMethods):
    """同步Chrome类 - 纯同步的CDP自动化接口"""

    def __init__(self, url=None, **kwargs):
        """初始化Chrome实例

        Args:
            url: 初始URL，默认为about:blank
            **kwargs: 传递给cdp_util.start_sync的参数
        """
        if not url:
            url = "about:blank"

        # 创建事件循环
        self.loop = asyncio.new_event_loop()

        # 启动CDP驱动
        self.driver = cdp_util.start_sync(**kwargs)

        # 获取页面
        self.page = self.loop.run_until_complete(self.driver.get(url))

        # 初始化父类
        super().__init__(self.loop, self.page, self.driver)

    def stop(self):
        """停止Chrome实例"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.stop()

    def close(self):
        """关闭Chrome实例"""
        self.stop()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()

    def __del__(self):
        """析构函数"""
        try:
            self.stop()
        except Exception:
            pass


class AsyncChrome(AsyncCDPMethods):
    """异步Chrome类 - 纯异步的CDP自动化接口"""

    def __init__(self, url=None, **kwargs):
        """初始化异步Chrome实例"""
        self.driver = None
        self.page = None
        self._initialized = False
        self._url = url
        self._kwargs = kwargs

    async def start(self):
        """异步启动Chrome实例
        Returns:
            self: 返回自身以支持链式调用
        """
        if not self._url:
            self._url = "about:blank"

        # 启动CDP驱动
        self.driver = await cdp_util.start(**self._kwargs)

        # 获取页面
        self.page = await self.driver.get(self._url)

        # 初始化父类
        super().__init__(self.page, self.driver)
        self._initialized = True

        return self

    async def stop(self):
        """异步停止Chrome实例"""
        if self._initialized and self.driver:
            if hasattr(self.driver, 'stop'):
                if asyncio.iscoroutinefunction(self.driver.stop):
                    await self.driver.stop()
                else:
                    self.driver.stop()
            self._initialized = False

    async def close(self):
        """异步关闭浏览器"""
        await self.stop()

    async def __aenter__(self):
        """异步上下文管理器入口"""
        if not self._initialized:
            await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.stop()

    def __del__(self):
        """析构函数"""
        # 注意：在析构函数中不能使用await，所以这里只是标记
        if hasattr(self, '_initialized') and self._initialized:
            try:
                # 尝试同步关闭（如果可能）
                if hasattr(self, 'driver') and self.driver:
                    if hasattr(self.driver, 'stop') and not asyncio.iscoroutinefunction(self.driver.stop):
                        self.driver.stop()
            except Exception:
                pass
