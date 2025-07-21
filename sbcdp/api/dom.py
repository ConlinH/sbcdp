"""
SBCDP 元素方法模块
处理元素查找和操作相关的功能
"""

import time
from contextlib import suppress

from .base import Base
from .. import settings
from ..fixtures import page_utils, js_utils


class Dom(Base):
    """元素方法类"""

    async def find_element(self, selector, best_match=False, timeout=None):
        """查找单个元素，支持文本内容搜索"""
        if not selector:
            raise ValueError("Selector cannot be empty")

        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        await self._add_light_pause()
        selector = js_utils.to_css_if_xpath(selector)
        early_failure = False
        if ":contains(" in selector:
            selector, _ = page_utils.recalculate_selector(
                selector, by="css selector", xp_ok=True
            )
        failure = False
        try:
            if early_failure:
                raise Exception("Failed!")
            element = await self.cdp.page.find(selector, best_match=best_match, timeout=timeout)
        except Exception:
            failure = True
            plural = "s"
            if timeout == 1:
                plural = ""
            message = "\n Element {%s} was not found after %s second%s!" % (
                selector,
                timeout,
                plural,
            )
        if failure:
            raise Exception(message)
        element = self.cdp.add_element_methods(element)
        return element

    async def find_element_by_text(self, text, tag_name=None, timeout=None):
        """通过文本内容查找元素"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        await self._add_light_pause()
        time_now = time.time()
        await self.cdp.assert_text(text, timeout=timeout)
        spent = int(time.time() - time_now)
        remaining = 1 + timeout - spent
        if tag_name:
            await self.cdp.assert_element(tag_name, timeout=remaining)
        elements = await self.cdp.page.find_elements_by_text(text=text)
        if tag_name:
            tag_name = tag_name.lower().strip()
        for element in elements:
            if element and not tag_name:
                element = self.cdp.add_element_methods(element)
                return element
            elif element and tag_name and element.tag_name.lower() == tag_name:
                element = self.cdp.add_element_methods(element)
                return element
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Text {%s} with tag {%s} was not found after %s second%s!"
            % (text, tag_name, timeout, plural)
        )

    async def find_elements_by_text(self, text, tag_name=None, timeout=None):
        """通过文本内容查找多个元素"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        await self._add_light_pause()
        elements = await self.cdp.page.find_elements_by_text(text=text)
        updated_elements = []
        if tag_name:
            tag_name = tag_name.lower().strip()
        for element in elements:
            if element and not tag_name:
                element = self.cdp.add_element_methods(element)
                updated_elements.append(element)
            elif element and tag_name and element.tag_name.lower() == tag_name:
                element = self.cdp.add_element_methods(element)
                updated_elements.append(element)
        return updated_elements

    async def find_all(self, selector, timeout=None):
        """查找所有匹配的元素"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        await self._add_light_pause()
        selector = js_utils.to_css_if_xpath(selector)
        elements = await self.cdp.page.find_all(selector, timeout=timeout)
        updated_elements = []
        for element in elements:
            element = self.cdp.add_element_methods(element)
            updated_elements.append(element)
        return updated_elements

    async def select(self, selector, timeout=None):
        """选择单个元素（类似find_element）"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        await self._add_light_pause()
        selector = js_utils.to_css_if_xpath(selector)
        if ":contains(" in selector:
            tag_name = selector.split(":contains(")[0].split(" ")[-1]
            text = selector.split(":contains(")[1].split(")")[0][1:-1]
            with suppress(Exception):
                new_timeout = timeout
                if new_timeout < 1:
                    new_timeout = 1
                await self.cdp.page.select(tag_name, timeout=new_timeout)
                await self.cdp.page.find(text, timeout=new_timeout)
            elements = await self.find_elements_by_text(text, tag_name=tag_name)
            if not elements:
                plural = "s"
                if timeout == 1:
                    plural = ""
                msg = "\n Element {%s} was not found after %s second%s!"
                message = msg % (selector, timeout, plural)
                raise Exception(message)
            element = self.cdp.add_element_methods(elements[0])
            return element
        failure = False
        try:
            element = await self.cdp.page.select(selector, timeout=timeout)
        except Exception:
            failure = True
            plural = "s"
            if timeout == 1:
                plural = ""
            msg = "\n Element {%s} was not found after %s second%s!"
            message = msg % (selector, timeout, plural)
        if failure:
            raise Exception(message)
        element = self.cdp.add_element_methods(element)
        return element

    async def select_all(self, selector, timeout=None):
        """选择所有匹配的元素"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        await self._add_light_pause()
        selector = js_utils.to_css_if_xpath(selector)
        elements = await self.cdp.page.select_all(selector, timeout=timeout)
        updated_elements = []
        for element in elements:
            element = self.cdp.add_element_methods(element)
            updated_elements.append(element)
        return updated_elements

    async def find_elements(self, selector, timeout=None):
        """查找多个元素（select_all的别名）"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        return await self.select_all(selector, timeout=timeout)

    async def find_visible_elements(self, selector, timeout=None):
        """查找所有可见的元素"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        visible_elements = []
        elements = await self.select_all(selector, timeout=timeout)
        for element in elements:
            with suppress(Exception):
                position = element.get_position()
                if position.width != 0 or position.height != 0:
                    visible_elements.append(element)
        return visible_elements

    async def click(self, selector, timeout=None):
        """点击元素"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element = await self.find_element(selector, timeout=timeout)
        await element.scroll_into_view()
        await element.click()
        await self.cdp.page.wait()

    async def click_nth_element(self, selector, number):
        """点击第N个匹配的元素"""
        elements = await self.select_all(selector)
        if len(elements) < number:
            raise Exception(
                "Not enough matching {%s} elements to "
                "click number %s!" % (selector, number)
            )
        number = number - 1
        if number < 0:
            number = 0
        element = elements[number]
        element.scroll_into_view()
        element.click()

    async def click_nth_visible_element(self, selector, number):
        """点击第N个可见的元素"""
        elements = await self.find_visible_elements(selector)
        if len(elements) < number:
            raise Exception(
                "Not enough matching {%s} elements to "
                "click number %s!" % (selector, number)
            )
        number = number - 1
        if number < 0:
            number = 0
        element = elements[number]
        element.scroll_into_view()
        element.click()

    async def click_link(self, link_text):
        """点击链接文本"""
        (await self.find_elements_by_text(link_text, "a"))[0].click()

    async def mouse_click(self, selector, timeout=None):
        """模拟鼠标点击"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        element = await self.find_element(selector, timeout=timeout)
        await element.scroll_into_view()
        await element.mouse_click()
        await self.cdp.page.wait()

    async def nested_click(self, parent_selector, selector):
        """在父元素内点击子元素"""
        element = await self.find_element(parent_selector)
        await (await element.query_selector(selector)).mouse_click()
        await self.cdp.page.wait()

    async def get_nested_element(self, parent_selector, selector):
        """获取父元素内的子元素"""
        element = await self.find_element(parent_selector)
        return await element.query_selector(selector)

    async def get_active_element(self):
        """获取当前活动的元素"""
        return await self.cdp.page.js_dumps("document.activeElement")

    async def get_active_element_css(self):
        """获取当前活动元素的CSS选择器"""
        from ..js_code import active_css_js

        js_code = active_css_js.get_active_element_css
        js_code = js_code.replace("return getBestSelector", "getBestSelector")
        return await self.cdp.page.evaluate(js_code)

    def extend_element(self, element):
        if not element:
            return

        element.query_selector = lambda selector: self.cdp.ele_query_selector(element, selector)
        element.querySelector = element.query_selector
        element.query_selector_all = lambda selector: self.cdp.ele_query_selector_all(element, selector)
        element.querySelectorAll = element.query_selector_all

        # shadow root
        element.sr_query_selector = (lambda selector: self.cdp.ele_shadow_root_query_selector(element, selector))
        element.shadow_root_query_selector = element.sr_query_selector
        element.sr_query_selector_all = (lambda selector: self.cdp.ele_shadow_root_query_selector_all(element, selector))
        element.shadow_root_query_selector_all = element.sr_query_selector_all

        element.highlight_overlay = lambda: self.cdp.ele_highlight_overlay(element)
        element.type = lambda text: self.cdp.ele_type(element, text)
        element.remove_from_dom = lambda: self.cdp.ele_remove_from_dom(element)
        element.save_to_dom = lambda: self.cdp.ele_save_to_dom(element)
        element.get_position = lambda: self.cdp.ele_get_position(element)
        element.get_html = lambda: self.cdp.ele_get_html(element)
        element.get_js_attributes = lambda: self.cdp.ele_get_js_attributes(element)
        element.get_attribute = lambda attribute: self.cdp.ele_get_attribute(element, attribute)
        element.get_parent = lambda: self.cdp.ele_get_parent(element)

    async def ele_remove_from_dom(self, element):
        return await element.remove_from_dom_async()

    async def ele_save_to_dom(self, element):
        return await element.save_to_dom_async()

    async def ele_type(self, element, text):
        with suppress(Exception):
            await element.clear_input()
        await element.send_keys(text)

    async def ele_highlight_overlay(self, element):
        return await element.highlight_overlay_async()

    async def ele_get_position(self, element):
        return await element.get_position_async()

    async def ele_get_html(self, element):
        return await element.get_html_async()

    async def ele_get_js_attributes(self, element):
        return await element.get_js_attributes_async()

    async def ele_get_attribute(self, element, attribute):
        try:
            return (await element.get_js_attributes())[attribute]
        except Exception as e:
            if not attribute:
                raise
            try:
                attribute_str = await element.get_js_attributes()
                locate = ' %s="' % attribute
                if locate in attribute_str.outerHTML:
                    outer_html = attribute_str.outerHTML
                    attr_start = outer_html.find(locate) + len(locate)
                    attr_end = outer_html.find('"', attr_start)
                    value = outer_html[attr_start:attr_end]
                    return value
            except Exception:
                pass
        return None

    async def ele_get_parent(self, element):
        return self.cdp.add_element_methods(element.parent)

    async def ele_query_selector(self, element, selector):
        selector = js_utils.to_css_if_xpath(selector)
        element2 = await element.query_selector_async(selector)
        element2 = self.cdp.add_element_methods(element2)
        return element2

    async def ele_query_selector_all(self, element, selector):
        selector = js_utils.to_css_if_xpath(selector)
        elements = await element.query_selector_all_async(selector)
        updated_elements = []
        for element in elements:
            element = self.cdp.add_element_methods(element)
            updated_elements.append(element)
        return updated_elements

    async def ele_shadow_root_query_selector(self, element, selector: str):
        selector = js_utils.to_css_if_xpath(selector)
        element2 = await element.shadow_root_query_selector_async(selector)
        element2 = self.cdp.add_element_methods(element2)
        return element2

    async def ele_shadow_root_query_selector_all(self, element, selector):
        selector = js_utils.to_css_if_xpath(selector)
        elements = await element.shadow_root_query_selector_all_async(selector)
        updated_elements = []
        for element in elements:
            element = self.cdp.add_element_methods(element)
            updated_elements.append(element)
        return updated_elements
