import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from itertools import count
import random
import time
from bs4 import BeautifulSoup

def Publication(url):
    res = {}
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    title = html_soup.find_all(class_= "title")
    conference = html_soup.find('header',{'class':'headline'}).find('h1').text
    Publications = []
    for x in range(len(title)):
        Publication = title[x].text
        Publications.append(Publication)
    Publicationdata= pd.DataFrame ( { 'Title Of Papers' : Publications })
    Publicationdata.update('"' + Publicationdata[['Title Of Papers']].astype(str) + '"')
    print(Publicationdata)
    res['title']=conference
    res['data']=Publicationdata
    return res


ip = ''
proxies = []
def removeip(ip):
    global proxies
    proxies.pop()
    print(str(len(proxies)) + "Proxies Remaining")

def getip():
    global ip , proxies
    i = len(proxies)-1
    if i > 0:
        ip = proxies[i]
        removeip(proxies[i])
        print("ip=" + ip )
        return True
    else:
        return False


def get_proxies():
    url = 'https://free-proxy-list.net/'
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    body=html_soup.find("table").find("tbody").find_all("tr")
    proxies = []
    for i in range(0,len(body)):
        c=body[i].findAll('td')[0].text+":"+body[i].findAll('td')[1].text
        proxies.append(c)
    return proxies

def init():
    global proxies
    proxies = get_proxies()
    print(str(len(proxies)) + "Proxies")
    getip()
init()

def iplen():
    global proxies
    return (len(proxies))

print(iplen())

Titles =[]
Citaions = []
Authors = []
Conference = []
def extract(response,dblp):
    print('inside extract')
    global Titles,Citatons,Authors,Conference
    soup = BeautifulSoup(response, 'html.parser')
    stop = soup.find('span',{'class':'gs_red'})
    check = soup.find('div',{'id':'gs_bdy_sb_in'}).find('ul').text
    if check is None:
        p = getip()
        print("newip")
        return p
    if stop:
        print("Paper not found")
        return True
    else:
        print('inside else')
        main = soup.find('div',{'class':'gs_ri'})
        if main:
            title = main.find('h3',{'class':'gs_rt'}).text
            print(title)
            Titles.append(title)
            citaion = main.find('div',{'class':'gs_fl'}).findAll('a')[2].text
            print(citaion)
            Citaions.append(citaion)
            author = main.find('div',{'class':'gs_a'}).text.split('-')[0]
            print(author)
            Authors.append(author)
            Conference.append(dblp)
            print("Finish")
            return True

linksnew = ['https://dblp.uni-trier.de/db/conf/asiacrypt/asiacrypt2014.html']

def scholar(number,title):
    global ip
    print(title)
    r = True
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C47&q='+number
    print('inside scholar')
    c_succes = False
    while not c_succes:
        print("Request " + ip)
        try:
            print()
            response = requests.get(url,proxies={"http": ip, "https": ip}, timeout=20)
            print("connected")
            r = extract(response.text, title)
            c_succes = True
            break
        except:
            print("Skipping. Connnection error")
            r = getip()
            if r is False:
                break
    return r
for p in linksnew:
    print(p)
    Publicationdata = Publication(p)
    for Pub in Publicationdata['data']['Title Of Papers'][1:len(Publicationdata['data']['Title Of Papers'])]:
        q = scholar(Pub,Publicationdata['title'])
        if q is False:
            init()
            q = scholar(Pub,Publicationdata['title'])
        if iplen() < 1:
            print("Out of IP at " + str(Pub))
            init()
            break
df = pd.DataFrame({'Title': Titles,'Citaions': Citaions,'Authors': Authors,'Conference': Conference})
test_df.to_csv('Scholardata.csv')
