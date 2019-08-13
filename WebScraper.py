from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import csv
from progress.bar import Bar

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

#returns false if hyperlink is in file
def containsHyperlink(link):
    with open('dataTest.csv') as data:
        read = csv.DictReader(data)
        for row in read:
            if row["Hyperlink"] == link:
                return True
        return False

#returns number of seconds in day today
#for comparing time by integer than by string
def getTodaySecond():
    today = datetime.today()
    midnight = today.replace(hour=0,minute=0,second=0,microsecond=0)
    second = (today - midnight).seconds
    return second

#gets second in time given
#time format: XX:XXPM/XX:XXAM
def getDaySecond(time):
    timeElements = time.split(':')
    if timeElements[1].endswith("AM"):
        hour = int(timeElements[0])
        mins = int(timeElements[1].strip("AM"))
    if timeElements[1].endswith("PM"):
        hour = int(timeElements[0]) + 12
        mins = int(timeElements[1].strip("PM"))
    seconds = hour * 60 * 60 + mins * 60
    return seconds

#returns the fiscal day today
#fiscal day runs between 4pm and 4pm
#hence, 4pm today is fiscal day tomorrow
def getFiscalDay():
    today = datetime.today()
    time = getTodaySecond()
    if time >= (4+12)*60*60:
        year = today.year - 2000
        day = today.day + 1
        fiscalDay = months[today.month] + "-%d-%d" % (day, year)
    else:
        year = today.year - 2000
        fiscalDay = months[today.month] + today.strftime("-%d-") + "%d" % year
    return fiscalDay

#returns true if day and time given are within fiscal day
#4pm yesterday till 4pm today
#day format: AAA-XX-XX
#time format: XX:XXPM/XX:XXAM
def isFiscalDay(day, time):
    today = getFiscalDay()
    todayParts = today.split("-")
    dayParts = day.split("-")
    daySeconds = getDaySecond(time)
    if daySeconds >= (4 + 12) * 60 * 60 and todayParts[0] == dayParts[0]:
        dayInt = int(dayParts[1]) + 1
        newDay = "%s-%d-%s" % (dayParts[0], dayInt, dayParts[2])
        return True if (today == newDay) else False
    else:
        return True if (today == day) else False

print("Type your choice and press enter:")
print("0: Run until stopped")
print("1: Run once")
continuous = input()
run = 0
while run == 0:
    print("Press 'ctrl-C' to stop the program")
    bar = Bar('Scraping',max=20)
    today = getFiscalDay()
    fileName = "CSvs/" + today + ".csv"
    try:
        open(fileName, mode='r')
    except:
        with open(fileName, mode='w') as data:
            writer = csv.writer(data)
            writer.writerow(["Date","Time","Ticker","Industry","Open Price","Market Cap","Shares Float","Gap","Price from Open","Relative Volume","News Headline","Hyperlink"])    
    urlBase = 'https://elite.finviz.com/'
    url1 = requests.get('https://elite.finviz.com/screener.ashx?v=152&f=cap_smallunder,sh_price_u20,sh_relvol_o3,ta_perf_dup&ft=4&o=-changeopen&c=1,4,6,25,60,61,64,65')
    soup = bs(url1.content, 'lxml')
    table = soup.find(id='screener-content')
    print(len(table.findAll(True, {'class':['table-dark-row-cp', 'table-light-row-cp']})))
    for row in table.findAll(True, {'class':['table-dark-row-cp', 'table-light-row-cp']}):
        link = urlBase + row.td.a['href']
        info = row.findAll('td')
        soup2 = bs(requests.get(link).content, 'lxml')
        for news in soup2.find(class_='fullview-news-outer').findAll('tr'):
            dateAndTime = news.td.text.split()
            time = (dateAndTime[0] if len(dateAndTime) == 1 else dateAndTime[1])
            if len(dateAndTime) > 1:
                date = dateAndTime[0]
            if isFiscalDay(date, time) and containsHyperlink(news.a['href']) == False:
                price = float(info[7].text)
                change = float(info[4].text.strip('%'))/100
                openPrice = round(price*(1-change),2)
                priceStr = '$' + info[7].text
                openPriceStr = '$%.2f' % openPrice
                ticker = info[0].text
                industry = info[1].text
                marketCap = info[2].text
                sharesFloat = info[3].text
                gap = info[5].text
                relativeVolume = info[6].text
                headline = news.a.text
                newsLink = news.a['href']
                with open(fileName, mode='a') as data:
                    writer = csv.writer(data)
                    writer.writerow([date,time,ticker,industry,openPriceStr,marketCap,sharesFloat,gap,priceStr,relativeVolume,headline,newsLink])
            elif isFiscalDay(date, time) == False:
                break
        bar.next()
    bar.finish()
    print("Scraping Complete")
    if continuous == 1:
        run += 1