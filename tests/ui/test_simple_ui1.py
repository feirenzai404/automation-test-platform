import pytest 
import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.edge.service import Service 
from webdriver_manager.microsoft import EdgeChromiumDriverManager 
 
@pytest.fixture 
def driver(): 
    service = Service(EdgeChromiumDriverManager().install()) 
    driver = webdriver.Edge(service=service) 
    driver.maximize_window() 
    yield driver 
    driver.quit() 
 
def test_saucedemo_login(driver): 

    driver.get("https://www.saucedemo.com/") 
    driver.find_element(By.ID, "user-name").send_keys("standard_user") 
    driver.find_element(By.ID, "password").send_keys("secret_sauce") 
    driver.find_element(By.ID, "login-button").click() 
    time.sleep(2) 
    assert "inventory.html" in driver.current_url, ""
    print("? ")
