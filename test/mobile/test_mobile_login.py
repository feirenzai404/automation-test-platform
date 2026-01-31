import pytest
import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    """测试打开 F-Droid App 并验证首页加载成功（用 app_list 验证）"""
    wait = WebDriverWait(app_driver, 60)

    try:
        # 用 app_list ID 验证首页列表容器是否存在
        app_list = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "org.fdroid.fdroid:id/app_list"))
        )
        assert app_list.is_displayed(), "首页 App 列表未显示"
        print("F-Droid App 启动成功，首页 App 列表可见")
    except Exception as e:
        print(f"首页验证失败: {e}")
        allure.attach(app_driver.get_screenshot_as_png(), name="首页加载失败截图", attachment_type=allure.attachment_type.PNG)
        raise

def test_search_app(app_driver):
    """测试点击搜索按钮并验证搜索功能"""
    wait = WebDriverWait(app_driver, 30)

    try:
        # 先点击搜索浮动按钮（fab_search）
        fab_search = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "org.fdroid.fdroid:id/fab_search"))
        )
        fab_search.click()
        time.sleep(2)  # 等待搜索界面弹出或键盘出现（时间可调）

        # 如果点击 fab_search 后直接弹出搜索框，这里可以再定位输入框
        # 但很多版本点击 fab 后直接进入搜索模式，已有输入焦点
        # 如果需要再定位输入框，用 Inspector 确认搜索框 ID 后替换下面一行
        # search_input = wait.until(EC.presence_of_element_located((AppiumBy.ID, "org.fdroid.fdroid:id/search_edit_text")))
        # search_input.send_keys("Tomato")

        # 直接输入关键词（假设点击 fab_search 后焦点在搜索框）
        app_driver.press_keycode(29)  # A 键测试键盘（可选）
        app_driver.press_keycode(46)  # T 键测试键盘（可选）
        # 更好的方式：用 send_keys 到当前焦点元素
        app_driver.find_element(AppiumBy.ID, "org.fdroid.fdroid:id/search").send_keys("Tomato")  # 如果有搜索框 ID

        # 等待搜索结果列表出现（复用 app_list）
        result_list = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "org.fdroid.fdroid:id/app_list"))
        )
        assert result_list.is_displayed(), "搜索结果列表未显示"
        print("点击搜索按钮并搜索 'Tomato' 成功，结果列表可见")
    except Exception as e:
        print(f"搜索失败: {e}")
        allure.attach(app_driver.get_screenshot_as_png(), name="搜索失败截图", attachment_type=allure.attachment_type.PNG)