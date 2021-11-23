from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import credentials as CREDENTIALS

options = Options()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)
driver.get(CREDENTIALS.loginPage)
usernameField = driver.find_element(By.NAME, "username")
usernameField.send_keys(CREDENTIALS.username)
passwordField = driver.find_element(By.NAME, "password")
passwordField.send_keys(CREDENTIALS.password)
buttonLogin = driver.find_element(By.CLASS_NAME, "btn")
buttonLogin.click()

appointments = []
found = False

teacherOccurrences = driver.find_elements(By.XPATH, "//*[text()='"+ CREDENTIALS.teacherName + "']")
for teacherOccurrence in teacherOccurrences:
    upperTable = teacherOccurrence.find_element(By.XPATH, "./..")
    headline = upperTable.find_element(By.CSS_SELECTOR, "div:first-child")
    fullInfo = headline.find_element(By.TAG_NAME, "h5")
    if (fullInfo.text != "Betelt"):
        found = True
        category = upperTable.find_element(By.CSS_SELECTOR, "div:nth-child(1)").text
        time = upperTable.find_element(By.CSS_SELECTOR, "div:nth-child(2)").text
        date = upperTable.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text
        quantity = upperTable.find_element(By.XPATH, "following-sibling::*[1]")
        quantity = quantity.find_element(By.XPATH, "following-sibling::*[1]")
        quantity = quantity.find_element(By.CSS_SELECTOR, "div:first-child")
        quantity = quantity.find_element(By.CSS_SELECTOR, "div:first-child").text
        appointments.append ({"category" : category, "date": date, "quantity": quantity, "time" : time})
driver.quit()

if (found):
    print(CREDENTIALS.teacherName + " óráin ekkor vannak szabad helyek:")
    for appointment in appointments:
        print(appointment ["category"] + ": " + appointment["quantity"] + " szabad időpont " + appointment["date"] + " " + appointment["time"])
else:
    print ("Nincs szabad időpont " + CREDENTIALS.teacherName + "hoz/hez :(")