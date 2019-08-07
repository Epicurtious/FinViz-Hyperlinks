from bs4 import BeautifulSoup as bs
import requests
import datetime

months = {
    1:"Jan",
    2:"Feb",
    3:"Mar",
    4:"Apr",
    5:"May",
    6:"Jun",
    7:"Jul",
    8:"Aug",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dec"
}

todayDateTime = datetime.datetime.today()
year = todayDateTime.year - 2000
today = months[todayDateTime.month] + todayDateTime.strftime("-%d-") + "%d" % year
urlBase = 'https://elite.finviz.com/'
url1 = requests.get('https://elite.finviz.com/screener.ashx?v=152&f=cap_smallunder,sh_price_u20,ta_perf_dup&ft=4&o=-change&c=1,4,6,25,61,64')
soup = bs(url1.content, 'lxml')
table = soup.find(id='screener-content')
rowLink = []
for row in table.findAll(True, {'class':['table-dark-row-cp', 'table-light-row-cp']}):
    link = urlBase + row.td.a['href']
    info = row.findAll('td')
    soup2 = bs(requests.get(link).content, 'lxml')
    news = soup2.find(class_='fullview-news-outer')
    date = news.td.text.split()[0]
    if date == today:
        print(news.a.text)
        print(news.a['href'])
        for text in info:
            print(text.text)
        print