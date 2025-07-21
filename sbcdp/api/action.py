"""
SBCDP 动作方法模块
处理输入、表单操作等交互动作
"""

import re
import asyncio
from contextlib import suppress

from .base import Base
from .. import settings
from ..fixtures import js_utils


class Action(Base):
    """动作方法类"""

    async def send_keys(self, selector, text, timeout=None):
        """向元素发送按键"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element = await self.cdp.select(selector, timeout=timeout)
        await element.scroll_into_view()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        await element.send_keys(text)
        await self.cdp.page.sleep(0.025)

    async def press_keys(self, selector, text, timeout=None):
        """以人类速度按键"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element = await self.cdp.select(selector, timeout=timeout)
        await element.scroll_into_view()
        submit = False
        if text.endswith("\n") or text.endswith("\r"):
            submit = True
            text = text[:-1]
        for key in text:
            await element.send_keys(key)
            await asyncio.sleep(0.044)
        if submit:
            await element.send_keys("\r\n")
            await asyncio.sleep(0.044)
        await self.cdp.page.sleep(0.025)

    async def type(self, selector, text, timeout=None):
        """输入文本（先清空字段）"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.page.select(selector, timeout=timeout)
        element = self.cdp.add_element_methods(element)
        await element.scroll_into_view()
        with suppress(Exception):
            await element.clear_input()
        if text.endswith("\n") or text.endswith("\r"):
            text = text[:-1] + "\r\n"
        await element.send_keys(text)
        await self.cdp.page.sleep(0.025)

    async def set_value(self, selector, text, timeout=None):
        """设置元素值"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.page.select(selector, timeout=timeout)
        element = self.cdp.add_element_methods(element)
        await element.scroll_into_view()
        press_enter = False
        if text.endswith("\n"):
            text = text[:-1]
            press_enter = True
        value = js_utils.escape_quotes_if_needed(re.escape(text))
        css_selector = re.escape(selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        set_value_script = (
            """m_elm = document.querySelector('%s');"""
            """m_elm.value = '%s';""" % (css_selector, value)
        )
        await self.cdp.page.evaluate(set_value_script)
        if press_enter:
            await element.send_keys("\r\n")
        await self.cdp.page.sleep(0.025)

    async def clear(self, selector, timeout=None):
        """清空输入字段"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.page.select(selector, timeout=timeout)
        element = self.cdp.add_element_methods(element)
        await element.scroll_into_view()
        await element.clear_input()

    async def submit(self, selector="form"):
        """提交表单"""
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.page.select(selector)
        element = self.cdp.add_element_methods(element)
        await element.scroll_into_view()
        await element.send_keys("\r\n")
        await self.cdp.page.wait()

    async def get_text(self, selector):
        """获取元素文本"""
        # 使用page.find来查找元素
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.page.find(selector)
        element = self.cdp.add_element_methods(element)
        try:
            if hasattr(element, 'text_all'):
                return element.text_all or ""
            else:
                return element.text or ""
        except Exception:
            return ""

    async def get_attribute(self, selector, attribute):
        """获取元素属性值"""
        selector = js_utils.to_css_if_xpath(selector)
        element = await self.cdp.page.find(selector)
        element = self.cdp.add_element_methods(element)
        return await element.get_attribute(attribute)

    async def get_element_attribute(self, selector, attribute):
        """获取元素属性值（带异常处理）"""
        attributes = await self.get_element_attributes(selector)
        with suppress(Exception):
            return attributes[attribute]
        locate = ' %s="' % attribute
        value = await self.get_attribute(selector, attribute)
        if not value and locate not in attributes:
            raise KeyError(attribute)
        return value

    async def get_element_attributes(self, selector):
        """获取元素所有属性"""
        selector = js_utils.to_css_if_xpath(selector)
        return await self.cdp.page.js_dumps(
            """document.querySelector('%s')"""
            % js_utils.escape_quotes_if_needed(re.escape(selector))
        )

    async def get_element_html(self, selector):
        """获取元素HTML"""
        selector = js_utils.to_css_if_xpath(selector)
        # 确保元素存在
        await self.cdp.page.find(selector)
        await self._add_light_pause()
        return await self.cdp.page.evaluate(
            """document.querySelector('%s').outerHTML"""
            % js_utils.escape_quotes_if_needed(re.escape(selector))
        )

    async def set_attribute(self, selector, attribute, value):
        """设置元素属性"""
        selector = js_utils.to_css_if_xpath(selector)
        # 确保元素存在
        await self.cdp.page.find(selector)
        await self._add_light_pause()
        attribute = re.escape(attribute)
        attribute = js_utils.escape_quotes_if_needed(attribute)
        value = re.escape(value)
        value = js_utils.escape_quotes_if_needed(value)
        css_selector = re.escape(selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        set_attribute_script = (
            """document.querySelector('%s').setAttribute('%s','%s');"""
            % (css_selector, attribute, value)
        )
        await self.cdp.page.evaluate(set_attribute_script)

    async def set_attributes(self, selector, attribute, value):
        """为所有匹配元素设置属性"""
        selector = js_utils.to_css_if_xpath(selector)
        # 确保元素存在
        await self.cdp.page.find(selector)
        await self._add_light_pause()
        attribute = re.escape(attribute)
        attribute = js_utils.escape_quotes_if_needed(attribute)
        value = re.escape(value)
        value = js_utils.escape_quotes_if_needed(value)
        css_selector = re.escape(selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        set_attributes_script = (
            """var $elements = document.querySelectorAll('%s');
            var index = 0, length = $elements.length;
            for(; index < length; index++){
            $elements[index].setAttribute('%s','%s');}"""
            % (css_selector, attribute, value)
        )
        await self.cdp.page.evaluate(set_attributes_script)

    async def remove_attribute(self, selector, attribute):
        """移除元素属性"""
        selector = js_utils.to_css_if_xpath(selector)
        # 确保元素存在
        await self.cdp.page.find(selector)
        await self._add_light_pause()
        attribute = re.escape(attribute)
        attribute = js_utils.escape_quotes_if_needed(attribute)
        css_selector = re.escape(selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        remove_attribute_script = (
            """document.querySelector('%s').removeAttribute('%s');"""
            % (css_selector, attribute)
        )
        await self.cdp.page.evaluate(remove_attribute_script)

    async def remove_attributes(self, selector, attribute):
        """移除所有匹配元素的属性"""
        selector = js_utils.to_css_if_xpath(selector)
        # 确保元素存在
        await self.cdp.page.find(selector)
        await self._add_light_pause()
        attribute = re.escape(attribute)
        attribute = js_utils.escape_quotes_if_needed(attribute)
        css_selector = re.escape(selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        remove_attributes_script = (
            """var $elements = document.querySelectorAll('%s');
            var index = 0, length = $elements.length;
            for(; index < length; index++){
            $elements[index].removeAttribute('%s');}"""
            % (css_selector, attribute)
        )
        await self.cdp.page.evaluate(remove_attributes_script)

    async def remove_elements(self, selector):
        """移除所有匹配的元素"""
        css_selector = js_utils.to_css_if_xpath(selector)
        css_selector = re.escape(css_selector)
        css_selector = js_utils.escape_quotes_if_needed(css_selector)
        js_code = (
            """var $elements = document.querySelectorAll('%s');
            var index = 0, length = $elements.length;
            for(; index < length; index++){
            $elements[index].remove();}"""
            % css_selector
        )
        with suppress(Exception):
            await self.cdp.page.evaluate(js_code)

    async def set_locale(self, locale):
        """设置语言环境"""
        await self.cdp.page.set_locale(locale)

    async def internalize_links(self):
        """将所有target="_blank"链接改为target="_self" """
        await self.set_attributes('[target="_blank"]', "target", "_self")

    def extend_element(self, element):
        if not element:
            return

        element.send_keys = lambda text: self.cdp.ele_send_keys(element, text)
        element.scroll_into_view = lambda: self.cdp.ele_scroll_into_view(element)
        element.click = lambda: self.cdp.ele_click(element)
        element.flash = (lambda *args, **kwargs: self.cdp.ele_flash(element, *args, **kwargs))
        element.focus = lambda: self.cdp.ele_focus(element)
        element.mouse_click = lambda: self.cdp.ele_mouse_click(element)
        element.mouse_drag = lambda destination: self.cdp.ele_mouse_drag(element, destination)
        element.mouse_move = lambda: self.cdp.ele_mouse_move(element)
        element.press_keys = lambda text: self.cdp.ele_press_keys(element, text)
        element.set_text = lambda value: self.cdp.ele_set_text(element, value)
        element.set_value = lambda value: self.cdp.ele_set_value(element, value)
        element.send_file = lambda *file_paths: self.cdp.ele_send_file(element, *file_paths)
        element.clear_input = lambda: self.cdp.ele_clear_input(element)
        element.select_option = lambda: self.cdp.ele_select_option(element)

    async def ele_select_option(self, element):
        return await element.select_option_async()

    async def ele_scroll_into_view(self, element):
        await element.scroll_into_view_async()
        await self._add_light_pause()
        return None

    async def ele_send_keys(self, element, text):
        return await element.send_keys_async(text)

    async def ele_click(self, element):
        result = await element.click_async()
        await self.cdp.page.wait()
        return result

    async def ele_flash(self, element, *args, **kwargs):
        await element.scroll_into_view()
        if len(args) < 3 and "x_offset" not in kwargs:
            x_offset = await self.cdp._get_x_scroll_offset()
            kwargs["x_offset"] = x_offset
        if len(args) < 3 and "y_offset" not in kwargs:
            y_offset = await self.cdp._get_y_scroll_offset()
            kwargs["y_offset"] = y_offset
        return await element.flash_async(*args, **kwargs)

    async def ele_focus(self, element):
        return await element.focus_async()

    async def ele_mouse_click(self, element):
        result = await element.mouse_click_async()
        await self.cdp.page.wait()
        return result

    async def ele_mouse_drag(self, element, destination):
        return await element.mouse_drag_async(destination)

    async def ele_mouse_move(self, element):
        return await element.mouse_move_async()

    async def ele_press_keys(self, element, text):
        await element.scroll_into_view()
        submit = False
        if text.endswith("\n") or text.endswith("\r"):
            submit = True
            text = text[:-1]
        for key in text:
            await element.send_keys(key)
            await asyncio.sleep(0.044)
        if submit:
            await element.send_keys("\r\n")
            await asyncio.sleep(0.044)
        return await self.cdp.page.sleep(0.025)

    async def ele_set_text(self, element, value):
        return await element.set_text_async(value)

    async def ele_set_value(self, element, value):
        return await element.set_value_async(value)

    async def ele_send_file(self, element, *file_paths):
        return await element.send_file_async(*file_paths)

    async def ele_clear_input(self, element):
        return await element.clear_input_async()