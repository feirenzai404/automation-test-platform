# 自动化测试平台

企业级自动化测试平台，集成 Web UI (Selenium) + REST API (Requests) 测试。

## 技术栈
- Python 3.10+
- Pytest 9.0+
- Selenium + webdriver-manager
- Requests
- allure-pytest

## 运行方式
1. 激活虚拟环境
.venv\Scripts\activate
2. 安装依赖
pip install -r requirements.txt
3. 运行测试并生成报告数据
pytest -s --alluredir=allure-results
4. 查看Allure报告（浏览器自动打开）
allure serve allure-results
## Allure报告示例
（100% 通过率，4个用例，执行时间约6秒）

![报告概览]("C:\Users\faker\Desktop\automation-test-platform\reports\index.html")

欢迎 Star & Fork！
