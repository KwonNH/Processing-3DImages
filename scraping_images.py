from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(15)

driver.get('https://www.google.com/search?q=3d+model+with+support+structure&tbm=isch&ictx=1&tbs=rimg:CZiV-IQeLpHSIgiYlfiEHi6R0ioSCZiV-IQeLpHSEVJC1lDYO5s4&hl=ko&sa=X&ved=2ahUKEwiA85XqnIrsAhUBVawKHRg5CcEQiRx6BAgAEAQ&biw=1366&bih=1024')

result = []

for i in range(0, 10):
    thumbnail_image = driver.find_elements_by_class_name("wXeWr")[i]
    thumbnail_image.click()
    image = driver.find_element_by_css_selector(".OUZ5W .n3VNCb").get_attribute("src")
    print("----------------------------")
    result.append(image)

    result_df = pd.DataFrame(result, columns=['img_url'])

    result_df.to_csv("./result.csv")

    time.sleep(8)

driver.quit()
driver.close()

