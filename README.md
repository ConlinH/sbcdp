
# SBCDP - 纯CDP自动化框架

SBCDP - Pure CDP (Chrome DevTools Protocol) Automation Framework

## 项目来源 | Project Origin

SBCDP 是基于 SeleniumBase 项目重构而来的纯CDP自动化框架。提取了SeleniumBase中的CDP功能，并进行了完全重构，创建了一个清晰分离同步和异步操作的现代化自动化框架。

SBCDP is a pure CDP automation framework refactored from the SeleniumBase project. extracted the CDP functionality from SeleniumBase and completely refactored it to create a modern automation framework with clear separation of synchronous and asynchronous operations.

## 功能特性 | Features

### 🏗️ 清晰的架构设计 | Clear Architecture Design
- **完全分离**: 同步和异步代码完全独立，无混合模式复杂性
- **模块化设计**: 基础类、方法类、接口类分层架构
- **代码复用**: 通过继承和混入实现功能复用

- **Complete Separation**: Synchronous and asynchronous code are completely independent, no hybrid mode complexity
- **Modular Design**: Layered architecture with base classes, method classes, and interface classes
- **Code Reuse**: Functionality reuse through inheritance and mixins

### ⚡ 高性能并发 | High-Performance Concurrency
- **真正异步**: 原生异步实现，支持真正的并发执行
- **性能优化**: 异步版本比传统方法快3-10倍
- **资源高效**: 更好的CPU和内存利用率

- **True Async**: Native async implementation supporting true concurrent execution
- **Performance Optimized**: Async version is 3-10x faster than traditional methods
- **Resource Efficient**: Better CPU and memory utilization

### 🎯 易于使用 | Easy to Use
- **简洁API**: 清晰直观的接口设计
- **双重选择**: 同步接口简单直接，异步接口高性能
- **向后兼容**: 100%兼容现有代码

- **Clean API**: Clear and intuitive interface design
- **Dual Choice**: Sync interface is simple and direct, async interface is high-performance
- **Backward Compatible**: 100% compatible with existing code

### 🔧 功能完整 | Feature Complete
- **32个核心方法**: 涵盖所有常用自动化操作
- **增强交互**: 鼠标操作、键盘输入、视觉效果等
- **表单处理**: 完整的表单操作支持
- **截图功能**: 页面和元素截图

- **32 Core Methods**: Covering all common automation operations
- **Enhanced Interaction**: Mouse operations, keyboard input, visual effects, etc.
- **Form Handling**: Complete form operation support
- **Screenshot Functionality**: Page and element screenshots

## 安装 | Installation

### 使用pip安装 | Install with pip

```bash
pip install sbcdp
```

### 开发版本安装 | Development Installation

```bash
git clone https://github.com/ConlinH/sbcdp.git
cd sbcdp
pip install -e .
```

## 快速开始 | Quick Start


### 异步接口 | Asynchronous Interface

```python
import asyncio
from sbcdp import AsyncChrome as Chrome

async def main():
    async with Chrome() as chrome:
        await chrome.get("https://httpbin.org/forms/post")
        await chrome.type('input[name="custname"]', "sbcdp 用户")
        await chrome.type('input[name="custtel"]', "123-456-7890")
        await chrome.type('input[name="custemail"]', "test@cdp-base.com")
        await chrome.type('textarea[name="comments"]', "这是使用sbcdp框架的测试")

        # 选择单选按钮
        await chrome.click('input[value="large"]')
        # 等待元素
        element = await chrome.find_element("button")
        await element.click()
        await chrome.sleep(2)

if __name__ == '__main__':
    asyncio.new_event_loop().run_until_complete(main())
    # asyncio.run(main())
```

### 同步接口 | Synchronous Interface

```python
from sbcdp import SyncChrome as Chrome

with Chrome() as chrome:
    chrome.get("https://httpbin.org/forms/post")
    chrome.type('input[name="custname"]', "sbcdp 用户")
    chrome.type('input[name="custtel"]', "123-456-7890")
    chrome.type('input[name="custemail"]', "test@cdp-base.com")
    chrome.type('textarea[name="comments"]', "这是使用sbcdp框架的测试")

    # 选择单选按钮
    chrome.click('input[value="large"]')
    # 等待元素
    element = chrome.find_element("button")
    element.click()
    chrome.sleep(2)
```

### 5s盾 | cloudflare

```python
import asyncio
from contextlib import suppress

from sbcdp import AsyncChrome as Chrome


async def main():
    # url = "https://fractal-testnet.unisat.io/explorer"
    url = "https://steamdb.info/"
    # url = "https://cn.airbusan.com/content/individual"
    # url = "https://pastebin.com/login"
    # url = "https://simple.ripley.com.pe/"
    # url = "https://www.e-food.gr/"
    async with Chrome() as chrome:
        await chrome.get(url)
        await chrome.sleep(5)
        with suppress(Exception):
            await chrome.mouse_click('input[type=checkbox]')
        assert 'cf_clearance' in {c.name: c.value for c in await chrome.get_all_cookies()}
        print({c.name: c.value for c in await chrome.get_all_cookies()})


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(main())
    # asyncio.run(main())
```

## 核心方法 | Core Methods

### 基础操作 | Basic Operations
- `get(url)` - 导航到URL | Navigate to URL
- `click(selector)` - 点击元素 | Click element
- `type(selector, text)` - 输入文本 | Type text
- `get_text(selector)` - 获取文本 | Get text
- `get_attribute(selector, attr)` - 获取属性 | Get attribute

### 增强交互 | Enhanced Interaction
- `mouse_click(selector)` - 鼠标点击 | Mouse click
- `press_keys(selector, text)` - 按键输入 | Press keys
- `focus(selector)` - 聚焦元素 | Focus element
- `scroll_to_element(selector)` - 滚动到元素 | Scroll to element

### 视觉效果 | Visual Effects
- `flash(selector)` - 闪烁元素 | Flash element
- `highlight(selector)` - 高亮元素 | Highlight element
- `highlight_overlay(selector)` - 高亮覆盖 | Highlight overlay

### 表单操作 | Form Operations
- `select_option_by_text(selector, text)` - 选择选项 | Select option
- `set_value(selector, value)` - 设置值 | Set value
- `set_text(selector, text)` - 设置文本 | Set text

### 截图功能 | Screenshot Functions
- `save_screenshot(filename)` - 保存页面截图 | Save page screenshot
- `save_element_screenshot(selector, filename)` - 保存元素截图 | Save element screenshot

## 架构设计 | Architecture Design

```
sbcdp/
├── core/           # 核心模块 | Core Modules
│   ├── chrome.py   # Chrome类 | Chrome Class
│   └── methods.py  # 方法实现 | Method Implementation
├── driver/         # 驱动模块 | Driver Modules
├── config/         # 配置模块 | Configuration Modules
└── fixtures/       # 工具模块 | Utility Modules
```

## 测试 | Testing

### 运行测试 | Run Tests

```bash
# 运行所有测试 | Run all tests
pytest

# 运行同步测试 | Run sync tests
pytest tests/test_sync_chrome.py

# 运行异步测试 | Run async tests
pytest tests/test_async_chrome.py

# 带覆盖率测试 | Run with coverage
pytest --cov=sbcdp
```

### 测试覆盖 | Test Coverage

项目包含完整的测试套件，覆盖：
- 同步和异步接口测试
- 错误处理测试
- 并发性能测试

The project includes a complete test suite covering:
- Synchronous and asynchronous interface tests
- Error handling tests
- Concurrent performance tests

## 贡献 | Contributing

欢迎贡献代码！请遵循以下步骤：

We welcome contributions! Please follow these steps:

1. Fork 项目 | Fork the project
2. 创建特性分支 | Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 提交更改 | Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 | Push to the branch (`git push origin feature/AmazingFeature`)
5. 打开Pull Request | Open a Pull Request

## 许可证 | License

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 致谢 | Acknowledgments

- 感谢 [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) 项目提供的基础代码
- 感谢所有贡献者的努力和支持

- Thanks to the [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) project for providing the foundation code
- Thanks to all contributors for their efforts and support

## 联系方式 | Contact

- 项目主页 | Project Homepage: https://github.com/ConlinH/sbcdp
- 问题反馈 | Issue Tracker: https://github.com/ConlinH/sbcdp/issues
- 邮箱 | Email: 995018884@qq.com

---

**SBCDP - 让自动化更简单、更快速、更可靠！**

**SBCDP - Making automation simpler, faster, and more reliable!**
