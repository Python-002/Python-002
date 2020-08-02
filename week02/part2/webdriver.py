# -*- coding: utf-8 -*-

from selenium import webdriver
import time

browser = webdriver.Chrome()

try:
    # 需要安装chrome driver, 和浏览器版本保持一致

    browser.get('https://shimo.im/welcome')

    btm1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    btm1.click()

    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys('15915843748')
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys('hwq15915843748')
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()

    cookies = browser.get_cookies()  # 获取cookies
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:
    browser.close()
