import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from .models import Product

class DataScrapper():
    def __init__(self):
        self.websites = \
        {'cartpk':
                {'url':'https://www.cartpk.com/',
                'suffix':['online-beef-delivery-in-pakistan', 'online-chicken-delivery-in-pakistan', 
                          'buy-mutton-online-delivery-in-karachi-pakistan', 'online-fish-delivery-in-karachi-pakistan']
                },
        'naheed':
                {'url': 'https://www.naheed.pk/groceries-pets/fresh-products/meat-poultry',
                'suffix': []
                },
        'chickenzone':
                {'url':'http://chickzone.pk/product-category/fresh-chicken/',
                'suffix': []                
                },
        'careeb':
                {'url':'https://careeb.com.pk/meat-online/',
                'suffix':['beef-meat-online', 'fresh-chicken-delivery', 'fish', 'mutton', 'veal']
                },
        'meatcart':
                {'url':'http://meatcart.pk/product-category/',
                'suffix':['chicken', 'mutton-meat', 'lumb', 'beef', 'camel', 'fish']},
        'meatone':
                {'url':'http://www.meatone.net/category/',
                'suffix':['mutton', 'chicken', 'beef']
                },
        'zenith':
                {'url':'http://zenithfoods.com.pk/cms/Products/',
                'suffix':['Chicken', 'Mutton', 'Beef', 'Veal']},
        'hummart':
                {'url':'https://hummart.com/meat',
                'suffix': []
                },
        'freshzone':
                {'url':'https://www.freshone.com.pk/',
                'suffix':['freshone-fish','chicken-category', 'prime-beef-category', 'mutton-category', 'prime-beef-steak-category']},
        '_24sevenpk':
                {'url':'https://24seven.pk/default/meats-vegetables-fruits/fresh-meat.html/',
                'suffix':[]
                }        
        }

        self.curr_date = datetime.date(datetime.now())
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',}

    def scrap_data(self):
        print('cartpk')
        self.cartpk()
        print('naheed')
        self.naheed()
        print('chikenzone')
        self.chikenzone()
        print('careeb')
        self.careeb()
        print('meatcart')
        self.meatcart()
        print('meatone')
        self.meatone()
        print('zenith')
        self.zenith()
        print('hummart')
        self.hummart()
        print('freshzone')
        self.freshzone()
        print('_24sevenpk')
        self._24sevenpk()
        count = Product.objects.all().count()
        print('Total Products Added: ',count)

    def delete_data(self):
        Product.objects.all().delete()

    def delete_data_eod(self,date):
        Product.objects.filter(eod_date=date).delete()


    def cartpk(self):
        for i in self.websites['cartpk']['suffix']:
            URL = self.websites['cartpk']['url']+i
            page = requests.get(URL, headers= self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id = "layer-product-list")
            urls = results.find_all('a',{'href': re.compile(r''+self.websites['cartpk']['url']+'.*')})
            images = [image.img['src'] for image in urls if image.img]
            names = [t.text.strip() for t in urls if len(t.text.strip())>0]
            prices = [float(price.text.replace(",","").split(" ")[1]) for price in results.find_all('span', {'class' : 'price'})]

            for j in range(len(names)):
                p = Product(name=names[j],image_url=images[j],price=prices[j],category=i.split('-')[1].lower(),brand='cartpk',eod_date=self.curr_date)
                p.save()

    def careeb(self):
        for i in self.websites['careeb']['suffix']:
            URL = self.websites['careeb']['url']+i
            page = requests.get(URL, headers= self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id = "content")
            urls = results.find_all('a',{'href': re.compile(r''+self.websites['careeb']['url']+'.*')})
            images = [image.img['src'] for image in urls if image.img]
            names = [t.text.strip() for t in urls if len(t.text.strip())>0]
            prices = [price.text.strip() for price in results.find_all('p', {'class' : 'price'})]
            for j in range(len(names)):
                p = Product(name=names[j],image_url=images[j],price=prices[j],category=i.split('-')[1].lower(),brand='careeb',eod_date=self.curr_date)
                print(p)
                p.save()

    def meatcart(self):
        for i in self.websites['meatcart']['suffix']:
            URL = self.websites['meatcart']['url'] +i
            page = requests.get(URL, headers= self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id = "apus-shop-products-wrapper")
            urls = results.find_all('div',{'class':'product-block grid version-style-1'})
            images = [image.img['data-src'] for image in urls if image.img]
            names = [name.a['title'] for name in urls]
            prices = [float(price.text.strip().replace(',','').replace('₨','')) for price in results.find_all('span', {'class' : 'price'})]
            for j in range(len(names)):
                p = Product(name=names[j],image_url=images[j],price=prices[j],category=i.split('-')[0].lower(),brand='meatcart',eod_date=self.curr_date)
                p.save()

    def meatone(self):
        for i in self.websites['meatone']['suffix']:
            URL = self.websites['meatone']['url'] +i
            page = requests.get(URL, headers= self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id = 'ajax_div')
            urls = results.find_all('a',{'href': re.compile(r''+self.websites['meatone']['url']+'.*')})
            images = [image.img['src'] for image in urls if image.img]
            names = [t.text.strip() for t in urls if len(t.text.strip())>0]

            prices = [float(price.text.strip().replace(",","").split()[1]) for price in results.find_all('p')]
            for j in range(len(names)):
                p = Product(name=names[j],image_url=images[j],price=prices[j],category=i.split('-')[1].lower(),brand='meatone',eod_date=self.curr_date)
                p.save()

    def zenith(self):
        for i in self.websites['zenith']['suffix']:
            URL = self.websites['zenith']['url']+i+'.aspx'
            page = requests.get(URL, headers= self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id = "dnn_ContentPane")
            urls = results.find_all('div',{'class': 'prices_table_page'})
            images = [image.img['src'] for image in urls if image.img]
            names = [name.text.strip() for name in results.find_all('h3', {'class' : 'top_price_title'})]
            prices = [float(price.text.replace(",","").split(" ")[1]) for price in results.find_all('p', {'class' : 'top_price_style'})]
            for j in range(len(names)):
                print(p)
                p = Product(name=names[j],image_url=images[j],price=prices[j],category=i.split('-')[0].lower(),brand='zenith',eod_date=self.curr_date)
                p.save()


    def naheed(self):
        URL = self.websites['naheed']['url']
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.findAll("li", {"class": "item product product-item odd product-12239"})
        results_div = soup.findAll("div", {"class": "images-container"})

        for div in results_div:
            x = div.findChildren("div" , recursive=False)
            image = x[0].findChildren("a" , recursive=False)[0].findChildren("img" , recursive=False)[0]['src']
            price = x[1].findChildren("span")[0].text
            price = float(price.replace(",","").strip().split(" ")[1])
            name = x[1].findChildren("h2")[0].text
            if 'chicken' in name.lower():
                category = "chicken"
            elif 'mutton' in name.lower():
                category = "mutton"
            elif 'beef' in name.lower():
                category = "beef"
            else:
                category = "meat"
            p = Product(name=name,image_url=image,price=price,category=category,brand='naheed',eod_date=self.curr_date)
            p.save()



    def chickenzone(self):
        URL = self.websites['chickenzone']['url']
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.findAll("div", {"class": "product"})
        products = []
        for div in results:
            image = div.findChildren("img")[0]["src"]
            name = div.findChildren("h5")[0].text
            price = 0
        price = 0
        if len(div.findChildren("p")) > 0:
            if len(div.findChildren("p")[0].findChildren("ins")) > 0:
                price = div.findChildren("p")[0].findChildren("ins")[0].text
                if '₨' in price:
                    price = price[1:]
            p = Product(name=name,image_url=image,price=price,category='chicken',brand='chikenzone',eod_date=self.curr_date)
            p.save()





    def hummart(self):
        URL = self.websites['hummart']['url']
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.findAll("li", {"class": "item product product-item"})
        products = []
        for div in results:
            image = div.findChildren("img")[0]["src"]
            name = div.findChildren("a", {"class": "product-item-link"})[0].text
            name = re.sub(' +', ' ', name)
            price = float(div.findChildren("span", {"class": "price"})[0].text.replace(',','').split(" ")[1])
            if 'chicken' in name.lower():
                category = "chicken"
            elif 'mutton' in name.lower():
                category = "mutton"
            elif 'beef' in name.lower():
                category = "beef"
            elif 'veal' in name.lower():
                category = "veal"
            elif 'fish' in name.lower():
                category = "fish"
            elif 'duck' in name.lower():
                category = "duck"
            elif 'turkey' in name.lower():
                category = "turkey"
            elif 'fowl' in name.lower():
                category = "fowl"
            else:
                category = "meat"
            p = Product(name=name,image_url=image,price=price,category=category,brand='hummart',eod_date=self.curr_date)
            p.save()


    def freshzone(self):
        for i in self.websites['cartpk']['suffix']:
            URL = self.websites['cartpk']['url']+'?pagesize=9'
            page = requests.get(URL, headers= self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.findAll("div", {"class": "item-grid"})
            urls = soup.findAll("div", {"class": "item-grid"})
            images = [image.img['src'] for image in urls if image.img]
            names = [name.find_all('h2', {'class' : 'product-title'})[0].text.strip() for name in urls]
            prices = [float(price.find_all('span', {'class' : 'price actual-price'})[0].text.replace(",","").split(" ")[0]) for price in urls]
            for j in range(len(names)):
                p = Product(name=names[j],image_url=images[j],price=prices[j],category=i.split('-')[1].lower(),brand='freshzone',eod_date=self.curr_date)
                p.save()

    def _24sevenpk(self):
        URL = self.websites['_24sevenpk']['url']
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.findAll("li", {"class": "item product product-item"})
        products = []
        for div in results:
            image = div.findChildren("img", {"class": "product-image-photo"})[0]["src"]
            price = float(div.findChildren("span", {"class": "price"})[0].text[3:].replace(',',''))
            name = div.findChildren("strong", {"class": "product name product-item-name"})[0].text.strip() 
            if 'chicken' in name.lower():
                category = "chicken"
            elif 'mutton' in name.lower():
                category = "mutton"
            elif 'beef' in name.lower():
                category = "beef"
            elif 'veal' in name.lower():
                category = "veal"
            elif 'fish' in name.lower():
                category = "fish"
            elif 'duck' in name.lower():
                category = "duck"
            elif 'turkey' in name.lower():
                category = "turkey"
            elif 'fowl' in name.lower():
                category = "fowl"
            else:
                category = "meat"
            p = Product(name=name,image_url=image,price=price,category=category,brand='24sevenpk',eod_date=self.curr_date)
            p.save()


