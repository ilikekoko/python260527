# web01.py
import urllib.request
from bs4 import BeautifulSoup

data = urllib.request.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=fri')
soup = BeautifulSoup(data, 'html.parser')

cartoons = soup.find_all('td', class_='title')

title = cartoons[0].find('a').text
link = cartoons[0].find('a')['href']
#print(title)
#print(link)

for item in cartoons:
    title = item.find('a').text
    print(title)