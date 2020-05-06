from flask import current_app
from bs4 import BeautifulSoup
import re
import functools
import requests
import io


class DownloadBook:
    @staticmethod
    def get_soup(url):
        res = requests.get(url)
        return BeautifulSoup(res.text, "lxml")

    @staticmethod
    def search_books( url, search_query):
        soup = DownloadBook.get_soup(url)
        tables = soup.find_all("table")[3:]

        books = []
        
        tables.pop()
        tables = [x for idx, x in enumerate(tables) if idx % 2 == 0]

        for table in tables:
            rows = table.find_all('tr')
            cols = rows[1].find_all('td')

            book = {}
            book['title'] = cols[2].find('a').get_text()
            book['author'] = rows[2].find_all('td')[1].find('a').get_text()

            if search_query in book["title"].lower() or search_query in book["author"].lower():
                book['download_url'] = cols[0].find('a').get('href')
                book['cover_url'] = cols[0].find('img').get('src')
                book["publisher"] = rows[4].find_all('td')[1].get_text()
                book["year"] = rows[5].find_all('td')[1].get_text()
                book['id'] = rows[6].find_all('td')[3].get_text()
                book["book_type"] = rows[9].find_all('td')[3].get_text()
                book["size"] = rows[9].find_all('td')[1].get_text().split('(')[0]

                books.append(book)

        return books


    @staticmethod
    def rank_list(records, search_query):
        def custom_comparator(a, b):
            if search_query in a["title"] and search_query in a["author"]:
                return 1
            else:
                return -1

        return sorted(records, key=functools.cmp_to_key(custom_comparator))


    @staticmethod
    def get_book(url):
        soup = DownloadBook.get_soup(url)
        table = soup.find('table')
        rows = table.find_all('tr')[0]
        col = rows.find_all('td')[1]
        header = col.find('h2')
        download_url = header.find('a').get('href')
        name = col.find('h1').get_text().strip()
        base_dir = current_app.config['BASE_DIR']
        ext = download_url.split('.').pop()

        _file = requests.get(download_url)
        raw_book = io.BytesIO()
        raw_book.write(_file.content)
        raw_book.seek(0)
        return raw_book, '{}.{}'.format(name, ext)
