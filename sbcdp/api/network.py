"""
SBCDP 等待方法模块
处理各种等待和断言操作
"""
import asyncio
from asyncio import iscoroutinefunction
from typing import List, Optional, Literal, Tuple, Any, Callable
from base64 import b64decode
import inspect

from loguru import logger
from mycdp import network, fetch

from .base import Base
from ..driver.tab import Tab


async def _call_cb(cb, *args, **kwargs):
    if iscoroutinefunction(cb):
        return await cb(*args, **kwargs)
    else:
        if cb:
            return cb(*args, **kwargs)


class NetHttp:
    def __init__(
            self,
            request_id,
            tab: Tab,
            monitor_cb: Optional[callable],
            intercept_cb: Optional[callable],
            delay_response_body: bool = False
    ):
        self.tab = tab
        self.__monitor_cb = monitor_cb
        self.__intercept_cb = intercept_cb
        self.__delay_response_body = delay_response_body
        self.__event_status: Literal['pending', 'ok', 'failed', 'stop'] = 'pending'

        self._request_id: Optional[network.RequestId] = request_id
        self._net_request: Optional[network.RequestWillBeSent] = None
        self._fetch_request: Optional[fetch.RequestPaused] = None
        self._request_extra_info: Optional[network.RequestWillBeSentExtraInfo] = None
        self._response: Optional[network.ResponseReceived] = None
        self._response_extra_info: Optional[network.ResponseReceivedExtraInfo] = None

    def __repr__(self):
        return f'<NetHttp {self._request_id} {self.method} {self.url}>'

    @property
    def url(self):
        if self._net_request:
            return self._net_request.request.url
        elif self._fetch_request:
            return self._fetch_request.request.url
        # raise Exception("get url failed")

    @property
    def method(self):
        if self._net_request:
            return self._net_request.request.method
        elif self._fetch_request:
            return self._fetch_request.request.method
        # raise Exception("get method failed")

    @property
    def resource_type(self):
        if self._net_request:
            return self._net_request.type_.value
        elif self._fetch_request:
            return self._fetch_request.resource_type.value
        raise Exception("get resource_type failed")

    @property
    def request_headers(self):
        if self._net_request:
            return self._net_request.request.headers
        elif self._fetch_request:
            return self._fetch_request.request.headers
        raise Exception("get request_headers failed")

    @property
    def response_headers(self):
        if self._response:
            return self._response.response.headers

    @property
    def response(self):
        if self._response:
            return self._response.response

    @property
    def request(self):
        if self._net_request:
            return self._net_request.request
        elif self._fetch_request:
            return self._fetch_request.request
        raise Exception("get Request failed")

    @property
    def request_body(self):
        if self._net_request:
            return self._net_request.request.post_data
        elif self._fetch_request:
            return self._fetch_request.request.post_data
        raise Exception("get request_body failed")

    @property
    def response_body(self):
        if not self._response.response:
            return

        body = getattr(self._response.response, 'body', None)
        if body is not None:
            return body

        raise Exception("get response_body failed")

    async def get_response_body(self):
        if not self._response:
            return

        if not self._response.response:
            return

        body = getattr(self._response.response, 'body', None)
        if body is not None:
            return body

        while self.__event_status == 'pending':
            await asyncio.sleep(0.1)

        if self.__event_status == 'ok':
            self._response.response._body, base64Encoded = await self.tab.send(network.get_response_body(self._request_id))
            if base64Encoded:
                self._response.response._body = b64decode(self._response.response._body)
            return self._response.response._body

    async def handler_event(self, e: Any) -> bool:
        if isinstance(e, network.RequestWillBeSent):
            self._net_request = e
        elif isinstance(e, network.RequestWillBeSentExtraInfo):
            self._request_extra_info = e
        elif isinstance(e, network.ResponseReceived):
            self._response = e
        elif isinstance(e, network.ResponseReceivedExtraInfo):
            self._response_extra_info = e
        elif isinstance(e, network.LoadingFinished):
            self.__event_status = 'ok'
            if not self._net_request:
                return True
            if not self.__delay_response_body:
                await self.get_response_body()
            await _call_cb(self.__monitor_cb, self)
            return True
        elif isinstance(e, network.LoadingFailed):
            if self.__event_status == 'stop':
                return True
            self.__event_status = 'failed'
            await _call_cb(self.__monitor_cb, self)
            return True
        elif isinstance(e, fetch.RequestPaused):
            self._fetch_request = e
            block_request = await _call_cb(self.__intercept_cb, self)
            if block_request:
                self.__event_status = 'stop'
                await self.tab.send(fetch.fail_request(e.request_id, network.ErrorReason.TIMED_OUT))
            else:
                await self.tab.send(fetch.continue_request(e.request_id))
        return False


class NetWebsocket:
    def __init__(
            self,
            request_id,
            tab: Tab,
            monitor_cb: Optional[callable],
    ):
        self.tab = tab
        self.__monitor_cb = monitor_cb
        self.__status: Optional[Literal['created', 'closed']] = None
        self._request_id: Optional[network.RequestId] = request_id

        self._url: Optional[str] = None
        self._request: Optional[network.WebSocketRequest] = None
        self._response: Optional[network.WebSocketResponse] = None

    def __repr__(self):
        return f'<NetWebsocket {self._request_id} {self.url}>'

    @property
    def url(self):
        return self._url

    @property
    def handshake_request(self):
        return self._request

    @property
    def handshake_response(self):
        return self._response

    async def handler_event(self, e: Any) -> bool:
        if isinstance(e, network.WebSocketCreated):
            # 在 WebSocket 创建时触发。
            self.__status = 'created'
            self._url = e.url
        elif isinstance(e, network.WebSocketClosed):
            # 当 WebSocket 关闭时触发。
            self.__status = 'closed'
            return True
        elif isinstance(e, network.WebSocketFrameError):
            # 当 WebSocket 消息发生错误时触发。
            logger.warning(f"发送msg失败， msg: {e.error_message}, 时间：{e.timestamp}, ws: {self}")
        elif isinstance(e, network.WebSocketFrameReceived):
            # 收到 WebSocket 消息时触发
            await _call_cb(self.__monitor_cb, e.response.payload_data, 'recv', self)
        elif isinstance(e, network.WebSocketFrameSent):
            # 发送 WebSocket 消息时触发。
            await _call_cb(self.__monitor_cb, e.response.payload_data, 'send', self)
        elif isinstance(e, network.WebSocketWillSendHandshakeRequest):
            # 当 WebSocket 即将发起握手时触发。
            self._request = e.request
        elif isinstance(e, network.WebSocketHandshakeResponseReceived):
            # 当 WebSocket 握手响应可用时触发。
            self._response = e.response
        return False


class NetWork(Base):
    """网络请求方法类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__http_cache: dict[Tuple[str, callable, callable, bool], NetHttp] = {}
        self.__ws_cache: dict[Tuple[str, callable], NetWebsocket] = {}

    async def set_blocked_urls(
            self,
            urls: str | List[str]
    ):
        """
        阻止url加载。
        Blocks URLs from loading.
        """
        if isinstance(urls, str):
            urls = [urls]
        await self.cdp.page.send(network.enable())
        await self.cdp.page.send(network.set_blocked_ur_ls(urls))

    def http_monitor(
            self,
            monitor_cb: Optional[Callable[[NetHttp], None]] = None,
            intercept_cb: Optional[Callable[[NetHttp], Optional[bool]]] = None,
            delay_response_body: bool = False,
    ):
        self.cdp.page.http_monitor(
            monitor_cb=monitor_cb,
            intercept_cb=intercept_cb,
            delay_response_body=delay_response_body
        )

    def http_monitor_all_tabs(
        self,
        monitor_cb: Optional[Callable[[NetHttp], None]] = None,
        intercept_cb: Optional[Callable[[NetHttp], Optional[bool]]] = None,
        delay_response_body: bool = False,
    ):
        self.cdp.page.http_monitor(monitor_cb, intercept_cb, delay_response_body)
        self.cdp.driver.http_monitor_all_tabs(monitor_cb, intercept_cb, delay_response_body)

    def ws_monitor(
            self,
            monitor_cb: Callable[[str, str, NetWebsocket], None]
    ):
        if not callable(monitor_cb):
            raise TypeError("monitor_cb must be a callable function")

        params = inspect.signature(monitor_cb).parameters
        if len(params) != 3:
            raise ValueError(f"expected monitor_cb: def cb(msg, msg_type, ws): pass")

        def lambda_cb(e, t):
            return self.cdp.network_ws_event_handler(e, t, monitor_cb)

        self.cdp.add_handler(network.WebSocketCreated, lambda_cb)
        self.cdp.add_handler(network.WebSocketClosed, lambda_cb)
        self.cdp.add_handler(network.WebSocketFrameError, lambda_cb)
        self.cdp.add_handler(network.WebSocketFrameReceived, lambda_cb)
        self.cdp.add_handler(network.WebSocketFrameSent, lambda_cb)
        self.cdp.add_handler(network.WebSocketHandshakeResponseReceived, lambda_cb)
        self.cdp.add_handler(network.WebSocketWillSendHandshakeRequest, lambda_cb)


    async def network_ws_event_handler(
            self,
            event: Any,
            tab: Tab,
            monitor_cb: Optional[callable],
    ):
        request_id = event.request_id
        if isinstance(event, fetch.RequestPaused):
            request_id = event.network_id
        if request_id is None:
            return

        net_ws = self.__ws_cache.get((request_id, monitor_cb))
        if net_ws is None:
            net_ws = NetWebsocket(request_id, tab, monitor_cb)
            self.__ws_cache[(request_id, monitor_cb)] = net_ws

        if await net_ws.handler_event(event):
            self.__ws_cache.pop((request_id, monitor_cb), None)
