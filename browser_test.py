from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("./chromedriver")


def test_knows_about_title():
    assert (
        driver.getTitle("https://unofficialsurvey-nine.vercel.app")
        == "Unofficial Imperial Survey"
    )
