from bs4 import BeautifulSoup as bs
import requests
import datetime
import csv

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
url1 = requests.get('https://elite.finviz.com/screener.ashx?v=152&f=cap_smallunder,sh_price_u20,ta_perf_dup&ft=4&o=-change&c=1,4,6,25,60,61,64,65')
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
        price = float(info[7].text)
        change = float(info[4].text.strip('%'))/100
        openPrice = round(price*(1-change),2)
        priceStr = '$' + info[7].text
        openPriceStr = '$' + "%f" % openPrice
        ticker = info[0].text
        industry = info[1].text
        marketCap = info[2].text
        sharesFloat = info[3].text
        gap = info[5].text
        relativeVolume = info[6].text
        headline = news.a.text
        newsLink = news.a['href']
        with open('dataTest.csv', mode='a') as data:
            writer = csv.writer(data)
            writer.writerow([ticker,industry,openPriceStr,marketCap,sharesFloat,gap,priceStr,relativeVolume,headline,newsLink])