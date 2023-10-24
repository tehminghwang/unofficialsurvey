from selenium import webdriver


driver = webdriver.Chrome("./chromedriver")


def test_knows_about_title():
    assert (
        driver.getTitle("https://unofficialsurvey-nine.vercel.app")
        == "Unofficial Imperial Survey"
    )
