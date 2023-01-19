from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import subprocess

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=options)
pages = ["https://munch.hu/product/la-donuteria-munch/",
        "https://munch.hu/product/pekmuhely-bartok-munch/"
        ]


def OnFound (name):
    print ("Found " + name)
    subprocess.run(["C:\Program Files\VideoLAN\VLC\vlc.exe","C:\\Users\\dinny\\Desktop\\Superklaas - Gop Stop (Electro Mix).mp3"])

while (True):
    print (time.ctime())
    for page in pages:
        munchName = page.split ('/')[-2]
        driver.get(page)
        statusElement = driver.find_element(By.CLASS_NAME,"stock-status")
        print (munchName + ": "+ statusElement.text)
        if ("Elfogyott" not in  statusElement.text):
            OnFound (munchName)
    time.sleep(60)