"""
SBCDP 异步方法实现 - 重构版
使用组合模式 + 代理模式拆分原来臃肿的AsyncCDPMethods类
"""

import asyncio
from typing import Optional, Callable

from ..driver.tab import Tab
from ..driver.browser import Browser

# 使用组合模式集成各个API模块
from .navigation import Navigation
from .dom import Dom
from .action import Action
from .wait import Wait
from .page_info import PageInfo
from .gui import GUI
from .network import NetWork, NetHttp


class AsyncCDP:
    """异步CDP方法类 - 使用组合模式重构"""

    def __init__(self, page: Tab, driver: Browser):
        self.page = page
        self.driver = driver

        self.__navigation = Navigation(self)
        self.__dom = Dom(self)
        self.__action = Action(self)
        self.__wait = Wait(self)
        self.__page_info = PageInfo(self)
        self.__gui = GUI(self)
        self.__net = NetWork(self)

        self.__reg_navigation()
        self.__reg_dom()
        self.__reg_action()
        self.__reg_wait()
        self.__reg_page_info()
        self.__reg_gui()
        self.__reg_net()

    def __reg_navigation(self):
        # 导航到指定URL
        self.get = self.__navigation.get
        self.open = self.__navigation.open
        # 刷新页面
        self.reload = self.__navigation.reload
        self.refresh = self.__navigation.reload
        # 后退
        self.go_back = self.__navigation.go_back
        # 前进
        self.go_forward = self.__navigation.go_forward
        # 获取导航历史
        self.history = self.__navigation.get_navigation_history
        self.get_navigation_history = self.__navigation.get_navigation_history
        # 打开新标签页
        self.open_new_tab = self.__navigation.open_new_tab
        # 打开新窗口
        self.open_new_window = self.__navigation.open_new_window
        # 切换到指定标签页
        self.switch_to_tab = self.__navigation.switch_to_tab
        # 切换到最新的标签页
        self.switch_to_newest_tab = self.__navigation.switch_to_newest_tab
        # 切换到指定窗口
        self.switch_to_window = self.__navigation.switch_to_window
        # 切换到最新的窗口
        self.switch_to_newest_window = self.__navigation.switch_to_newest_window
        # 关闭当前活动的标签页
        self.close_active_tab = self.__navigation.close_active_tab
        # 获取当前活动的标签页
        self.get_active_tab = self.__navigation.get_active_tab
        # 获取所有标签页
        self.get_tabs = self.__navigation.get_tabs
        # 获取窗口信息
        self.get_window = self.__navigation.get_window
        # 将活动窗口置于前台
        self.bring_active_window_to_front = self.__navigation.bring_active_window_to_front
        # 平铺窗口
        self.tile_windows = self.__navigation.tile_windows
        # 授予权限
        self.grant_permissions = self.__navigation.grant_permissions
        # 授予所有权限
        self.grant_all_permissions = self.__navigation.grant_all_permissions

    def __reg_dom(self):
        # 查找单个元素
        self.find_element = self.__dom.find_element
        # 通过文本内容查找元素
        self.find_element_by_text = self.__dom.find_element_by_text
        # 通过文本内容查找多个元素
        self.find_elements_by_text = self.__dom.find_elements_by_text
        # 查找所有匹配的元素
        self.find_all = self.__dom.find_all
        # 选择单个元素
        self.select = self.__dom.select
        # 选择所有匹配的元素
        self.select_all = self.__dom.select_all
        # 查找多个元素
        self.find_elements = self.__dom.find_elements
        # 查找所有可见的元素
        self.find_visible_elements = self.__dom.find_visible_elements
        # 点击元素
        self.click = self.__dom.click
        # 点击第N个匹配的元素
        self.click_nth_element = self.__dom.click_nth_element
        # 点击第N个可见的元素
        self.click_nth_visible_element = self.__dom.click_nth_visible_element
        # 点击链接文本
        self.click_link = self.__dom.click_link
        # 模拟鼠标点击
        self.mouse_click = self.__dom.mouse_click
        # 在父元素内点击子元素
        self.nested_click = self.__dom.nested_click
        # 获取父元素内的子元素
        self.get_nested_element = self.__dom.get_nested_element
        # 获取当前活动的元素
        self.get_active_element = self.__dom.get_active_element
        # 获取当前活动元素的CSS选择器
        self.get_active_element_css = self.__dom.get_active_element_css

        # 扩展element方法
        self.ele_query_selector = self.__dom.ele_query_selector
        self.ele_query_selector_all = self.__dom.ele_query_selector_all
        self.ele_shadow_root_query_selector = self.__dom.ele_shadow_root_query_selector
        self.ele_shadow_root_query_selector_all = self.__dom.ele_shadow_root_query_selector_all
        self.ele_highlight_overlay = self.__dom.ele_highlight_overlay
        self.ele_type = self.__dom.ele_type
        self.ele_remove_from_dom = self.__dom.ele_remove_from_dom
        self.ele_save_to_dom = self.__dom.ele_save_to_dom
        self.ele_get_position = self.__dom.ele_get_position
        self.ele_get_html = self.__dom.ele_get_html
        self.ele_get_js_attributes = self.__dom.ele_get_js_attributes
        self.ele_get_attribute = self.__dom.ele_get_attribute
        self.ele_get_parent = self.__dom.ele_get_parent

    def __reg_action(self):
        # 向元素发送按键
        self.send_keys = self.__action.send_keys
        # 以人类速度按键
        self.press_keys = self.__action.press_keys
        # 输入文本（先清空字段）
        self.type = self.__action.type
        # 设置元素值
        self.set_value = self.__action.set_value
        # 清空输入字段
        self.clear = self.__action.clear
        # 提交表单
        self.submit = self.__action.submit
        # 获取元素文本
        self.get_text = self.__action.get_text
        # 获取元素属性值
        self.get_attribute = self.__action.get_attribute
        # 获取元素属性值（带异常处理）
        self.get_element_attribute = self.__action.get_element_attribute
        # 获取元素所有属性
        self.get_element_attributes = self.__action.get_element_attributes
        # 获取元素HTML
        self.get_element_html = self.__action.get_element_html
        # 设置元素属性
        self.set_attribute = self.__action.set_attribute
        # 为所有匹配元素设置属性
        self.set_attributes = self.__action.set_attributes
        # 移除元素属性
        self.remove_attribute = self.__action.remove_attribute
        # 移除所有匹配元素的属性
        self.remove_attributes = self.__action.remove_attributes
        # 移除所有匹配的元素
        self.remove_elements = self.__action.remove_elements
        # 设置语言环境
        self.set_locale = self.__action.set_locale
        # 将所有target="_blank"链接改为target="_self"
        self.internalize_links = self.__action.internalize_links

        # 扩展element方法
        self.ele_send_keys = self.__action.ele_send_keys
        self.ele_scroll_into_view = self.__action.ele_scroll_into_view
        self.ele_click = self.__action.ele_click
        self.ele_flash = self.__action.ele_flash
        self.ele_focus = self.__action.ele_focus
        self.ele_mouse_click = self.__action.ele_mouse_click
        self.ele_mouse_drag = self.__action.ele_mouse_drag
        self.ele_mouse_move = self.__action.ele_mouse_move
        self.ele_press_keys = self.__action.ele_press_keys
        self.ele_set_text = self.__action.ele_set_text
        self.ele_set_value = self.__action.ele_set_value
        self.ele_send_file = self.__action.ele_send_file
        self.ele_clear_input = self.__action.ele_clear_input
        self.ele_select_option = self.__action.ele_select_option

    def __reg_wait(self):
        # 检查元素是否存在
        self.is_element_present = self.__wait.is_element_present
        # 检查元素是否可见
        self.is_element_visible = self.__wait.is_element_visible
        # 检查文本是否可见
        self.is_text_visible = self.__wait.is_text_visible
        # 检查精确文本是否可见
        self.is_exact_text_visible = self.__wait.is_exact_text_visible
        # 等待元素可见
        self.wait_for_element_visible = self.__wait.wait_for_element_visible
        # 等待元素不可见
        self.wait_for_element_not_visible = self.__wait.wait_for_element_not_visible
        # 等待元素从DOM中消失
        self.wait_for_element_absent = self.__wait.wait_for_element_absent
        # 等待文本出现
        self.wait_for_text = self.__wait.wait_for_text
        # 等待文本不可见
        self.wait_for_text_not_visible = self.__wait.wait_for_text_not_visible
        # 断言元素存在且可见
        self.assert_element = self.__wait.assert_element
        # 断言元素可见
        self.assert_element_visible = self.__wait.assert_element_visible
        # 断言文本存在
        self.assert_text = self.__wait.assert_text
        # 断言精确文本存在
        self.assert_exact_text = self.__wait.assert_exact_text
        # 等待指定秒数
        self.sleep = self.__wait.sleep
        # 通用等待方法
        self.wait_for = self.__wait.wait_for

    def __reg_page_info(self):
        # 获取页面标题
        self.get_title = self.__page_info.get_title
        # 获取当前URL
        self.get_current_url = self.__page_info.get_current_url
        # 获取页面来源
        self.get_origin = self.__page_info.get_origin
        # 获取页面源码
        self.get_page_source = self.__page_info.get_page_source
        # 获取用户代理
        self.get_user_agent = self.__page_info.get_user_agent
        # 获取Cookie字符串
        self.get_cookie_string = self.__page_info.get_cookie_string
        # 获取Cookies
        self.get_all_cookies = self.__page_info.get_all_cookies
        # 获取语言代码
        self.get_locale_code = self.__page_info.get_locale_code
        # 获取localStorage项
        self.get_local_storage_item = self.__page_info.get_local_storage_item
        # 获取sessionStorage项
        self.get_session_storage_item = self.__page_info.get_session_storage_item
        # 获取屏幕矩形信息
        self.get_screen_rect = self.__page_info.get_screen_rect
        # 获取元素矩形信息
        self.get_element_rect = self.__page_info.get_element_rect
        # 获取GUI元素矩形信息
        self.get_gui_element_rect = self.__page_info.get_gui_element_rect
        # 获取GUI元素中心点坐标
        self.get_gui_element_center = self.__page_info.get_gui_element_center
        # 获取窗口矩形信息
        self.get_window_rect = self.__page_info.get_window_rect
        # 获取文档对象
        self.get_document = self.__page_info.get_document
        # 获取扁平化文档对象
        self.get_flattened_document = self.__page_info.get_flattened_document
        # 执行JavaScript表达式
        self.evaluate = self.__page_info.evaluate
        # 执行JavaScript脚本
        self.execute_script = self.__page_info.execute_script
        # 保存截图
        self.save_screenshot = self.__page_info.save_screenshot
        # 打印为PDF
        self.print_to_pdf = self.__page_info.print_to_pdf
        # 滚动元素到可视区域
        self.scroll_into_view = self.__page_info.scroll_into_view
        # 滚动到指定Y坐标
        self.scroll_to_y = self.__page_info.scroll_to_y
        # 滚动到页面顶部
        self.scroll_to_top = self.__page_info.scroll_to_top
        # 滚动到页面底部
        self.scroll_to_bottom = self.__page_info.scroll_to_bottom
        # 向上滚动
        self.scroll_up = self.__page_info.scroll_up
        # 向下滚动
        self.scroll_down = self.__page_info.scroll_down
        # 设置localStorage项
        self.set_local_storage_item = self.__page_info.set_local_storage_item
        # 设置sessionStorage项
        self.set_session_storage_item = self.__page_info.set_session_storage_item

    def __reg_gui(self):
        # GUI按键
        self.gui_press_key = self.__gui.gui_press_key
        # GUI按多个键
        self.gui_press_keys = self.__gui.gui_press_keys
        # GUI写入文本
        self.gui_write = self.__gui.gui_write
        # GUI点击坐标
        self.gui_click_x_y = self.__gui.gui_click_x_y
        # GUI点击元素
        self.gui_click_element = self.__gui.gui_click_element
        # GUI拖拽坐标点
        self.gui_drag_drop_points = self.__gui.gui_drag_drop_points
        # GUI拖拽元素
        self.gui_drag_and_drop = self.__gui.gui_drag_and_drop
        # GUI点击并保持
        self.gui_click_and_hold = self.__gui.gui_click_and_hold
        # GUI悬停坐标
        self.gui_hover_x_y = self.__gui.gui_hover_x_y
        # GUI悬停元素
        self.gui_hover_element = self.__gui.gui_hover_element
        # GUI悬停并点击
        self.gui_hover_and_click = self.__gui.gui_hover_and_click

        # 扩展element方法
        self.ele_gui_click = self.__gui.ele_gui_click

    def __reg_net(self):
        self.http_monitor = self.__net.http_monitor
        self.http_monitor_all_tabs = self.__net.http_monitor_all_tabs
        self.ws_monitor = self.__net.ws_monitor
        self.network_ws_event_handler = self.__net.network_ws_event_handler

    def add_element_methods(self, element):
        self.__navigation.extend_element(element)
        self.__action.extend_element(element)
        self.__wait.extend_element(element)
        self.__page_info.extend_element(element)
        self.__gui.extend_element(element)
        self.__dom.extend_element(element)
        return element

    async def _get_x_scroll_offset(self):
        x_scroll_offset = await self.page.evaluate("window.pageXOffset")
        return x_scroll_offset or 0

    async def _get_y_scroll_offset(self):
        y_scroll_offset = await self.page.evaluate("window.pageYOffset")
        return y_scroll_offset or 0

    async def _add_light_pause(self):
        """添加轻微暂停"""
        await asyncio.sleep(0.007)

    def add_handler(self, event, handler):
        """添加事件处理器"""
        self.page.add_handler(event, handler)

    async def verify_cf(self, text="verify you are human", timeout=10):
        """(An attempt)"""
        checkbox = None
        checkbox_sibling = await self.wait_for(text=text, timeout=timeout)
        if checkbox_sibling:
            parent = checkbox_sibling.parent
            while parent:
                checkbox = await parent.query_selector_async("input[type=checkbox]")
                if checkbox:
                    break
                parent = parent.parent
        await checkbox.mouse_move_async()
        await checkbox.mouse_click_async()



class SyncCDP(AsyncCDP):
    """同步CDP方法类 - 包装异步方法"""

    def __init__(self, loop, page, driver):
        self.loop = loop
        self.doing = False
        super(SyncCDP, self).__init__(page, driver)

    def __getattribute__(self, name):
        """动态代理所有方法到异步版本"""
        attr = super().__getattribute__(name)
        if asyncio.iscoroutinefunction(attr):
            # 如果是协程函数，包装为同步调用
            def sync_wrapper(*args, **kwargs):
                return self._run_sync(attr(*args, **kwargs))
            return sync_wrapper
        return attr

    def _run_sync(self, coro):
        """同步执行协程"""
        if not self.doing:
            try:
                self.doing = True
                return self.loop.run_until_complete(coro)
            finally:
                self.doing = False
        return coro
