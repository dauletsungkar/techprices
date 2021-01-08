from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    def update(self, product_name, price, category):
        return

    def hello_world(self):
        print("Just a shop")
        
    def __str__(self):
        return self.name


class Price(models.Model):
    cost = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, related_name='product_prices', on_delete=models.CASCADE)
    shop = models.ForeignKey(
        Shop, related_name='shop_prices', on_delete=models.CASCADE)

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
        return self.category

    def get_shop(self):
        return self.shop


class Sulpak(Shop):
    def get_data(self, driver):
        # category_urls = self.urls.all()
        # for category_url in category_urls:
        #     url = category_url.get_url()
        #     category = category_url.get_category()
        #     while url:
        #         driver.get(url)
        #         products = driver.find_elements_by_xpath(
        #             '//li[@class="tile-container"]')
        #         for product in products:
        #             name = product.get_attribute('data-name')
        #             price = int(float(product.get_attribute('data-price')))
        #             if 'Нет в наличии' not in product.text and price > 0:
        #                 super().update(name, price, category)
        #         nxt = driver.find_elements_by_xpath('//a[@class="next"]')
        #         if len(nxt) > 0:
        #             url = nxt[0].get_attribute('href')
        #         else:
        #             url = ''
        return 
    def hello_world(self):
        print("Sulpak")

    class Meta:
        proxy = True


class BelyiVeter(Shop):

    def get_data(self, driver):
        # category_urls = self.urls.all()
        # for category_url in category_urls:
        #     url = category_url.get_url()
        #     category = category_url.get_category()
        #     while(url):
        #         driver.get(url)
        #         laptops = driver.find_elements_by_xpath(
        #             '//div[@class="bx_catalog_item double"]')
        #         for laptop in laptops:
        #             name = laptop.find_element_by_xpath(
        #                 './/div[@class="bx_catalog_item_title"]/a').get_attribute('title')
        #             price = laptop.find_element_by_xpath(
        #                 './/div[@class="bx_catalog_item_price"]').text
        #             price = price.replace(' ', '')
        #             price = price.split('₸')
        #             if(len(price) > 2):
        #                 price = int(price[1])
        #             else:
        #                 price = int(price[0])
        #             super().update(name, price, category)
        #         nxt = driver.find_elements_by_xpath(
        #             '//li[@class="bx-pag-next"]/a')
        #         if(len(nxt) > 0):
        #             url = nxt[0].get_attribute('href')
        #         else:
        #             url = ''
        return

    def hello_world(self):
        print("Sulpak")

    class Meta:
        proxy = True
