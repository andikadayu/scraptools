from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
import json
import time


class getShopee:
    options = webdriver.ChromeOptions()
    f = open("settings/settings.json")
    config = json.load(f)
    driver = uc

    url = ""
    numberMaxPage = 0
    links = []
    interval = config['delay_time']
    alldata = []

    def __init__(self, url):
        self.url = url
        self.links = []
        self.alldata = []
        self.driver = uc.Chrome(
            options=self.options, driver_executable_path=self.config['chromedriver_path'])

    def getMaxPage(self):
        try:
            self.driver.get(self.url)
            time.sleep(self.interval)
            self.driver.execute_script('window.scrollTo(0, 1500);')
            time.sleep(self.interval)
            self.driver.execute_script('window.scrollTo(0, 2500);')
            time.sleep(self.interval)
            soup_a = BeautifulSoup(self.driver.page_source, 'html.parser')
            pages = soup_a.find(
                'span', class_='shopee-mini-page-controller__total')

            for pag in pages:
                self.numberMaxPage = pag

        except TimeoutException:
            return f"==Error Timeout=="

        return self.numberMaxPage

    def getAllUrl(self, number):
        # Limiter
        i = 0
        while(i < int(number)):
            try:
                self.driver.get(
                    self.url + "?page={}&sortBy=pop".format(i))
                time.sleep(self.interval)
                self.driver.execute_script('window.scrollTo(0, 1500);')
                time.sleep(self.interval)
                self.driver.execute_script('window.scrollTo(0, 2500);')
                time.sleep(self.interval)
                soup_a = BeautifulSoup(self.driver.page_source, 'html.parser')
                products = soup_a.find(
                    'div', class_='shop-search-result-view')
                prs = products.find_all('a')
                for link in prs:
                    self.links.append(link.get('href'))

            except TimeoutException:
                print("==Error Timeout==")
                pass

            i += 1
        return self.links

    def getAllData(self, alllink):
        for link in alllink:
            try:

                self.driver.get("https://shopee.co.id/"+link)
                time.sleep(self.interval)
                self.driver.execute_script('window.scrollTo(0, 1500);')
                time.sleep(self.interval)
                self.driver.execute_script('window.scrollTo(0, 2500);')
                time.sleep(self.interval)
                soup_a = BeautifulSoup(self.driver.page_source, 'html.parser')

                # Get name
                name = soup_a.find(
                    'div', class_='VCNVHn')
                name = name.text
                # Get price
                price = soup_a.find(
                    'div', class_='pmmxKx')
                price = price.text

                # get Price Detail
                price = price.replace('Rp', '').replace('.', '')
                # if price contains - symbols
                if '-' in price:
                    price = price.split(' - ')
                    price = price[1]

                # Get stock
                stock = soup_a.find(
                    'div', class_='_3Xk7SJ')
                stock = stock.text

                alldesc = soup_a.find_all('div', class_='_3Xk7SJ')
                desc = ""
                for d in alldesc:
                    # if d.text first string is Stok
                    if d.text[:4] == "Stok":
                        stock = d.text
                        break

                # Get description
                description = soup_a.find(
                    'p', class_='hrQhmh')
                description = description.text

                images = soup_a.find(
                    'div', class_='hGIHhp')
                images = images.find_all('div', class_='agPpyA _8akja2')
                images = [image.get('style') for image in images]

                imageData = []

                for image in images:
                    imageData.append(image.replace('background-image: url("https://cf.shopee.co.id/file/',
                                                   '').replace('"); background-size: contain; background-repeat: no-repeat;', '').replace('_tn', ''))

                data = {
                    'name': name,
                    'price': price.replace('Rp', '').replace('.', ''),
                    'stock': stock.replace('Stok', ''),
                    'description': description,
                    'images': imageData
                }

                self.alldata.append(data)

            except TimeoutException:
                print("==Error Timeout==")
                continue

            except Exception as e:
                print(e)
                continue

        return self.alldata

    def shutDown(self):
        self.driver.quit()
