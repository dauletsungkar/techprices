# techprices

Это проект разработан для сравнения цен в разных магазинах (Sulpak, Technodom, Mechta, Белый ветер). Он собирает данные с сайтов магазинов каждый час, и обновляет 
в случаи изменений. Все собранные данные сохраняются, пре желаний можно создать график изменения цен.

#tracker

Весь проект состоит из одного приложения - tracker.

#Data base

Модель Category описывает категорий товаров и состоит только из одного поля name (CharField). Товары описаны моделью Product. Его поля: name (CharField), 
category(ForeignKey(Category)). Магазины описаны моделью Shop, и состоят из полей: name (CharField), url (URLField). Цены вынесены в отдельную таблицу, которая 
состоит из полей: cost (IntegerField), date (DateTimeField) , product (ForeiignKey(product)), shop (ForeignKey(shop)). Для каждого магазина создается отдельная 
proxy модель, потому что у каждого магазина свой способ сбора данных, и при этом мы храним их всех в одной таблице, так же это облегчает добавление новых магазинов 
для сбора данных. Что бы было еще легче есть модель Url c полями: url (URLField), shop (ForeignKey(Shop)), category (ForeignKey(Category)). Это сделано для 
упращения добавления магазинов блогодаря StackedInline, это же упрощает расширеие списка страниц для сбора даных уже существующих страниц.(Это так же упрощает 
добавлеие продукта вручную если такая нужда появится, вы сможе сразу с одной страницы указать все цены со всех магазинов которые есть в базе)

#How does it work?

Для начало нужно добавить магазин из которых и будут подкачиватся даные. Создадим porxy модель, которая будет наследовать от Shop, для магазина и распишем способ 
сбора данных в методе get_data(). Сделав миграцию создаем новый магазин с помощью админ панели, там же добавляем все ссылки и категорий которые они отображают. 
Осталось добавить нашу новую модель в лист shops который находит внутри tasks.py update_data() нашего приложения tracker. Все, теперь проект с помощью celery 
будет собирать новые данные со ссылок которые вы добавили вместе с вашим магазином. update_data() будет пробегаться по всем моделям магазинов и запускать метод
get_data(), он соберет все данные и вызовет метод super().update_data() из супер класса Shop, он же в свою очередь проверит изменилась ли цена и будет добавлять 
новую цену если она все-таки изменилась. Для получения результата перейдите по ссылке http://localhost:8000/api/products/, вы увидите json со всеми товарами. 
Что бы увидеть ценны на определенный продукт добавьте его id/.

#How to start?

Создайте виртуальную среду

`python -m venv venv`

Запустите ее

`source venv/bin/activate`

С помощью pip установите:

`django`

`celery`

`django_celery_beat`

`selenium`

`beautifulsoup4`

`django_restframework`

`webdriver_manager`

Установите redis

https://redis.io

Запустите проект

`python manage.py runserver`

Запустите сервер redis

`redis-server`

Запустите celery worker

`celery -A techprices worker -l INFO`

Запустите celery beat

`celery -A techprices beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`
