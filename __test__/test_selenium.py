import time
from selenium import webdriver

wd = webdriver.Chrome('D:/ProgramData_Yeon/chromedriver/chromedriver.exe')
wd.get('http://www.google.com')

time.sleep(5)
html = wd.page_source
print(html)

wd.quit()