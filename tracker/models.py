from django.db import models
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)

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
                name=product_name, category_id=category)
            Price.objects.create(
                cost=cost, product_id=product.id, shop_id=shop)

    def __str__(self):
        return self.name


class Price(models.Model):
    cost = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, related_name='product_prices', on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Shop, related_name='shop_prices', on_delete=models.CASCADE)

    def get_cost(self):
        return self.cost

    def __str__(self):
        return str(self.cost)


class Url(models.Model):
    url = models.URLField()
    category = models.ForeignKey(
        Category, related_name='category_urls', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='urls',
                             on_delete=models.CASCADE)

    def get_url(self):
        return self.url

    def get_category(self):
        return self.category.id

    def get_shop(self):
        return self.shop


class BelyiVeter(Shop):
    def get_data(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        category_urls = Url.objects.filter(shop=1)
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
                    super().update_data(name, price, category, 1)
                nxt = driver.find_elements_by_xpath(
                    '//li[@class="bx-pag-next"]/a')
                if(len(nxt) > 0):
                    url = nxt[0].get_attribute('href')
                else:
                    url = ''
        driver.quit()

    class Meta:
        proxy = True


class Sulpak(Shop):

    def get_data(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
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

    class Meta:
        proxy = True


class TechnoDom(Shop):
    def get_data(self):
        category_urls = Url.objects.filter(shop=3)
        for category_url in category_urls:
            url = category_url.get_url()
            category = category_url.get_category()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content)
            products = soup.findAll('li', attrs={'class': 'ProductCard'})
            for product in products:
                name = product.find('h4')
                price = product.find('data')
                cost = 0
                for i in price.text:
                    try:
                        if int(i) >= 0 and int(i) <= 9:
                            cost = cost * 10 + int(i)
                    except ValueError:
                        continue
                super().update_data(name.text, cost, category, 3)
            driver.quit()

    class Meta:
        proxy = True


class Mechta(Shop):
    def get_data(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        category_urls = Url.objects.filter(shop=4)
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
                super().update_data(name, cost, category, 4)
        driver.quit()

    class Meta:
        proxy = True
