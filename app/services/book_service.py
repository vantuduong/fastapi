from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import joinedload

from schemas.book import Book
from services.base_service import BaseService, not_found_exception


class BookService(BaseService):

    def get_books(self, **filters):
        limit = filters.get('limit', 10)
        page = filters.get('page', 1)
        query = self._db.query(Book)

        if filters.get('title'):
            query = query.filter(Book.title.ilike(f'%{filters.get("title")}%'))

        if filters.get('author_id'):
            query = query.filter(Book.author_id == filters.get('author_id'))

        if filters.get('is_published'):
            query = query.filter(Book.is_published == filters.get('is_published'))

        if filters.get('user_id'):
            query = query.filter(Book.user_id == filters.get('user_id'))

        return query.offset((page-1)*limit).limit(limit).all()

    def get_book_by_id(self, book_id: UUID):
        book = self._db.query(Book).filter(Book.id == book_id)\
            .options(joinedload(Book.author, innerjoin=True))\
            .first()

        if not book:
            raise not_found_exception()

        return book

    def create_book(self, data: dict):
        book = Book(**data)
        book.created_at = datetime.now()

        return self.save(book)

    def update_book(self, book_id: UUID | Book, data: dict):

        if isinstance(book_id, Book):
            book = book_id
        else:
            book = self.get_book_by_id(book_id)

        book.title = data.get('title')
        book.author_id = data.get('author_id')
        book.rating = data.get('rating')
        book.is_published = data.get('is_published')
        book.description = data.get('description')
        book.updated_at = datetime.now()

        return self.save(book)

    def delete_book(self, book_id: UUID | Book):
        if isinstance(book_id, Book):
            book = book_id
        else:
            book = self.get_book_by_id(book_id)
        self.delete(book)
