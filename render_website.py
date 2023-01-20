from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('data/books.json', "r") as json_file:
        books = json.load(json_file)

    rendered_page = template.render(books=chunked(books, 2))

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main__":
    main()
