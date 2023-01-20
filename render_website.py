from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
import os


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('data/books.json', "r") as json_file:
        books = json.load(json_file)

    for page_number, books_package in enumerate(chunked(books, 10)):
        rendered_page = template.render(books=chunked(books_package, 2))
        os.makedirs('./pages/', exist_ok=True)
        with open(f"./pages/index{page_number}.html", 'w', encoding="utf-8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main__":
    main()
