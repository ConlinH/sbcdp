"""
SBCDP 等待方法模块
处理各种等待和断言操作
"""
import asyncio
from asyncio import iscoroutinefunction
from typing import List, Optional, Literal, Tuple, Any
from base64 import b64decode

from mycdp import network, fetch

from .base import Base
from ..driver.tab import Tab


class NetData:
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
        return f'<NetData {self._request_id} {self.method} {self.url}>'

    @property
    def url(self):
        if self._net_request:
            return self._net_request.request.url
        elif self._fetch_request:
            return self._fetch_request.request.url
        raise Exception("get url failed")

    @property
    def method(self):
        if self._net_request:
            return self._net_request.request.method
        elif self._fetch_request:
            return self._fetch_request.request.method
        raise Exception("get method failed")

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
            await self.__call_cb(self.__monitor_cb)
            return True
        elif isinstance(e, network.LoadingFailed):
            if self.__event_status == 'stop':
                return True
            self.__event_status = 'failed'
            await self.__call_cb(self.__monitor_cb)
            return True
        elif isinstance(e, fetch.RequestPaused):
            self._fetch_request = e
            block_request = await self.__call_cb(self.__intercept_cb)
            if block_request:
                self.__event_status = 'stop'
                await self.tab.send(fetch.fail_request(e.request_id, network.ErrorReason.TIMED_OUT))
            else:
                await self.tab.send(fetch.continue_request(e.request_id))
        return False

    async def __call_cb(self, cb):
        if iscoroutinefunction(cb):
            return await cb(self)
        else:
            if cb:
                return cb(self)


class NetWork(Base):
    """网络请求方法类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__requests: dict[Tuple[str, callable, callable, bool], NetData] = {}
        self.lock = asyncio.Lock()

    async def set_blocked_urls(
            self,
            urls: str | List[str]
    ):
        """通用等待方法"""
        if isinstance(urls, str):
            urls = [urls]
        await self.cdp.page.send(network.enable())
        await self.cdp.page.send(network.set_blocked_ur_ls(urls))

    async def request_monitor(
            self,
            monitor_cb: Optional[callable] = None,
            intercept_cb: Optional[callable] = None,
            delay_response_body: bool = False,
    ):
        def lambda_cb(e, t):
            return self.cdp.net_work_handler_request_event(e, t, monitor_cb, intercept_cb, delay_response_body)
        if intercept_cb:
            await self.cdp.add_handler(fetch.RequestPaused, lambda_cb)
        if monitor_cb:
            await self.cdp.add_handler(network.RequestWillBeSent, lambda_cb)
            await self.cdp.add_handler(network.RequestWillBeSentExtraInfo, lambda_cb)
            await self.cdp.add_handler(network.ResponseReceived, lambda_cb)
            await self.cdp.add_handler(network.ResponseReceivedExtraInfo, lambda_cb)
            await self.cdp.add_handler(network.LoadingFinished, lambda_cb)
            await self.cdp.add_handler(network.LoadingFailed, lambda_cb)

    async def net_work_handler_request_event(
            self,
            event: Any,
            tab: Tab,
            monitor_cb: Optional[callable],
            intercept_cb: Optional[callable],
            delay_response_body
    ):
        request_id = event.request_id
        if isinstance(event, fetch.RequestPaused):
            request_id = event.network_id
        if request_id is None:
            return

        # 根据worker loaderId为空的特征过滤Worker
        if isinstance(event, network.RequestWillBeSent) and not event.loader_id:
            return

        net_data = self.__requests.get((request_id, monitor_cb, intercept_cb, delay_response_body))
        if net_data is None:
            net_data = NetData(request_id, tab, monitor_cb, intercept_cb, delay_response_body)
            self.__requests[(request_id, monitor_cb, intercept_cb, delay_response_body)] = net_data

        if await net_data.handler_event(event):
            self.__requests.pop((request_id, monitor_cb, intercept_cb, delay_response_body), None)
