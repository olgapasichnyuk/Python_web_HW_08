import configparser

from mongoengine import Document, connect
from mongoengine.fields import StringField, BooleanField

"""Використовуючи ODM Mongoengine, створіть модель для контакту.
Модель обов'язково повинна включати поля: повне ім'я, email та логічне поле, яке має значення False за замовчуванням.
Воно означає, що повідомлення контакту не надіслано і має стати True, коли буде відправлено. Інші поля для інформаційного навантаження можете придумати самі."""

"""Введіть у моделі додаткове поле телефонний номер. Також додайте поле, що відповідає за кращий спосіб надсилання 
повідомлень — SMS по телефону або email. """

config = configparser.ConfigParser()
config.read('config.ini')
mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')

connect(
    host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@pasichniuk.qpmb3z9.mongodb.net/{db_name}?retryWrites=true&w=majority",
    ssl=True)


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    is_sent = BooleanField()
    prefer_email = BooleanField()
