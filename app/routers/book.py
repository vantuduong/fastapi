from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.book import BookListModel, BookDetailModel, BookFormModel
from schemas.user import User
from services.auth_service import token_interceptor
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Book"])

@router.get('', response_model=list[BookListModel])
async def get_books(
    title: str = None,
    author_id: UUID | None = None,
    is_published: bool | None = None,
    limit: int = 10,
    page: int = 1,
    book_service: BookService = Depends()
):
    return book_service.get_books(
        title=title,
        author_id=author_id,
        is_published=is_published,
        limit=limit,
        page=page
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookListModel)
async def create_book(
        request: BookFormModel,
        user: User = Depends(token_interceptor),
        book_service: BookService = Depends()
):
    data = request.model_dump()
    data['user_id'] = user.id

    return book_service.create_book(data)

@router.get('/{book_id}', response_model=BookDetailModel)
async def get_book(book_id: UUID, book_service: BookService = Depends()):
    return book_service.get_book_by_id(book_id)

@router.put('/{book_id}', response_model=BookListModel)
async def update_book(
    book_id: UUID, request: BookFormModel,
    user: User = Depends(token_interceptor),
    book_service: BookService = Depends()
):
    book = book_service.get_book_by_id(book_id)
    if not user.is_admin and book.user_id != user.id:
        raise HTTPException(status_code=403, detail='Permission denied')

    return book_service.update_book(book, request.model_dump())

@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, user: User = Depends(token_interceptor), book_service: BookService = Depends()):
    book = book_service.get_book_by_id(book_id)

    if not user.is_admin and book.user_id != user.id:
        raise HTTPException(status_code=403, detail='Permission denied')

    book_service.delete_book(book)
