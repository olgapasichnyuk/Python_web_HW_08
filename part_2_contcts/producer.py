import pika
from faker import Faker

from models_contact import Contact

"""Під час запуску скрипта producer.py він генерує певну кількість фейкових контактів та записує їх у базу даних.
Потім поміщає у чергу RabbitMQ повідомлення, яке містить ObjectID створеного контакту, і так для всіх згенерованих контактів.

Додаткове завдання
Введіть у моделі додаткове поле телефонний номер.
Також додайте поле, що відповідає за кращий спосіб надсилання повідомлень — SMS по телефону або email.
Нехай producer.py відправляє у різні черги контакти для SMS та email.
Створіть два скрипти consumer_sms.py та consumer_email.py, кожен з яких отримує свої контакти та обробляє їх."""

fake_data = Faker()

for _ in range(30):
    Contact(fullname=fake_data.name(),
            email=fake_data.email(),
            phone=fake_data.phone_number(),
            is_sent=False,
            prefer_email=fake_data.boolean()).save()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


def sms_deque():
    channel.queue_declare(queue='send_sms')
    for contact in Contact.objects():
        if not contact.prefer_email and contact.phone:
            msg = f"{contact.id}"
            channel.basic_publish(exchange='', routing_key='send_sms', body=msg.encode())


def email_deque():
    channel.queue_declare(queue='send_email')
    for contact in Contact.objects():
        if contact.prefer_email and contact.email:
            msg = f"{contact.id}"
            channel.basic_publish(exchange='', routing_key='send_email', body=msg.encode())


if __name__ == '__main__':
    sms_deque()
    email_deque()
    connection.close()
