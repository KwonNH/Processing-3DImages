from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(15)

driver.get('https://www.google.com/search?q=3d+model+with+support+structure&tbm=isch&ictx=1&tbs=rimg:CZiV-IQeLpHSIgiYlfiEHi6R0ioSCZiV-IQeLpHSEVJC1lDYO5s4&hl=ko&sa=X&ved=2ahUKEwiA85XqnIrsAhUBVawKHRg5CcEQiRx6BAgAEAQ&biw=1366&bih=1024')

result = []

for i in range(0, 200):
    thumbnail_image = driver.find_elements_by_class_name("rg_i")[i]
    thumbnail_image.click()
    image = driver.find_elements_by_css_selector(".n3VNCb")

    for k in image:
        src = k.get_attribute("src")
        if "https" in src:
            result.clear()
            result.append([str(i), src])
            print(result)
    print("----")

    try:
        result_df = pd.DataFrame(result, columns=['index', 'img_url'])
        result_df.to_csv("./result.csv", mode='a', header=False, index=False)
    except IndexError:
        pass

    time.sleep(15)

driver.quit()
driver.close()

