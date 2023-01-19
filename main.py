from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open('data/books.json', "r") as json_file:
        books = json.load(json_file)

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
    # mb = []
    # for file_ in os.listdir('./data/books'):
    #     mb.append(''.join(file_.split('.')[1:-1])[1:])
    #
    # with open('data/books.json', "r") as json_file:
    #     books = json.load(json_file)
    #
    # for book in books:
    #     if book['title'] not in mb:
    #         books.remove(book)
    #
    # with open('data/books.json', "w") as json_file:
    #     json.dump(books, json_file, indent=2, ensure_ascii=False)
