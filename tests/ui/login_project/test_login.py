import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 提取常量（定义后要实际使用！）
TEST_URL = "https://www.saucedemo.com/"
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
USERNAME_ID = "user-name"
PASSWORD_ID = "password"
LOGIN_BUTTON_ID = "login-button"
SHOPPING_CART_CLASS = "shopping_cart_link"  # 把购物车的定位值也抽成常量


@pytest.fixture
def driver():
    driver = webdriver.Edge()  # 用Edge
    driver.implicitly_wait(5)  # 隐式等待：找元素时最多等5秒
    driver.get(TEST_URL)  # ✨ 修改1：用常量替代硬编码的URL
    yield driver
    driver.quit()


def test_success_login(driver):
    # ✨ 修改2：用常量替代硬编码的元素ID和用户名/密码
    # 找到用户名框，输入
    driver.find_element(By.ID, USERNAME_ID).send_keys(VALID_USERNAME)
    # 找到密码框，输入
    driver.find_element(By.ID, PASSWORD_ID).send_keys(VALID_PASSWORD)
    # 点击登录按钮
    driver.find_element(By.ID, LOGIN_BUTTON_ID).click()

    # 等页面跳，转到inventory.html
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url, "登录后未跳转到商品页面"
    # ✨ 修改3：用常量替代硬编码的购物车类名
    assert driver.find_element(By.CLASS_NAME, SHOPPING_CART_CLASS).is_displayed(), "登录后未显示购物车，页面异常"

    print("登录成功啦！")