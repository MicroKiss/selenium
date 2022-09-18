from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time
import credentials as CREDENTIALS
import os


#for some reason pyautogui.write doesn't write these characters so we throw them out
def RemoveProblematicFromFileName (path):
    path = path.replace('<','')
    path = path.replace('>','')
    path = path.replace('"','')
    path = path.replace('|','')
    path = path.replace('?','')
    path = path.replace('*','')
    path = path.replace("'",'')
    path = path.replace('`','')
    path = path.replace('˛','')
    path = path.replace('’','')
    path = path.replace(':','')
    path = path.replace('/','')
    path = path.replace('\\','')
    path = path.replace('&','')
    path = path.replace('“','')
    path = path.replace('”','')
    path = path.replace('#','')
    return path


#only works for chrome
def WaitForDownload (downloadFolder, driver):
    maxSeconds = 200
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < maxSeconds:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(downloadFolder):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
        if (seconds % 20 == 0):
            driver.refresh ()
    if (dl_wait == True):
        print ("It took more than"+ str (maxSeconds/60) + "minutes")
        raise Exception('too long')
    return True


try:
    options = webdriver.ChromeOptions ()
    options.add_extension ('./Allow-Right-Click.crx')
    driver = webdriver.Chrome (options=options) 
    driver.get (CREDENTIALS.loginPage)
    driver.switch_to.window (window_name=driver.window_handles[0])
    driver.close ()
    driver.switch_to.window (window_name=driver.window_handles[0])
    usernameField = driver.find_element (By.ID, "user_login")
    usernameField.send_keys (CREDENTIALS.username)
    passwordField = driver.find_element (By.ID, "user_pass")
    passwordField.send_keys (CREDENTIALS.password)
    buttonLogin = driver.find_element (By.ID, "wp-login-submit")
    buttonLogin.click ()
    driver.implicitly_wait (1)

    days = set ()
    recordingStructs = []
    for recondinsPage in CREDENTIALS.recordingsPages:
        driver.get (recondinsPage)
        driver.implicitly_wait (5)
        recordingsByDay = (driver.find_elements (By.XPATH, "//a[@title='View Recording']"))
        day = recondinsPage.split("/")[-2]

        for recording in recordingsByDay:
            containerDiv = recording.find_element (By.XPATH, "./../..")
            child = containerDiv.find_element (By.CSS_SELECTOR, "div:first-child")
            title = child.find_element (By.CSS_SELECTOR, "p:first-child").text
            secondaryTitle = containerDiv.find_element(By.CSS_SELECTOR, "div:nth-child(2)").text
            if (secondaryTitle != ""):
                title = title + " - " +  secondaryTitle
            title  = RemoveProblematicFromFileName (title)
            link = recording.get_attribute ('href')
            days.add (day)
            recordingStructs.append ({"title" : title, "link": link, "day": day})

    mainFolder = CREDENTIALS.mainFolder
    recordingsFolder = os.path.join (mainFolder, "Recordings")
    for day in days:
        if not os.path.isdir (mainFolder):
            print("[+] Making " + mainFolder + "folder")
            os.mkdir(mainFolder)
        if not os.path.isdir (recordingsFolder):
            print("[+] Making Recordings folder")
            os.mkdir(recordingsFolder)
        folder = os.path.join (recordingsFolder, day)
        if not os.path.isdir (folder):
            print("[+] Making " + folder + " folder")
            os.mkdir(folder)
        else:
            for fname in os.listdir(folder):
                if fname.endswith('.crdownload'):
                    os.remove(os.path.join (folder,fname))
                    print("[-] Removed " + os.path.join (folder,fname))
  
    for recordingStruct in recordingStructs:
        savePath = os.path.join (recordingsFolder, recordingStruct["day"], recordingStruct["title"] + ".mp4")
        if (not os.path.exists (savePath)):
            print("[+] Trying to download "+ recordingStruct["title"] + " video")
            driver.get (recordingStruct ["link"])
            time.sleep (5)
            pyautogui.moveTo (300, 300, duration=1)
            pyautogui.rightClick ()
            time.sleep (5)
            pyautogui.moveTo (330,400, duration=1)
            pyautogui.leftClick ()
            time.sleep (10)
            pyautogui.write (savePath)
            time.sleep (2)
            pyautogui.press ("Enter")
            success = WaitForDownload (os.path.join (recordingsFolder, recordingStruct["day"]), driver)
            print ("Success" if success else "Failed")
    driver.quit ()
except:
    print ("there wan an internet error...")
print("############# IT IS DONE #############")
