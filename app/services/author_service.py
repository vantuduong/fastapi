from datetime import datetime
from uuid import UUID

from schemas.author import Author
from services.base_service import BaseService, not_found_exception


class AuthorService(BaseService):

    def get_authors(self, **filters):
        limit = filters.get('limit', 10)
        page = filters.get('page', 1)
        query = self._db.query(Author)

        if filters.get('full_name'):
            query = query.filter(Author.full_name.ilike(f'{filters.get("full_name")}%') )

        return query.offset((page-1)*limit).limit(limit).all()

    def get_all_authors(self):
         return self._db.query(Author).all()

    def get_author_by_id(self, author_id: UUID):
        author = self._db.query(Author).filter(Author.id == author_id).first()

        if not author:
            raise not_found_exception()

        return author

    def create_author(self, data) -> Author:
        author = Author(**data)
        author.created_at = datetime.now()

        return self.save(author)


    def update_author(self, author_id: UUID, data: dict):
        author = self.get_author_by_id(author_id)

        author.full_name = data.get('full_name')
        author.gender = data.get('gender')
        author.updated_at = datetime.now()

        return  self.save(author)

    def delete_author(self, author_id: UUID):
        author = self.get_author_by_id(author_id)

        self.delete(author)
