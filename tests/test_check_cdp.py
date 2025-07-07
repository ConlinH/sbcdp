"""
测试cdp检测
"""

import pytest
from sbcdp import AsyncChrome as Chrome


class TestCheckCDP:
    """异步Chrome测试类"""

    @pytest.mark.asyncio
    async def test_cdp(self):
        """测试基本导航功能"""
        async with Chrome() as chrome:
            test_html = r"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>开发者工具【CDP】检测示例</title>
            </head>
            <body>
                <h1>开发者工具【CDP】检测示例</h1>
                <p>检测stack: 	<span id="result-stack">正在检测...</span></p>
                <p>检测时间间隔:	 <span id="result-table">正在检测...</span></p>
                <script>
                document.addEventListener('DOMContentLoaded', () => {
                    const resultElementStack = document.getElementById('result-stack');
                    const resultElementTable = document.getElementById('result-table');
                    function w() {
                        for (var e = function() {
                            for (var e = {}, t = 0; t < 500; t++)
                                e["".concat(t)] = "".concat(t);
                            return e
                        }(), t = [], n = 0; n < 50; n++)
                            t.push(e);
                        return t
                    }
                    const cdp_table = w();
                    console.log(cdp_table);
                
                    function detectConsoleStack() {
                         let devToolsOpened = false;
                         const err = new Error();
                         Object.defineProperty(err, 'stack', {
                             get: function() {
                                 devToolsOpened = true;
                             }
                         });
                
                         console.log(err);
                
                         if (devToolsOpened) {
                             resultElementStack.textContent = '【已打开】';
                             resultElementStack.style.color='red'
                         } else {
                             resultElementStack.textContent = '【未打开】';
                             resultElementStack.style.color='green'
                         }
                    }
                
                    function detectConsoleTable(){
                        let st = (new Date).getTime();
                        console.table(cdp_table);
                        let interval = (new Date).getTime() - st;
                        console.clear()
                        if (interval>1){
                            resultElementTable.textContent = '【已打开】 时间间隔->' + interval;
                            resultElementTable.style.color='red'
                        } else {
                             resultElementTable.textContent = '【未打开】 时间间隔->0';
                             resultElementTable.style.color='green'
                         }
                
                    }
                
                    setInterval(detectConsoleStack, 500);
                    setInterval(detectConsoleTable, 500);
                });
            </script>
            </body>
            </html>
            """
            await chrome.get(f"data:text/html;charset=UTF-8,{test_html}")

            await chrome.sleep(1)
            assert await chrome.get_text('#result-stack') == '【未打开】'
            assert await chrome.get_text('#result-table') == '【未打开】 时间间隔->0'

    async def test_event(self):
        """测试基本导航功能"""
        async with Chrome() as chrome:
            test_html = r"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>检查Event的isTrusted属性</title>
            </head>
            <body>
                <input type="checkbox" >
                <p></p>
            <script>
                i = document.querySelector('input')
                i.addEventListener('click', function(e){
                    document.querySelector('p').innerText = JSON.stringify(e);
                });
            </script>
            </body>
            </html>
            """
            await chrome.get(f"data:text/html;charset=UTF-8,{test_html}")

            await chrome.sleep(1)
            await chrome.mouse_click('input')
            await chrome.sleep(1)
            assert await chrome.get_text('p') == '{"isTrusted":true}'

            await chrome.sleep(1)
            await chrome.click('input')
            await chrome.sleep(1)
            assert await chrome.get_text('p') == '{"isTrusted":false}'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
