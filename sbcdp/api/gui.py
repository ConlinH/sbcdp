"""
SBCDP GUI方法模块
处理GUI自动化操作（需要pyautogui）
"""

import sys
import asyncio
from typing import Optional

import fasteners

from .base import Base
from ..fixtures import constants


class GUI(Base):
    """GUI方法类"""

    def __install_pyautogui_if_missing(self):
        """安装PyAutoGUI（如果缺失）"""
        try:
            import pyautogui
        except ImportError:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])

    def __get_configured_pyautogui(self, pyautogui):
        """配置PyAutoGUI"""
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        return pyautogui

    def __make_sure_pyautogui_lock_is_writable(self):
        """确保PyAutoGUI锁文件可写"""
        import os
        lock_file = constants.MultiBrowser.PYAUTOGUILOCK
        if os.path.exists(lock_file):
            try:
                os.chmod(lock_file, 0o666)
            except Exception:
                pass

    async def gui_press_key(self, key):
        """GUI按键"""
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            pyautogui.press(key)
            await asyncio.sleep(0.044)
        await self.cdp.page.sleep(0.025)

    async def gui_press_keys(self, keys):
        """GUI按多个键"""
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            for key in keys:
                pyautogui.press(key)
                await asyncio.sleep(0.044)
        await self.cdp.page.sleep(0.025)

    async def gui_write(self, text):
        """GUI写入文本"""
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            pyautogui.write(text)
        await self.cdp.page.sleep(0.025)

    async def __gui_click_x_y(self, x, y, timeframe=0.25, uc_lock=False):
        """内部GUI点击坐标方法"""
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        screen_width, screen_height = pyautogui.size()
        if x < 0 or y < 0 or x > screen_width or y > screen_height:
            raise Exception(
                "PyAutoGUI cannot click on point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x, y, screen_width, screen_height)
            )
        if uc_lock:
            gui_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.PYAUTOGUILOCK
            )
            with gui_lock:
                self.__make_sure_pyautogui_lock_is_writable()
                pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
                if timeframe >= 0.25:
                    await asyncio.sleep(0.056)
                if "--debug" in sys.argv:
                    print(" <DEBUG> pyautogui.click(%s, %s)" % (x, y))
                pyautogui.click(x=x, y=y)
        else:
            pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
            if timeframe >= 0.25:
                await asyncio.sleep(0.056)
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.click(%s, %s)" % (x, y))
            pyautogui.click(x=x, y=y)

    async def gui_click_x_y(self, x, y, timeframe=0.25):
        """GUI点击坐标"""
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            await self.cdp.bring_active_window_to_front()
            await self.__gui_click_x_y(x, y, timeframe=timeframe, uc_lock=False)

    async def gui_click_element(self, selector, timeframe=0.25):
        """GUI点击元素"""
        x, y = await self.cdp.get_gui_element_center(selector)
        await self._add_light_pause()
        await self.gui_click_x_y(x, y, timeframe=timeframe)
        await self.cdp.page.wait()

    async def __gui_drag_drop(self, x1, y1, x2, y2, timeframe=0.25, uc_lock=False):
        """内部GUI拖拽方法"""
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        screen_width, screen_height = pyautogui.size()
        if x1 < 0 or y1 < 0 or x1 > screen_width or y1 > screen_height:
            raise Exception(
                "PyAutoGUI cannot drag-drop from point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x1, y1, screen_width, screen_height)
            )
        if x2 < 0 or y2 < 0 or x2 > screen_width or y2 > screen_height:
            raise Exception(
                "PyAutoGUI cannot drag-drop to point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x2, y2, screen_width, screen_height)
            )
        if uc_lock:
            gui_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.PYAUTOGUILOCK
            )
            with gui_lock:
                pyautogui.moveTo(x1, y1, 0.25, pyautogui.easeOutQuad)
                await self._add_light_pause()
                if "--debug" in sys.argv:
                    print(" <DEBUG> pyautogui.moveTo(%s, %s)" % (x1, y1))
                pyautogui.dragTo(x2, y2, button="left", duration=timeframe)
        else:
            pyautogui.moveTo(x1, y1, 0.25, pyautogui.easeOutQuad)
            await self._add_light_pause()
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.dragTo(%s, %s)" % (x2, y2))
            pyautogui.dragTo(x2, y2, button="left", duration=timeframe)

    async def gui_drag_drop_points(self, x1, y1, x2, y2, timeframe=0.35):
        """GUI拖拽坐标点"""
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            await self.cdp.bring_active_window_to_front()
            await self.__gui_drag_drop(
                x1, y1, x2, y2, timeframe=timeframe, uc_lock=False
            )
        await self.cdp.page.wait()

    async def gui_drag_and_drop(self, drag_selector, drop_selector, timeframe=0.35):
        """GUI拖拽元素"""
        await self.cdp.bring_active_window_to_front()
        x1, y1 = await self.cdp.get_gui_element_center(drag_selector)
        await self._add_light_pause()
        x2, y2 = await self.cdp.get_gui_element_center(drop_selector)
        await self._add_light_pause()
        await self.gui_drag_drop_points(x1, y1, x2, y2, timeframe=timeframe)

    async def gui_click_and_hold(self, selector, timeframe=0.35):
        """GUI点击并保持"""
        await self.cdp.bring_active_window_to_front()
        x, y = await self.cdp.get_gui_element_center(selector)
        await self._add_light_pause()
        await self.gui_drag_drop_points(x, y, x, y, timeframe=timeframe)

    async def __gui_hover_x_y(self, x, y, timeframe=0.25, uc_lock=False):
        """内部GUI悬停坐标方法"""
        self.__install_pyautogui_if_missing()
        import pyautogui
        pyautogui = self.__get_configured_pyautogui(pyautogui)
        screen_width, screen_height = pyautogui.size()
        if x < 0 or y < 0 or x > screen_width or y > screen_height:
            raise Exception(
                "PyAutoGUI cannot hover on point (%s, %s)"
                " outside screen. (Width: %s, Height: %s)"
                % (x, y, screen_width, screen_height)
            )
        if uc_lock:
            gui_lock = fasteners.InterProcessLock(
                constants.MultiBrowser.PYAUTOGUILOCK
            )
            with gui_lock:
                pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
                await asyncio.sleep(0.056)
                if "--debug" in sys.argv:
                    print(" <DEBUG> pyautogui.moveTo(%s, %s)" % (x, y))
        else:
            pyautogui.moveTo(x, y, timeframe, pyautogui.easeOutQuad)
            await asyncio.sleep(0.056)
            if "--debug" in sys.argv:
                print(" <DEBUG> pyautogui.moveTo(%s, %s)" % (x, y))

    async def gui_hover_x_y(self, x, y, timeframe=0.25):
        """GUI悬停坐标"""
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            await self.cdp.bring_active_window_to_front()
            await self.__gui_hover_x_y(x, y, timeframe=timeframe, uc_lock=False)

    async def gui_hover_element(self, selector, timeframe=0.25):
        """GUI悬停元素"""
        element_rect = await self.cdp.get_gui_element_rect(selector)
        width = element_rect["width"]
        height = element_rect["height"]
        if width > 0 and height > 0:
            x, y = await self.cdp.get_gui_element_center(selector)
            await self.cdp.bring_active_window_to_front()
            await self.__gui_hover_x_y(x, y, timeframe=timeframe)
        await self.cdp.page.wait()

    async def gui_hover_and_click(self, hover_selector, click_selector):
        """GUI悬停并点击"""
        gui_lock = fasteners.InterProcessLock(
            constants.MultiBrowser.PYAUTOGUILOCK
        )
        with gui_lock:
            self.__make_sure_pyautogui_lock_is_writable()
            await self.cdp.bring_active_window_to_front()
            await self.gui_hover_element(hover_selector)
            await asyncio.sleep(0.15)
            await self.gui_hover_element(click_selector)
            await self.cdp.click(click_selector)

    def extend_element(self, element):
        if not element:
            return
        element.gui_click = (lambda *args, **kwargs: self.cdp.ele_gui_click(element, *args, **kwargs))

    async def ele_gui_click(self, element, timeframe=None):
        element.scroll_into_view()
        await self._add_light_pause()
        position = element.get_position()
        x = position.x
        y = position.y
        e_width = position.width
        e_height = position.height
        # Relative to window
        element_rect = {"height": e_height, "width": e_width, "x": x, "y": y}
        window_rect = await self.cdp.get_window_rect()
        w_bottom_y = window_rect["y"] + window_rect["height"]
        viewport_height = window_rect["innerHeight"]
        x = window_rect["x"] + element_rect["x"]
        y = w_bottom_y - viewport_height + element_rect["y"]
        y_scroll_offset = window_rect["pageYOffset"]
        y = y - y_scroll_offset
        x = x + window_rect["scrollX"]
        y = y + window_rect["scrollY"]
        # Relative to screen
        element_rect = {"height": e_height, "width": e_width, "x": x, "y": y}
        e_width = element_rect["width"]
        e_height = element_rect["height"]
        e_x = element_rect["x"]
        e_y = element_rect["y"]
        x, y = ((e_x + e_width / 2.0) + 0.5), ((e_y + e_height / 2.0) + 0.5)
        if not timeframe or not isinstance(timeframe, (int, float)):
            timeframe = 0.25
        if timeframe > 3:
            timeframe = 3
        await self.gui_click_x_y(x, y, timeframe=timeframe)
        return await self.cdp.page.wait()
