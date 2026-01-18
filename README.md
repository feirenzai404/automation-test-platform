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
100% 通过率，4个用例，执行时间约6秒

![报告概览](reports/overview.png)

![用例列表](reports/suites.png)

完整静态报告：运行 `allure generate allure-results -o reports --clean` 生成后，用本地服务器查看（cd reports && python -m http.server 8000）
## Postman + Newman 接口自动化报告示例

使用Newman命令行自动化执行Postman集合，生成HTML报告。

总体统计：15个断言，平均响应时间223ms，通过率约60%（负向用例用于验证API边界行为）。

![Newman报告概览](NewmanReport.png)

![失败详情]()

完整报告文件：reports/report.html（双击打开查看每个请求详情、通过/失败、响应时间）。

命令行运行方式：
```bash
newman run "api_collection.json" -r html --reporter-html-export report.html。

欢迎 Star & Fork！
