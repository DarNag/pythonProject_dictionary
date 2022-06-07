import conf
import random
import faker
import json


def main():  # функция запускает генератор, формирует список из 100 книг (список словарей) и записывает его в json файл
    c = return_dict()  # cоздаем генератор
    with open("dictionary.json", "w", encoding="utf8") as f:  # запись словарей в json файл
        for _ in range(100):
            json.dump(next(c), f, indent=4, ensure_ascii=False)


def return_dict(start: int = 1):  # функция-генератор, формирующая словарь
    pk = start
    while True:
        dict_ = {
            "model": conf.MODEL,
            "pk": pk,
            "fields": func_fields()
        }
        yield dict_
        pk += 1


def func_fields() -> dict:  # функция, формирующая словарь fields
    fields = {
        "title": func_title(),
        "year": func_year(),
        "pages": func_pages(),
        "isbn13": func_isbn(),
        "rating": func_rating(),
        "price": func_price(),
        "author": func_author()
    }
    return fields


def decorator_factory(len_):  # фабрика декораторов для проверки максимальной длины названия книги
    def decorator(func):
        def wrapper():
            if len(func()) > len_:
                raise ValueError("Превышена длина названия книги")
            result = func()
            return result

        return wrapper

    return decorator


def func_title_gen() -> str:  # вспомогательная функция-генератор, выдает название книги из файла books.txt
    with open("books.txt", 'r', encoding='utf8') as f:
        for line in f:
            yield line


@decorator_factory(100)
def func_title() -> str:  # функция, формирующая название книги
    books = func_title_gen()  # создаем генератор названий
    n = random.choice(range(sum(1 for _ in books)))  # выбираем рандомное число из количества книг в файле books
    with open("books.txt", 'r', encoding='utf8') as f:  # считываем строку из файла
        for i, line in enumerate(f):
            if i == n:
                return line.rstrip()


def func_year() -> int:  # функция, формирующая год
    return random.choice(range(1900, 2023, 1))


def func_pages() -> int:  # функция, формирующая количество страниц
    return random.choice(range(1, 2000, 1))


def func_isbn() -> str:  # функция, формирующая isbn
    fake = faker.Faker()
    return fake.isbn13()


def func_rating() -> float:  # функция, формирующая рейтинг
    return round(random.uniform(0.00, 5.00), 2)


def func_price() -> float:  # функция, формирующая цену
    return round(random.uniform(0.00, 100000), 2)


def func_author() -> list:  # функция, формирующая список авторов
    fake = faker.Faker()
    list_ = []
    for _ in range(random.choice(range(1, 4, 1))):
        list_.append(fake.name())
    return list_


if __name__ == '__main__':
    main()
