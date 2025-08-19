"""
SBCDP 页面信息方法模块
处理页面信息获取和JavaScript执行
"""

import os
import re
import asyncio
from contextlib import suppress

from .base import Base
from .. import settings
from ..fixtures import js_utils, constants


class PageInfo(Base):
    """页面信息方法类"""

    async def get_title(self):
        """获取页面标题"""
        return await self.cdp.page.evaluate("document.title")

    async def get_current_url(self):
        """获取当前URL"""
        return await self.cdp.page.evaluate("window.location.href")

    async def get_origin(self):
        """获取页面来源"""
        return await self.cdp.page.evaluate("window.location.origin")

    async def get_page_source(self):
        """获取页面源码"""
        try:
            source = await self.cdp.page.evaluate("document.documentElement.outerHTML")
        except Exception:
            await asyncio.sleep(constants.UC.CDP_MODE_OPEN_WAIT)
            source = await self.cdp.page.evaluate("document.documentElement.outerHTML")
        return source

    async def get_user_agent(self):
        """获取用户代理"""
        return await self.cdp.page.evaluate("navigator.userAgent")

    async def get_cookie_string(self):
        """获取Cookie字符串"""
        return await self.cdp.page.evaluate("document.cookie")

    async def get_all_cookies(self, *args, **kwargs):
        """获取Cookies"""
        return await self.cdp.driver.cookies.get_all(*args, **kwargs)

    async def get_locale_code(self):
        """获取语言代码"""
        return await self.cdp.page.evaluate("navigator.language || navigator.languages[0]")

    async def get_local_storage_item(self, key):
        """获取localStorage项"""
        js_code = """localStorage.getItem('%s');""" % key
        with suppress(Exception):
            return await self.cdp.page.evaluate(js_code)

    async def get_session_storage_item(self, key):
        """获取sessionStorage项"""
        js_code = """sessionStorage.getItem('%s');""" % key
        with suppress(Exception):
            return await self.cdp.page.evaluate(js_code)

    async def get_screen_rect(self):
        """获取屏幕矩形信息"""
        return await self.cdp.page.js_dumps("window.screen")

    async def get_element_rect(self, selector, timeout=None):
        """获取元素矩形信息"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.select(selector, timeout=timeout)
        await self._add_light_pause()
        coordinates = None
        if ":contains(" in selector:
            position = await element.get_position()
            x = position.x
            y = position.y
            width = position.width
            height = position.height
            coordinates = {"x": x, "y": y, "width": width, "height": height}
        else:
            coordinates = await self.cdp.page.js_dumps(
                """document.querySelector('%s').getBoundingClientRect()"""
                % js_utils.escape_quotes_if_needed(re.escape(selector))
            )
        return coordinates

    async def get_gui_element_rect(self, selector, timeout=None):
        """获取GUI元素矩形信息（相对于屏幕）"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element_rect = await self.get_element_rect(selector, timeout=timeout)
        window_rect = await self.get_window_rect()
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"] + window_rect["x"]
        e_y = element_rect["y"] + window_rect["y"]
        return {"x": e_x, "y": e_y, "width": e_width, "height": e_height}

    async def get_gui_element_center(self, selector, timeout=None):
        """获取GUI元素中心点坐标（相对于屏幕）"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element_rect = await self.get_gui_element_rect(selector, timeout=timeout)
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"]
        e_y = element_rect["y"]
        return (e_x + e_width / 2.0) + 0.5, (e_y + e_height / 2.0) + 0.5

    async def get_window_rect(self):
        """获取窗口矩形信息"""
        return await self.cdp.page.evaluate("""
            () => {
                return {
                    x: window.screenX,
                    y: window.screenY,
                    width: window.outerWidth,
                    height: window.outerHeight,
                    innerWidth: window.innerWidth,
                    innerHeight: window.innerHeight,
                    pageXOffset: window.pageXOffset,
                    pageYOffset: window.pageYOffset,
                    scrollX: window.scrollX,
                    scrollY: window.scrollY
                };
            }
        """)

    async def get_document(self):
        """获取文档对象"""
        return await self.cdp.page.get_document()

    async def get_flattened_document(self):
        """获取扁平化文档对象"""
        return await self.cdp.page.get_flattened_document()

    async def evaluate(self, expression):
        """执行JavaScript表达式并返回结果"""
        expression = expression.strip()
        exp_list = expression.split("\n")
        if exp_list and exp_list[-1].strip().startswith("return "):
            expression = (
                "\n".join(exp_list[0:-1]) + "\n"
                + exp_list[-1].strip()[len("return "):]
            ).strip()
        return await self.cdp.page.evaluate(expression)

    async def execute_script(self, script, *args):
        """执行JavaScript脚本"""
        return await self.evaluate(script)

    async def save_screenshot(self, name, folder=None, selector=None):
        """保存截图"""
        filename = name
        if folder:
            filename = os.path.join(folder, name)
        if not selector:
            return await self.cdp.page.save_screenshot(filename)
        else:
            return await (await self.cdp.select(selector)).save_screenshot(filename)

    async def print_to_pdf(self, name, folder=None):
        """打印为PDF"""
        filename = name
        if folder:
            filename = os.path.join(folder, name)
        await self.cdp.page.print_to_pdf(filename)

    async def scroll_into_view(self, selector):
        """滚动元素到可视区域"""
        await (await self.cdp.find_element(selector)).scroll_into_view()
        await self.cdp.page.wait()

    async def scroll_to_y(self, y):
        """滚动到指定Y坐标"""
        y = int(y)
        js_code = "window.scrollTo(0, %s);" % y
        with suppress(Exception):
            await self.cdp.page.evaluate(js_code)
            await self.cdp.page.wait()

    async def scroll_to_top(self):
        """滚动到页面顶部"""
        js_code = "window.scrollTo(0, 0);"
        with suppress(Exception):
            await self.cdp.page.evaluate(js_code)
            await self.cdp.page.wait()

    async def scroll_to_bottom(self):
        """滚动到页面底部"""
        js_code = "window.scrollTo(0, 10000);"
        with suppress(Exception):
            await self.cdp.page.evaluate(js_code)
            await self.cdp.page.wait()

    async def scroll_up(self, amount=25):
        """向上滚动"""
        await self.cdp.page.scroll_up(amount)
        await self.cdp.page.wait()

    async def scroll_down(self, amount=25):
        """向下滚动"""
        await self.cdp.page.scroll_down(amount)
        await self.cdp.page.wait()

    async def set_local_storage_item(self, key, value):
        """设置localStorage项"""
        js_code = """localStorage.setItem('%s', '%s');""" % (key, value)
        with suppress(Exception):
            await self.cdp.page.evaluate(js_code)

    async def set_session_storage_item(self, key, value):
        """设置sessionStorage项"""
        js_code = """sessionStorage.setItem('%s', '%s');""" % (key, value)
        with suppress(Exception):
            await self.cdp.page.evaluate(js_code)

    def extend_element(self, element):
        if not element:
            return
        element.save_screenshot = (lambda *args, **kwargs: self.cdp.ele_save_screenshot(element, *args, **kwargs))

    async def ele_save_screenshot(self, element, *args, **kwargs):
        return await element.save_screenshot_async(*args, **kwargs)
