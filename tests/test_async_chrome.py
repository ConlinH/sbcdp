"""
测试异步Chrome接口
"""

import pytest
import asyncio
from sbcdp import AsyncChrome as Chrome


class TestAsyncChrome:
    """异步Chrome测试类"""

    @pytest.mark.asyncio
    async def test_basic_navigation(self):
        """测试基本导航功能"""
        async with Chrome() as chrome:
            # 测试导航到数据URL
            test_html = "<html><head><title>Async Test Page</title></head><body><h1>Hello Async World</h1></body></html>"
            await chrome.get(f"data:text/html,{test_html}")

            # 验证标题
            title = await chrome.get_title()
            assert title == "Async Test Page"

            # 验证URL
            url = await chrome.get_current_url()
            assert "data:text/html" in url

    @pytest.mark.asyncio
    async def test_element_interaction(self):
        """测试元素交互"""
        test_html = """
        <html>
        <head><title>Async Element Test</title></head>
        <body>
            <h1 id="title">Async Test Title</h1>
            <input id="input1" type="text" placeholder="Enter text">
            <button id="btn1" onclick="document.getElementById('result').innerText='Async Clicked'">Click Me</button>
            <div id="result"></div>
        </body>
        </html>
        """

        async with Chrome() as chrome:
            await chrome.get(f"data:text/html,{test_html}")

            # 测试获取文本
            title_text = await chrome.get_text("#title")
            assert title_text == "Async Test Title"

            # 测试输入
            await chrome.type("#input1", "Hello Async World")
            input_value = await chrome.get_attribute("#input1", "value")
            assert input_value == "Hello Async World"

            # 测试点击
            await chrome.click("#btn1")
            await asyncio.sleep(0.1)  # 等待JavaScript执行
            result_text = await chrome.get_text("#result")
            assert result_text == "Async Clicked"

    @pytest.mark.asyncio
    async def test_element_finding(self):
        """测试元素查找"""
        test_html = """
        <html>
        <body>
            <div class="async-container">
                <p class="async-text">Async Paragraph 1</p>
                <p class="async-text">Async Paragraph 2</p>
                <p class="async-text">Async Paragraph 3</p>
            </div>
        </body>
        </html>
        """

        async with Chrome() as chrome:
            await chrome.get(f"data:text/html,{test_html}")

            # 测试查找单个元素
            element = await chrome.find_element(".async-container")
            assert element is not None

            # 测试查找多个元素
            elements = await chrome.find_elements(".async-text")
            assert len(elements) == 3

    @pytest.mark.asyncio
    async def test_javascript_execution(self):
        """测试JavaScript执行"""
        test_html = "<html><body><div id='async-test'>Original Async</div></body></html>"

        async with Chrome() as chrome:
            await chrome.get(f"data:text/html,{test_html}")

            # 测试JavaScript执行
            result = await chrome.evaluate("return 'Async JavaScript works!'")
            assert result == "Async JavaScript works!"

            # 测试DOM操作
            await chrome.evaluate("document.getElementById('async-test').innerText = 'Modified Async'")
            text = await chrome.get_text("#async-test")
            assert text == "Modified Async"

    @pytest.mark.asyncio
    async def test_form_operations(self):
        """测试表单操作"""
        test_html = """
        <html>
        <body>
            <form>
                <input id="async-text-input" type="text" value="">
                <select id="async-select-input">
                    <option value="1">Async Option 1</option>
                    <option value="2">Async Option 2</option>
                    <option value="3">Async Option 3</option>
                </select>
                <textarea id="async-textarea-input">Original async text</textarea>
            </form>
        </body>
        </html>
        """

        async with Chrome() as chrome:
            await chrome.get(f"data:text/html,{test_html}")

            # 测试设置值
            await chrome.set_value("#async-text-input", "New Async Value")
            value = await chrome.get_attribute("#async-text-input", "value")
            assert value == "New Async Value"

            # 测试设置文本
            ele = await chrome.find_element("#async-textarea-input")
            await ele.set_text("New Async Text")
            text = await chrome.get_text("#async-textarea-input")
            assert text == "New Async Text"

    @pytest.mark.asyncio
    async def test_visibility_checks(self):
        """测试可见性检查"""
        test_html = """
        <html>
        <body>
            <div id="async-visible">Async Visible Element</div>
            <div id="async-hidden" style="display: none;">Async Hidden Element</div>
        </body>
        </html>
        """

        async with Chrome() as chrome:
            await chrome.get(f"data:text/html,{test_html}")

            # 测试元素存在性
            assert await chrome.is_element_present("#async-visible") == True
            assert await chrome.is_element_present("#async-hidden") == True
            assert await chrome.is_element_present("#async-nonexistent") == False

    @pytest.mark.asyncio
    async def test_screenshot(self):
        """测试截图功能"""
        import os

        test_html = "<html><body><h1>Async Screenshot Test</h1></body></html>"
        screenshot_path = "test_async_screenshot.png"

        async with Chrome() as chrome:
            await chrome.get(f"data:text/html,{test_html}")

            # 测试保存截图
            result = await chrome.save_screenshot(screenshot_path)

            # 验证截图文件存在（这里只是测试方法调用，实际文件可能不存在）
            assert result is not None

        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """测试并发操作"""

        async def get_page_info(page_num):
            async with Chrome() as chrome:
                test_html = f"<html><head><title>Page {page_num}</title></head><body><h1>Content {page_num}</h1></body></html>"
                await chrome.get(f"data:text/html,{test_html}")

                title = await chrome.get_title()
                text = await chrome.get_text("h1")
                return f"{title}: {text}"

        # 并发执行多个任务
        tasks = [get_page_info(i) for i in range(1, 4)]
        results = await asyncio.gather(*tasks)

        assert len(results) == 3
        assert "Page 1: Content 1" in results
        assert "Page 2: Content 2" in results
        assert "Page 3: Content 3" in results

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """测试异步上下文管理器"""
        # 测试async with语句自动清理
        async with Chrome() as chrome:
            await chrome.get("data:text/html,<title>Async Context Test</title>")
            title = await chrome.get_title()
            assert title == "Async Context Test"

        # Chrome应该已经自动关闭

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """测试错误处理"""
        async with Chrome() as chrome:
            await chrome.get("data:text/html,<body></body>")

            # 测试查找不存在的元素
            with pytest.raises(Exception):
                await chrome.find_element("#async-nonexistent", timeout=0.1)

            # 测试无效选择器
            with pytest.raises(Exception):
                await chrome.find_element("", timeout=0.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
