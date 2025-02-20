from . import Book


class Library:
    def __init__(self, storage):
        self.books = {}
        self.storage = storage
        self.last_id = None

    def _get_last_id_book(self):
        last_id = self.storage.get_last_id()
        return last_id

    def increment_book_id(self):
        self.last_id = int(self._get_last_id_book())
        self.last_id += 1
        self.storage.increment_last_id()

    def add_book(self, book: Book):
        if isinstance(book, Book):
            self.increment_book_id()
            book.id = str(self.last_id)
            self.storage.write_data(book.to_dict())
            return book
        raise ValueError("Неверный формат книги!")

    def get_book_by_id(self, book_id: str):
        book = self.books.get(book_id)
        if book:
            return book
        raise ValueError("Такой книги нет!")

    def get_book_by_isbn(self, isbn: str):
        results = []
        books = self.storage.read_data()
        for item in books:
            if isbn.lower() in item['ISBN'].lower():
                results.append(Book.from_dict(item))
        return results

    def get_books(self):
        books = self.storage.read_data()
        books_obj = []
        for book in books:
            books_obj.append(Book.from_dict(book))
        return books_obj

    def get_books_by_author(self, author: str):
        results = []
        books = self.storage.read_data()
        for item in books:
            if author.lower() in item['author'].lower():
                results.append(Book.from_dict(item))
        return results

    def get_books_by_title(self, title: str):
        results = []
        books = self.storage.read_data()
        for item in books:
            if title.lower() in item['title'].lower():
                results.append(Book.from_dict(item))
        return results

    def search_book(self, query):
        results = {}
        for id_, book in self.books.items():
            if query.lower() in book.author.lower():
                results[id_] = book
        return results

    def book_delete(self, isbn: str):
        books = self.storage.read_data()        #получаем список словарей
        for i, book in enumerate(books):        # проходим по списку словарей и
            if book['ISBN'].lower() == isbn.lower():    # удаляем словарь с нужным isbn
                books.pop(i)

        self.storage.file.seek(33)      # очищаем файл начиная с конца хедера (33)
        self.storage.file.truncate()

        for book in books:                 # добавляем заново книги из словаря в файл, перед этим преобразуя в Book
            self.add_book((Book.from_dict(book)))

    def get_book_count(self):
        count = self.storage.count_book()
        return count

    def check_book(self, isbn):
        books = self.storage.read_data()
        for item in books:
            if item['ISBN'].lower() == isbn.lower():
                return item['ISBN']
        return None

    def dump_books_data(self, filename):
        self.storage.dump_books_to_json(filename)

