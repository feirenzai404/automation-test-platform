import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # 可选：用于强制等待

@pytest.fixture(scope="session")
def app_driver():
    """Appium 驱动 fixture"""
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = 'emulator-5554'
    options.app = r'C:\Users\faker\Desktop\automation-test-platform\apps\F-Droid.apk'
    options.app_package = 'org.fdroid.fdroid'
    options.app_activity = '.views.main.MainActivity'
    options.no_reset = True
    options.unicode_keyboard = True
    options.reset_keyboard = True

    driver = webdriver.Remote(
        command_executor='http://localhost:4723/wd/hub',
        options=options
    )
    yield driver
    driver.quit()

def test_open_fdroid(app_driver):
    """测试打开 F-Droid App 并验证首页加载成功"""
    wait = WebDriverWait(app_driver, 60)  # 延长到60秒

    try:
        # 用 XPath 验证标题 "F-Droid"（根据你的 Inspector 替换）
        home_title = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[@text='F-Droid']"))
        )
        assert home_title.is_displayed(), "首页标题 'F-Droid' 未显示"
        print("F-Droid App 启动成功，标题可见:", home_title.text)
    except Exception as e:
        print(f"首页验证失败: {e}")
        allure.attach(app_driver.get_screenshot_as_png(), name="首页加载失败截图", attachment_type=allure.attachment_type.PNG)
        raise

def test_search_app(app_driver):
    """测试在 F-Droid 中搜索 App"""
    wait = WebDriverWait(app_driver, 30)

    try:
        # 定位搜索框（必须用 Inspector 确认真实 ID）
        search_box = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "org.fdroid.fdroid:id/search"))  # ← 这里替换成真实 ID
        )
        search_box.click()
        search_box.send_keys("Tomato")  # 搜索一个存在的 App

        # 等待搜索结果出现（用 XPath 匹配结果文字）
        result_item = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Tomato')]"))
        )
        assert result_item.is_displayed(), "搜索 'Tomato' 结果未显示"
        print("搜索 'Tomato' 成功，结果可见")
    except Exception as e:
        print(f"搜索失败: {e}")
        allure.attach(app_driver.get_screenshot_as_png(), name="搜索失败截图", attachment_type=allure.attachment_type.PNG)
        raise