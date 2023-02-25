from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd


def scrape_answersq():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
                rv:50.0) Gecko/20100101 Firefox/50.0'}
    html_data = requests.get('https://answersq.com/udemy-paid-courses-for-free-with-certificate/',
                             headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')

    lis = soup.find_all('li')
    print(len(lis))
    mylist = []
    for li in lis:
        if li.find('a'):
            if 'Enroll for Free' not in str(li.find('a')):
                continue
            mylist.append(li.find('a')['href'])
    return mylist


def scrape_yofree():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
                rv:50.0) Gecko/20100101 Firefox/50.0'}
    html_data = requests.get('https://yofreesamples.com/courses/free-discounted-udemy-courses-list/',
                            headers=headers)
    soup = BeautifulSoup(html_data.text, 'html.parser')

    h4s = soup.find_all('h4')
    mylist = []
    for h4 in h4s:
        if h4.find('a') and h4.find('a')['href']:
            mylist.append(h4.find('a')['href'])
    return mylist


def scrape_fc():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
            rv:50.0) Gecko/20100101 Firefox/50.0'}

    def get_soup(url):
        html_data = requests.get(url,
                                 headers=headers)
        soup = BeautifulSoup(html_data.text, 'html.parser')

        return soup

    soup = get_soup('https://coursefolder.net/free-udemy-coupon.php')

    h5s = soup.find_all('h5')
    print(len(h5s))
    mylist = []
    for h5 in h5s:
        if h5.find('a') and h5.find('a')['href']:
            sec_page = get_soup(h5.find('a')['href'])
            btns = sec_page.find_all('button')
            for btn in btns:
                if 'Get on Udemy' not in str(btn):
                    continue
                mylist.append(btn['onclick'].split("'")[1])
    return(mylist)


def isFree(links):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    # options = Options()
    options.add_argument('--headless')
    mylist = []

    for link in links:
        driver = webdriver.Chrome(options=options)
        print(link)
        driver.get(link)
        element = driver.find_element(By.XPATH,
                                      '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text
        search_result = re.search('.*left at this price',
                                  element)
        trials = 0
        if search_result and re.search('Free', element):
            name = link.split('/')[-2]
            coupon = link.split('=')[-1]
            url = link
            expiration = search_result.group(0).split('left')[0]
            line = {'name': name, 'coupon': coupon,
                    'url': url, 'expiration': expiration}
            mylist.append(line)
        else:
            while trials < 3:
                driver = webdriver.Chrome(options=options)
                driver.get(link)
                element = driver.find_element(By.XPATH,
                                              '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]').text
                search_result = re.search('.*left at this price',
                                          element)
                if search_result and re.search('Free', element):
                    name = link.split('/')[-2]
                    coupon = link.split('=')[-1]
                    url = link
                    expiration = search_result.group(0).split('left')[0]
                    line = {'name': name, 'coupon': coupon,
                            'url': url, 'expiration': expiration}
                    mylist.append(line)
                else:
                    if trials == 2:
                        print('not found', link)
                        break

                    trials = trials + 1

        driver.quit()
    return mylist


# data = isFree(scrape_yofree())
# print(data)
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('yofreesamples.csv')

# print(len(scrape_fc()))
# data = isFree(scrape_fc())
# pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('coursefolder.csv')

data = isFree(scrape_answersq())
pd.DataFrame(data, columns=['name', 'coupon', 'url', 'expiration']).to_csv('answersq.csv')
