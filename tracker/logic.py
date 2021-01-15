from .models import Product, Price, Shop, Url
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Parser():
    def update_data(self, product_name, cost, category, shop):
        try:
            product = Product.objects.get(name=product_name)
            try:
                current_price = product.product_prices.filter(
                    shop=shop).latest('date')
                if current_price.get_cost() != cost:
                    Price.objects.create(
                        cost=cost, product_id=product.id, shop_id=shop)
            except Price.DoesNotExist:
                Price.objects.create(
                    cost=cost, product_id=product.id, shop_id=shop)
        except Product.DoesNotExist:
            product = Product.objects.create(
                name=product_name, category_id=category.id)
            Price.objects.create(
                cost=cost, product_id=product.id, shop_id=shop)


class BelyiVeter(Parser):
    def get_data(self):
        driver = webdriver.Remote(
            "http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
        category_urls = Url.objects.filter(shop=4)
        for category_url in category_urls:
            url = category_url.get_url()
            category = category_url.get_category()
            while(url):
                driver.get(url)
                laptops = driver.find_elements_by_xpath(
                    '//div[@class="bx_catalog_item double"]')
                for laptop in laptops:
                    name = laptop.find_element_by_xpath(
                        './/div[@class="bx_catalog_item_title"]/a').get_attribute('title')
                    price = laptop.find_element_by_xpath(
                        './/div[@class="bx_catalog_item_price"]').text
                    price = price.replace(' ', '')
                    price = price.split('₸')
                    if(len(price) > 2):
                        price = int(price[1])
                    else:
                        price = int(price[0])
                    super().update_data(name, price, category, 4)
                nxt = driver.find_elements_by_xpath(
                    '//li[@class="bx-pag-next"]/a')
                if(len(nxt) > 0):
                    url = nxt[0].get_attribute('href')
                else:
                    url = ''
        driver.quit()


class Sulpak(Parser):

    def get_data(self):
        driver = webdriver.Remote(
            "http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
        category_urls = Url.objects.filter(shop=2)
        for category_url in category_urls:
            url = category_url.get_url()
            category = category_url.get_category()
            while url:
                driver.get(url)
                products = driver.find_elements_by_xpath(
                    '//li[@class="tile-container"]')
                for product in products:
                    name = product.get_attribute('data-name')
                    price = int(float(product.get_attribute('data-price')))
                    if 'Нет в наличии' not in product.text and price > 0:
                        super().update_data(name, price, category, 2)

                nxt = driver.find_elements_by_xpath('//a[@class="next"]')
                if len(nxt) > 0:
                    url = nxt[0].get_attribute('href')
                else:
                    url = ''
        driver.quit()


class TechnoDom(Parser):
    def get_data(self):
        category_urls = Url.objects.filter(shop=1)
        for category_url in category_urls:
            url = category_url.get_url()
            category = category_url.get_category()
            driver = webdriver.Remote(
                "http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content)
            products = soup.findAll('li', attrs={'class': 'ProductCard'})
            for product in products:
                name = product.find('h4')
                price = product.find('data')
                cost = 0
                price = price.text
                for i in price:
                    try:
                        if int(i) >= 0 and int(i) <= 9:
                            cost = cost * 10 + int(i)
                    except ValueError:
                        continue
                super().update_data(name.text, cost, category, 1)
            driver.quit()


class Mechta(Parser):
    def get_data(self):
        driver = webdriver.Remote(
            "http://selenium:4444/wd/hub", DesiredCapabilities.CHROME)
        category_urls = Url.objects.filter(shop=3)
        for category_url in category_urls:
            url = category_url.get_url()
            category = category_url.get_category()
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content)
            products = soup.findAll('div', attrs={'class': 'hoverCard'})
            for product in products:
                child = product.find(
                    'div', attrs={'class': 'hoverCard-child bg-white'})
                name = child.find(
                    'div', attrs={'class': 'q-pt-md q-mt-xs q-px-md text-ts3 text-color2 ellipsis'}).text
                price = child.find(
                    'div', attrs={'row items-center q-px-md'}).text.split('\n')[1]
                cost = 0
                for i in price:
                    try:
                        if(int(i) >= 0 and int(i) <= 9):
                            cost = cost * 10 + int(i)
                    except ValueError:
                        continue
                super().update_data(name, cost, category, 3)
        driver.quit()
