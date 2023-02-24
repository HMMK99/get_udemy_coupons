from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64;\
            rv:50.0) Gecko/20100101 Firefox/50.0'}
html_data = requests.get('https://yofreesamples.com/courses/free-discounted-udemy-courses-list/',
                         headers=headers)
soup = BeautifulSoup(html_data.text, 'html.parser')

h4s = soup.find_all('h4')
print(len(h4s))
for h4 in h4s:
    if h4.find('a'):
        print(h4.find('a')['href'])
