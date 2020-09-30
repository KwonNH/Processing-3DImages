from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
import time
import pandas as pd
import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError
import re


def get_image_urls():
    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(30)

    driver.get('https://www.google.com/search?q=3d+model+with+support+structure&tbm=isch&ictx=1&tbs=rimg:CZiV-IQeLpHSIgiYlfiEHi6R0ioSCZiV-IQeLpHSEVJC1lDYO5s4&hl=ko&sa=X&ved=2ahUKEwiA85XqnIrsAhUBVawKHRg5CcEQiRx6BAgAEAQ&biw=1366&bih=1024')

    result = []

    time.sleep(15)

    for i in range(100, 200):
        try:
            thumbnail_image = driver.find_elements_by_class_name("rg_i")[i]
            thumbnail_image.click()
            image = driver.find_elements_by_css_selector(".n3VNCb")

            time.sleep(10)
            result.clear()

            for k in image:
                src = k.get_attribute("src")
                # avoid scraping thumbnail images below the target image
                if "http" in src:
                    if "jpg" in src or "jpeg" in src or "png" in src:
                        result.append([str(i), src])
                        print(result)
            print("----")

            try:
                result_df = pd.DataFrame(result, columns=['index', 'img_url'])
                result_df.to_csv("./result.csv", mode='a', header=False, index=False)
            except IndexError:
                pass

            time.sleep(5)

        except ElementNotVisibleException:
            pass

    driver.quit()
    driver.close()


def download_images_from_urls():

    urls = pd.read_csv("./result.csv")

    for i in range(0, len(urls)):
        print(urls.iloc[i])

        try:
            response = requests.get(urls.iloc[i][1])

            file = open("./image_with_supports/" + str(urls.iloc[i][0]) + ".jpg", "wb")
            file.write(response.content)
            file.close()
        except SSLError:
            pass
        except MaxRetryError:
            pass


def get_image_title():

    urls = pd.read_csv("./result.csv")

    title = []

    for i in range(0, len(urls)):

        url_parts = re.split("/|\?", urls.iloc[i][1])

        for part in url_parts:
            if "jpg" in part:
                title.append(part.split(".jpg")[0])
                break
            elif "jpeg" in part:
                title.append(part.split(".jpeg")[0])
                break
            elif "png" in part:
                title.append(part.split(".png")[0])
                break

    urls['title'] = title

    urls.to_csv("./result_title_added.csv", index=False)


if __name__ == "__main__":
    get_image_title()
