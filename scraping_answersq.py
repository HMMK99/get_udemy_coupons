from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
            rv:50.0) Gecko/20100101 Firefox/50.0'}
html_data = requests.get('https://answersq.com/udemy-paid-courses-for-free-with-certificate/',
                         headers=headers)
soup = BeautifulSoup(html_data.text, 'html.parser')

lis = soup.find_all('li')
print(len(lis))
for li in lis:
    if li.find('a'):
        if 'Enroll for Free' not in str(li.find('a')):
            continue
        print(li.find('a')['href'])
