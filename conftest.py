import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture(scope="session")
def browser():
    """全局浏览器fixture"""
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Allure报告钩子"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # 如果是UI测试且失败了，截图
        if 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except:
                pass
        
        # 附加错误日志
        if call.excinfo:
            allure.attach(
                str(call.excinfo.value),
                name="失败日志",
                attachment_type=allure.attachment_type.TEXT
            )

@pytest.fixture(autouse=True)
def log_test_name(request):
    """自动记录测试名称"""
    print(f"\n{'='*60}")
    print(f"开始测试: {request.node.name}")
    print(f"{'='*60}")
    yield
    print(f"\n结束测试: {request.node.name}")