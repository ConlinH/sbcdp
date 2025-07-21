"""
SBCDP 等待方法模块
处理各种等待和断言操作
"""

import time
import asyncio
from contextlib import suppress
from typing import Optional

from .base import Base
from .. import settings
from ..fixtures import js_utils


class Wait(Base):
    """等待方法类"""

    async def is_element_present(self, selector):
        """检查元素是否存在"""
        try:
            await self.cdp.select(selector, timeout=0.01)
            return True
        except Exception:
            return False

    async def is_element_visible(self, selector):
        """检查元素是否可见"""
        selector = js_utils.to_css_if_xpath(selector)
        try:
            element = await self.cdp.select(selector, timeout=0.1)
            with suppress(Exception):
                position = element.get_position()
                if position.width != 0 or position.height != 0:
                    return True
        except Exception:
            pass
        return False

    async def is_text_visible(self, text, selector="body"):
        """检查文本是否可见"""
        selector = js_utils.to_css_if_xpath(selector)
        text = text.strip()
        element = None
        try:
            element = await self.cdp.find_element(selector, timeout=0.1)
        except Exception:
            return False
        with suppress(Exception):
            if text in await element.text_all:
                return True
        return False

    async def is_exact_text_visible(self, text, selector="body"):
        """检查精确文本是否可见"""
        selector = js_utils.to_css_if_xpath(selector)
        text = text.strip()
        element = None
        try:
            element = await self.cdp.find_element(selector, timeout=0.1)
        except Exception:
            return False
        with suppress(Exception):
            if text == element.text_all.strip():
                return True
        return False

    async def wait_for_element_visible(self, selector, timeout=None):
        """等待元素可见"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        try:
            await self.cdp.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} was not found!" % selector)
        for i in range(30):
            if await self.is_element_visible(selector):
                return await self.cdp.select(selector)
            await asyncio.sleep(0.1)
        raise Exception("Element {%s} was not visible!" % selector)

    async def wait_for_element_not_visible(self, selector, timeout=None):
        """等待元素不可见"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            if not await self.is_element_present(selector):
                return True
            elif not await self.is_element_visible(selector):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            await asyncio.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Element {%s} was still visible after %s second%s!"
            % (selector, timeout, plural)
        )

    async def wait_for_element_absent(self, selector, timeout=None):
        """等待元素从DOM中消失"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            if not await self.is_element_present(selector):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            await asyncio.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Element {%s} was still present after %s second%s!"
            % (selector, timeout, plural)
        )

    async def wait_for_text(self, text, selector="body", timeout=None):
        """等待文本出现"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        text = text.strip()
        element = None
        try:
            element = await self.cdp.find_element(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(int(timeout * 10)):
            with suppress(Exception):
                element = await self.cdp.find_element(selector, timeout=0.1)
            if text in element.text_all:
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            await asyncio.sleep(0.1)
        raise Exception(
            "Text {%s} not found in {%s}! Actual text: {%s}"
            % (text, selector, element.text_all)
        )

    async def wait_for_text_not_visible(self, text, selector="body", timeout=None):
        """等待文本不可见"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        text = text.strip()
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout * 10)):
            if not await self.is_text_visible(text, selector):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            await asyncio.sleep(0.1)
        plural = "s"
        if timeout == 1:
            plural = ""
        raise Exception(
            "Text {%s} in {%s} was still visible after %s second%s!"
            % (text, selector, timeout, plural)
        )

    async def assert_element(self, selector, timeout=None):
        """断言元素存在且可见"""
        await self.assert_element_visible(selector, timeout=timeout)
        return True

    async def assert_element_visible(self, selector, timeout=None):
        """断言元素可见"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        try:
            await self.cdp.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} was not found!" % selector)
        for i in range(30):
            if await self.is_element_visible(selector):
                return True
            await asyncio.sleep(0.1)
        raise Exception("Element {%s} was not visible!" % selector)

    async def assert_text(self, text, selector="body", timeout=None):
        """断言文本存在"""
        await self.wait_for_text(text, selector=selector, timeout=timeout)
        return True

    async def assert_exact_text(self, text, selector="body", timeout=None):
        """断言精确文本存在"""
        if not timeout:
            timeout = settings.SMALL_TIMEOUT
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        text = text.strip()
        element = None
        try:
            element = await self.cdp.select(selector, timeout=timeout)
        except Exception:
            raise Exception("Element {%s} not found!" % selector)
        for i in range(int(timeout * 10)):
            with suppress(Exception):
                element = await self.cdp.select(selector, timeout=0.1)
            if (
                await self.is_element_visible(selector)
                and text.strip() == element.text_all.strip()
            ):
                return True
            now_ms = time.time() * 1000.0
            if now_ms >= stop_ms:
                break
            await asyncio.sleep(0.1)
        raise Exception(
            "Expected Text {%s}, is not equal to {%s} in {%s}!"
            % (text, element.text_all, selector)
        )

    async def sleep(self, seconds):
        """等待指定秒数"""
        await asyncio.sleep(seconds)

    async def wait_for(
            self,
            selector: Optional[str] = "",
            text: Optional[str] = "",
            timeout: Optional[float] = 10
    ):
        """通用等待方法"""
        return await self.cdp.page.wait_for(selector, text, timeout=timeout)
