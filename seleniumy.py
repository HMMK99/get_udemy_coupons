# from bs4 import BeautifulSoup
# import requests
# import os


# __location__ = os.path.realpath(os.path.join(os.getcwd(),
#                                 os.path.dirname(__file__)))


# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
#             rv:50.0) Gecko/20100101 Firefox/50.0'}
# html_data = requests.get('https://www.udemy.com/abhyasa-summary/?couponCode=UDNWYR2018-SUM-FREE', headers={'User-Agent': 'Google Chrome'})

# print(html_data.url)
# # soup = BeautifulSoup(html_data.text, 'html.parser')
# # with open(os.path.join(__location__, './test.html'), 'w',
# #            encoding="utf-8") as dictfile:
# #     dictfile.write(str(soup))

from selenium import webdriver
from selenium.webdriver.common.by import By
import re


link = 'https://www.udemy.com/course/wastewater-treatment-explained/?couponCode=F1631F827804983CFA8B'


def isFree(link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    # options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(link)
    search_result = re.search('.*left at this price',
                              driver.find_element(By.XPATH,
                                                  '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text)
    if search_result:
        print(search_result.group(0).split('left')[0])
    else:
        print('not found')
    driver.quit()


isFree(link)
