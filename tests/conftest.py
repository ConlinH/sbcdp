"""
pytest配置文件
"""

import pytest
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环fixture"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sync_chrome():
    """同步Chrome fixture"""
    from sbcdp import SyncChrome
    chrome = SyncChrome()
    yield chrome
    chrome.close()


@pytest.fixture
async def async_chrome():
    """异步Chrome fixture"""
    from sbcdp import AsyncChrome
    chrome = AsyncChrome()
    yield chrome
    await chrome.close()


# pytest配置
def pytest_configure(config):
    """pytest配置"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试项目"""
    # 为异步测试添加asyncio标记
    for item in items:
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)


# 测试环境设置
@pytest.fixture(autouse=True)
def setup_test_environment():
    """设置测试环境"""
    # 在每个测试前运行
    yield
    # 在每个测试后运行（清理）
    pass


# 跳过条件
def pytest_runtest_setup(item):
    """测试运行前设置"""
    # 可以在这里添加跳过条件
    pass
