from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
import os
from math import ceil


def on_reload():
    """Функция рендерит html страницы с данными из books.json
    """
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('data/books.json', "r") as json_file:
        books = json.load(json_file)

    total_page_number = ceil(len(books) / 10)

    for page_number, books_package in enumerate(chunked(books, 10)):
        page_number += 1
        rendered_page = template.render(books=chunked(books_package, 2),
                                        page_number=page_number,
                                        total_page_number=total_page_number)
        os.makedirs('./pages/', exist_ok=True)
        with open(f"./pages/index{page_number}.html", 'w', encoding="utf-8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    server = Server()
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root='.')
