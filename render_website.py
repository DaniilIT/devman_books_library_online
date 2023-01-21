import argparse
import json
import os
from math import ceil

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


BOOKS_PER_PAGE_NUM = 10
COLUMNS_NUM = 2


def on_reload():
    """Функция рендерит html страницы с данными из books.json
    """
    global args

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open(args.json_path, "r") as json_file:
        books = json.load(json_file)

    total_page_number = ceil(len(books) / BOOKS_PER_PAGE_NUM)

    for page_number, books_package in enumerate(chunked(books, BOOKS_PER_PAGE_NUM)):
        page_number += 1
        rendered_page = template.render(books=chunked(books_package, COLUMNS_NUM),
                                        page_number=page_number,
                                        total_page_number=total_page_number)
        os.makedirs('./pages/', exist_ok=True)
        with open(f"./pages/index{page_number}.html", 'w', encoding="utf-8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Данная программа - это сервер для сайта с библиотекой книг"
    )
    parser.add_argument(
        "--json_path",
        help="путь к *.json файлу с информацией про книги",
        default="data/books.json",
        type=str
    )
    args = parser.parse_args()

    server = Server()
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root='.')
