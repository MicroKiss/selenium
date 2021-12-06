from os import error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import credentials as CREDENTIALS

def SetupDriver():
    options = Options()
    #options.add_argument('headless')
    #options.add_argument('disable-gpu')
    #options.add_argument('log-level=3')
    return webdriver.Chrome(options=options)
    

def Login(driver):
    driver.get(CREDENTIALS.loginPage)
    usernameField = driver.find_element(By.NAME, "__authentication[Neos][Flow][Security][Authentication][Token][UsernamePassword][username]")
    usernameField.send_keys(CREDENTIALS.username)
    passwordField = driver.find_element(By.NAME, "__authentication[Neos][Flow][Security][Authentication][Token][UsernamePassword][password]")
    passwordField.send_keys(CREDENTIALS.password)
    form = driver.find_element(By.TAG_NAME, "form")
    buttonLogin = form.find_element(By.CSS_SELECTOR, "div:nth-child(6)")
    buttonLogin = buttonLogin.find_element(By.CSS_SELECTOR, "div:nth-child(1)")
    buttonLogin = buttonLogin.find_element(By.CSS_SELECTOR, "input:nth-child(1)")
    buttonLogin.click()

def LikeImages(driver):
    modal = driver.find_element_by_class_name('modal')
    collection = modal.find_element_by_class_name('neos-contentcollection')
    rowsOfImages = collection.find_elements(By.XPATH, "./*") # all the children

    row = 0
    for rowOfImages in rowsOfImages:
        if (row == 0):
            row = row + 1
            continue
        try:
            likeBoxes = rowOfImages.find_elements_by_class_name('like-box')
            for likeBox in likeBoxes:
                try:
                    likeBox = likeBox.find_element_by_class_name('like-count--liked')
                except NoSuchElementException:
                    likeBox.click()
        except NoSuchElementException:
            pass

def Main ():
    driver = SetupDriver ()
    Login (driver)
    LikeImages (driver)
    driver.quit()



Main()

    

