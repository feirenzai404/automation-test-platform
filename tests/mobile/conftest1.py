import pytest
import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # 只在 call 阶段（用例执行）失败时截图
    if rep.when == "call" and rep.failed:
        # 获取 app_driver fixture（pytest 会自动注入）
        driver = item.funcargs.get("app_driver")  # 从 item.funcargs 获取 fixture

        if driver is not None:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"截图失败: {e}")
        else:
            print("app_driver fixture 未找到，无法截图")