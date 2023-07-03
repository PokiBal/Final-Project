import time
import pytest
from selenium.webdriver.common.by import By
from tests_logs import BaseClass
from config_test import setup


# @pytest.mark.usefixtures("setup")
class Test_class(BaseClass):
    def test_signup(self,setup):
        global driver
        log = self.log_conf()
        driver = setup
        driver.get("http://18.233.65.192:5000/")
        sign_up = driver.find_element(By.CSS_SELECTOR, ".signup")
        sign_up.click()
        name = 'inbal'
        user_name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Full Name"]').send_keys(name)
        email = driver.find_element(By.CSS_SELECTOR,'input[placeholder="E-Mail"]').send_keys('inbalamr@gmail.com')
        sign_up_button = driver.find_element(By.CSS_SELECTOR,'input[value="Sign-Up"]').click()
        hello_user = driver.find_element(By.CSS_SELECTOR,'.helo').text
        time.sleep(5)
        try:
            assert hello_user == f"Welcome {name}"
        except AssertionError as msg:
            log.error(msg)
            raise AssertionError(msg)
        else:
            log.info("Test Passed successfully")
