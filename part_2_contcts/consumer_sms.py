import sys

import pika

from models_contact import Contact

"""Скрипт consumer.py отримує з черги RabbitMQ повідомлення, обробляє його та імітує функцією-заглушкою надсилання повідомлення по email.
Після надсилання повідомлення необхідно логічне поле для контакту встановити в True.
Скрипт працює постійно в очікуванні повідомлень з RabbitMQ."""


def send_sms():
    pass


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='send_sms')

    def callback(ch, method, properties, body):
        # body повідомлення містить ObjectID контакту
        contact_id = body.decode()
        contact = Contact.objects(id=contact_id)[0]

        # імітація відправки смс
        send_sms()
        print(f"Зімітовано відправку Sms повідомлення контакту {contact.fullname}")

        # встановлення статусу True в полі для контакту, яке відображає статус відправки смс

        contact.update(is_sent=True)
        print(f"Поле, яке відображає статус відправки смс для контакту {contact.fullname} змінено на True")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='send_sms', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
