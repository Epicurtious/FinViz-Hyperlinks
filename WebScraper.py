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
urlBase = 'https://finviz.com/'
url1 = requests.get('https://finviz.com/screener.ashx?v=111&f=cap_small,sh_price_u20,sh_relvol_o3&o=-change')
soup = bs(url1.content, 'lxml')
first = soup.find(class_='table-dark-row-cp')
link = first.td.a.get('href')
#print(link)
url2 = urlBase + link
soup2 = bs(requests.get(url2).content, 'lxml')
news = soup2.find(class_='fullview-news-outer')
date = news.td.text.split()[0]
year = todayDateTime.year - 2000
today = months[todayDateTime.month] + todayDateTime.strftime("-%d-") + "%d" % year
if date == today:
    print(news.a['href'])