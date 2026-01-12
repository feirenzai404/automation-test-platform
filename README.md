<img width="1270" height="1355" alt="image" src="https://github.com/user-attachments/assets/7e87e623-e853-4c53-8777-786d05a6c15a" /># 自动化测试平台

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
100% 通过率，4个用例，执行时间约6秒

![报告概览](reports/overview.png)

![用例列表](reports/suites.png)

完整静态报告：运行 `allure generate allure-results -o reports --clean` 生成后，用本地服务器查看（cd reports && python -m http.server 8000）。

欢迎 Star & Fork！
