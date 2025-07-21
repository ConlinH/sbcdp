"""
SBCDP API基础类
提供所有API模块的共同基础功能
"""

from typing import TYPE_CHECKING
import asyncio
from weakref import ref


if TYPE_CHECKING:
    from . import AsyncCDP


class Base:
    """API方法基础类"""
    
    def __init__(self, cdp: "AsyncCDP"):
        self.__cdp = ref(cdp)

    @property
    def cdp(self):
        return self.__cdp()

    async def _add_light_pause(self):
        """添加轻微暂停"""
        await asyncio.sleep(0.007)

    def extend_element(self, element):
        pass
