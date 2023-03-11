"""Реалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора
або набором тегів.

Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у наступному форматі команда: значення. Приклад:
name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
tag:life — знайти та повернути список цитат для тега life;
tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
exit — завершити виконання скрипту;"""

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

COMMANDS = ['name', 'tags', 'tag', 'help', 'exit']


@cache
def search_by_name(name):
    authors = Author.objects(fullname__startswith=name.capitalize())
    res = []
    for author in authors:
        res.extend(Quote.objects(author=author.id))

    for quote in res:
        print(f"{quote.author.fullname}{quote.quote}")


@cache
def search_by_tag(tag: str):

    res = Quote.objects(tags=tag)

    for quote in res:
        print(quote.quote)


@cache
def search_by_tags(tags: str):
    print(tags)
    tags = list(map(lambda x: x.strip(), tags.split(",")))
    print(tags)

    res = Quote.objects(tags__in=tags)

    for quote in res:
        print(quote.quote)


def my_help(_):
    print(f"Доступні комнади: {COMMANDS}")


def my_exit(_):
    quit()


def unknown_command(user_input):
    print(f"Невдома команда '{user_input}'.\nДоступні комнади: {COMMANDS}")


def input_parser(user_input):
    for command in handler.keys():
        if user_input.strip().startswith(command):
            cmd = command
            args = user_input.strip().removeprefix(cmd).strip().removeprefix(":").strip()
            return cmd, args

    return 'unknown_command', user_input


handler = {'name': search_by_name,
           'tags': search_by_tags,
           'tag': search_by_tag,
           'help': my_help,
           'exit': my_exit,
           'unknown_command': unknown_command
           }


def main():
    while True:
        raw_user_input = input(
            "Введіть команду у форматі 'команда: значення' наприклад name: Steve Martin \n"
            "або 'help' для перегляду переліку доступних комнад \nабо 'exit' для виходу:")

        if not raw_user_input:
            continue

        cmd, args = input_parser(raw_user_input)

        handler[cmd](args)


if __name__ == "__main__":
    main()
