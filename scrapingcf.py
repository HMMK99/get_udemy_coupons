from bs4 import BeautifulSoup
import requests

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
for h5 in h5s:
    if h5.find('a'):
        sec_page = get_soup(h5.find('a')['href'])
        btns = sec_page.find_all('button')
        for btn in btns:
            if 'Get on Udemy' not in str(btn):
                continue
            print(btn['onclick'].split("'")[1])
