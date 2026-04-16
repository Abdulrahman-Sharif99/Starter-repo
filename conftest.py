from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def pytest_setup_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    return options