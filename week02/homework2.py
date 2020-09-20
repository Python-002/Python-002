#使用Selenium模拟登录石墨文档 https://shimo.im

from selenium import webdriver
import time


try:
    browser = webdriver.Chrome()

    browser.get('https://shimo.im')
    time.sleep(2)

    btm1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]')
    btm1.click()
    time.sleep(5)

    #点击之后，网页跳转至登录页面，即https://shimo.im/login?from=home
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input').send_keys('17318681615')
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input').send_keys('249219511')
    #密码输入错误，所以登录不成功
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()

    cookies = browser.get_cookies() # 获取cookies
    print(cookies)

except Exception as e:
    print(e)
finally:
    browser.close()
