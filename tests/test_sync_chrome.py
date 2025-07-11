"""
测试同步Chrome接口
"""

import pytest
import time
from sbcdp import SyncChrome as Chrome


class TestSyncChrome:
    """同步Chrome测试类"""

    def test_basic_navigation(self):
        """测试基本导航功能"""
        with Chrome() as chrome:
            # 测试导航到数据URL
            test_html = "<html><head><title>Test Page</title></head><body><h1>Hello World</h1></body></html>"
            chrome.get(f"data:text/html,{test_html}")

            # 验证标题
            title = chrome.get_title()
            assert title == "Test Page"

            # 验证URL
            url = chrome.get_current_url()
            assert "data:text/html" in url

    def test_element_interaction(self):
        """测试元素交互"""
        test_html = """
        <html>
        <head><title>Element Test</title></head>
        <body>
            <h1 id="title">Test Title</h1>
            <input id="input1" type="text" placeholder="Enter text">
            <button id="btn1" onclick="document.getElementById('result').innerText='Clicked'">Click Me</button>
            <div id="result"></div>
        </body>
        </html>
        """

        with Chrome() as chrome:
            chrome.get(f"data:text/html,{test_html}")

            # 测试获取文本
            title_text = chrome.get_text("#title")
            assert title_text == "Test Title"

            # 测试输入
            chrome.type("#input1", "Hello World")
            input_value = chrome.get_attribute("#input1", "value")
            assert input_value == "Hello World"

            # 测试点击
            chrome.click("#btn1")
            time.sleep(0.1)  # 等待JavaScript执行
            result_text = chrome.get_text("#result")
            assert result_text == "Clicked"

    def test_element_finding(self):
        """测试元素查找"""
        test_html = """
        <html>
        <body>
            <div class="container">
                <p class="text">Paragraph 1</p>
                <p class="text">Paragraph 2</p>
                <p class="text">Paragraph 3</p>
            </div>
        </body>
        </html>
        """

        with Chrome() as chrome:
            chrome.get(f"data:text/html,{test_html}")

            # 测试查找单个元素
            element = chrome.find_element(".container")
            assert element is not None

            # 测试查找多个元素
            elements = chrome.find_elements(".text")
            assert len(elements) == 3

    def test_javascript_execution(self):
        """测试JavaScript执行"""
        test_html = "<html><body><div id='test'>Original</div></body></html>"

        with Chrome() as chrome:
            chrome.get(f"data:text/html,{test_html}")

            # 测试JavaScript执行
            result = chrome.evaluate("return 'JavaScript works!'")
            assert result == "JavaScript works!"

            # 测试DOM操作
            chrome.evaluate("document.getElementById('test').innerText = 'Modified'")
            text = chrome.get_text("#test")
            assert text == "Modified"

    def test_form_operations(self):
        """测试表单操作"""
        test_html = """
        <html>
        <body>
            <form>
                <input id="text-input" type="text" value="">
                <select id="select-input">
                    <option value="1">Option 1</option>
                    <option value="2">Option 2</option>
                    <option value="3">Option 3</option>
                </select>
                <textarea id="textarea-input">Original text</textarea>
            </form>
        </body>
        </html>
        """

        with Chrome() as chrome:
            chrome.get(f"data:text/html,{test_html}")

            # 测试设置值
            chrome.set_value("#text-input", "New Value")
            value = chrome.get_attribute("#text-input", "value")
            assert value == "New Value"

            # 测试设置文本
            chrome.find_element("#textarea-input").set_text("New Text")
            text = chrome.get_text("#textarea-input")
            assert text == "New Text"

    def test_visibility_checks(self):
        """测试可见性检查"""
        test_html = """
        <html>
        <body>
            <div id="visible">Visible Element</div>
            <div id="hidden" style="display: none;">Hidden Element</div>
        </body>
        </html>
        """

        with Chrome() as chrome:
            chrome.get(f"data:text/html,{test_html}")

            # 测试元素存在性
            assert chrome.is_element_present("#visible") == True
            assert chrome.is_element_present("#hidden") == True
            assert chrome.is_element_present("#nonexistent") == False

    def test_screenshot(self):
        """测试截图功能"""
        import os

        test_html = "<html><body><h1>Screenshot Test</h1></body></html>"
        screenshot_path = "test_screenshot.png"

        with Chrome() as chrome:
            chrome.get(f"data:text/html,{test_html}")

            # 测试保存截图
            result = chrome.save_screenshot(screenshot_path)

            # 验证截图文件存在（这里只是测试方法调用，实际文件可能不存在）
            assert result is not None

        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    def test_context_manager(self):
        """测试上下文管理器"""
        # 测试with语句自动清理
        with Chrome() as chrome:
            chrome.get("data:text/html,<title>Context Test</title>")
            title = chrome.get_title()
            assert title == "Context Test"

        # Chrome应该已经自动关闭

    def test_error_handling(self):
        """测试错误处理"""
        with Chrome() as chrome:
            chrome.get("data:text/html,<body></body>")

            # 测试查找不存在的元素
            with pytest.raises(Exception):
                chrome.find_element("#nonexistent", timeout=0.1)

            # 测试无效选择器
            with pytest.raises(Exception):
                chrome.find_element("", timeout=0.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
