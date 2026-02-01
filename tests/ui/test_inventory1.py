import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service


@pytest.fixture
def driver():
    """初始化浏览器驱动"""
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")

    # 登录
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # 等待登录成功
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )

    yield driver
    driver.quit()


def test_add_to_cart(driver):
    """测试添加商品到购物车"""
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert "1" in cart_badge.text, "购物车数量应为1"
    print("✅ 测试通过：成功添加商品到购物车")


def test_remove_from_cart(driver):
    """测试从购物车移除商品"""
    # 先添加商品
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)

    # 移除商品
    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()

    # 验证购物车徽章消失
    try:
        driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert False, "购物车徽章应该不存在"
    except NoSuchElementException:
        print("✅ 测试通过：成功从购物车移除商品")


@pytest.mark.parametrize("item_id", [
    "sauce-labs-backpack",
    "sauce-labs-bike-light",
    "sauce-labs-bolt-t-shirt",
    "sauce-labs-fleece-jacket",
    "sauce-labs-onesie",
    "test.allthethings()-t-shirt-(red)"
])
def test_add_multiple_items(driver, item_id):
    """参数化测试添加多个商品"""
    driver.find_element(By.ID, f"add-to-cart-{item_id}").click()
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    cart_count = int(cart_badge.text)
    assert cart_count > 0, f"购物车应有商品，但实际为{cart_count}"

    # 重置购物车以便下一个测试
    driver.find_element(By.ID, f"remove-{item_id}").click()


def test_view_product_details(driver):
    """测试查看商品详情"""
    # 点击商品标题
    driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
    time.sleep(2)

    # 验证跳转到详情页
    assert "inventory-item.html" in driver.current_url, "应该在商品详情页"
    assert driver.find_element(By.CLASS_NAME, "inventory_details_img"), "应该有商品图片"
    print("✅ 测试通过：成功查看商品详情")

    # 返回列表页
    driver.find_element(By.ID, "back-to-products").click()


def test_checkout_process(driver):
    """测试完整结账流程"""
    # 1. 添加商品
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    # 2. 进入购物车
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert "cart.html" in driver.current_url, "应该在购物车页面"

    # 3. 点击结账
    driver.find_element(By.ID, "checkout").click()
    assert "checkout-step-one.html" in driver.current_url, "应该在结账第一步"

    # 4. 填写信息
    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    # 5. 确认订单
    assert "checkout-step-two.html" in driver.current_url, "应该在结账第二步"

    # 6. 完成订单
    driver.find_element(By.ID, "finish").click()

    # 7. 验证订单完成
    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "THANK YOU FOR YOUR ORDER" in success_message, "订单应该完成成功"
    print("✅ 测试通过：完整结账流程成功")


def test_filter_products(driver):
    """测试商品筛选功能"""
    # 按名称A-Z排序
    driver.find_element(By.CLASS_NAME, "product_sort_container").click()
    driver.find_element(By.XPATH, "//option[@value='az']").click()

    # 获取第一个商品名称
    first_item = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert first_item.startswith("Sauce Labs Backpack"), f"第一个商品应为'Sauce Labs Backpack', 实际是'{first_item}'"

    # 按价格从低到高
    driver.find_element(By.CLASS_NAME, "product_sort_container").click()
    driver.find_element(By.XPATH, "//option[@value='lohi']").click()
    print("✅ 测试通过：商品筛选功能正常")


def test_logout(driver):
    """测试登出功能"""
    # 打开菜单
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)

    # 点击登出
    driver.find_element(By.ID, "logout_sidebar_link").click()

    # 验证返回登录页
    assert "www.saucedemo.com" in driver.current_url, "应该返回登录页"
    assert driver.find_element(By.ID, "login-button"), "应该有登录按钮"
    print("✅ 测试通过：成功登出系统")


# 负向测试
def test_add_invalid_item(driver):
    """测试添加不存在的商品（负向）"""
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.ID, "add-to-cart-invalid").click()
    print("✅ 测试通过：无效商品无法添加")


def test_checkout_without_info(driver):
    """测试不填写信息直接结账（负向）"""
    # 添加商品并进入结账
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    # 直接点击继续（不填写信息）
    driver.find_element(By.ID, "continue").click()

    # 验证错误提示
    error_element = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert "Error" in error_element.text, "应该有错误提示"
    print("✅ 测试通过：不填写信息结账应有错误提示")


# 数据驱动测试 - 多用户登录
@pytest.mark.parametrize("username, password, expected_result", [
    ("standard_user", "secret_sauce", "success"),
    ("locked_out_user", "secret_sauce", "locked_out"),
    ("problem_user", "secret_sauce", "success"),
    ("performance_glitch_user", "secret_sauce", "success"),
    ("invalid_user", "secret_sauce", "failure"),
    ("standard_user", "wrong_pass", "failure")
])
def test_multiple_user_login(driver, username, password, expected_result):
    """测试多用户登录场景"""
    # 先登出
    try:
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        driver.find_element(By.ID, "logout_sidebar_link").click()
    except:
        pass

    # 重新登录
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    if expected_result == "success":
        assert "inventory.html" in driver.current_url, f"用户{username}应该登录成功"
    elif expected_result == "locked_out":
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "locked out" in error.lower(), f"用户{username}应该被锁定"
    else:
        error = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "do not match" in error.lower(), f"用户{username}应该登录失败"


def test_shopping_cart_persistence(driver):
    """测试购物车持久性（添加商品后刷新页面）"""
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.refresh()

    # 验证购物车商品仍在
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert "1" in cart_badge.text, "刷新后购物车商品应该还在"
    print("✅ 测试通过：购物车商品刷新后仍在")


def test_inventory_item_count(driver):
    """测试库存商品数量"""
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(items) == 6, f"应该有6个商品，实际有{len(items)}个"
    print(f"✅ 测试通过：库存商品数量正确 - {len(items)}个")


def test_product_images_loaded(driver):
    """测试商品图片是否加载"""
    images = driver.find_elements(By.CLASS_NAME, "inventory_item_img")
    for img in images:
        src = img.get_attribute("src")
        assert src is not None and "jpg" in src.lower(), "商品图片应该正确加载"
    print(f"✅ 测试通过：所有{len(images)}个商品图片已加载")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])