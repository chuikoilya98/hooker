import requests
from bs4 import BeautifulSoup
import json
from config.config import parseUrl,parseHeaders , parseMainUrl
from db.configuredb import DataBase

class Parser :

    def getAllCities(self) -> list :
        citiesUrls = []
        url = 'https://where2smoke.net/ru'
        htmlCode = requests.get(url, headers=parseHeaders)
        soup = BeautifulSoup(htmlCode.text, 'lxml')

        links = soup.find_all('a',class_= 'd-flex align-items-center')

        for a in links :
            link = url + '/' + a['href']
            citiesUrls.append(link)

        return citiesUrls

    def getInfoByPage(self, placeUrl:str) -> list :

        #placeInfo = {} potom esli nujni budut telefoni
        pageInfo = []

        htmlCode = requests.get(placeUrl, headers=parseHeaders)
        soup = BeautifulSoup(htmlCode.text, 'lxml')

        links = soup.find_all('div', class_='soc-icon')

        for div in links :
            link = div.find('a', class_='js-sendStat' , href=True)
            pageInfo.append(link['href'])

        #if len(pageInfo) >= 0 and pageInfo[0] == pageInfo[1]:
         #   pageInfo.pop()

        return pageInfo

    def getSocLinks(self) :
        
        cities = self.getAllCities()

        for city in cities :
            htmlCode = requests.get(city, headers=parseHeaders)
            soup = BeautifulSoup(htmlCode.text, 'lxml')

            elements = soup.find_all('div', class_='logo')

            count = 0

            for div in elements :
                a = div.find('a', href=True)
                if a['href'][0] != '/' :
                    continue
                else:
                    link = parseMainUrl + a['href']
                    pageInfo = self.getInfoByPage(link) 
                    print(pageInfo)
                    DataBase.updatePlace(pageInfo)
                    count += 1

if __name__ == '__main__' :
    parsing = Parser()
    parsing.getSocLinks()

    print('ready')