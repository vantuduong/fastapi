from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.author import AuthorModel, AuthorViewModel, AuthorDetailModel
from schemas.base_entity import Gender
from schemas.user import User
from services.auth_service import token_interceptor
from services.author_service import AuthorService

router = APIRouter(prefix="/authors", tags=["Author"])

@router.get('', response_model=list[AuthorViewModel])
async def get_authors(
        full_name: str = None,
        gender: Gender = 'N',
        limit: int = 10,
        page: int = 1,
        author_service: AuthorService = Depends()
):
    return author_service.get_authors(full_name=full_name, gender=gender, limit=limit, page=page)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=AuthorViewModel)
async def create_author(
    request: AuthorModel,
    user: User = Depends(token_interceptor),
    author_service: AuthorService = Depends()
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Permission denied')

    return author_service.create_author(request.model_dump())

@router.get('/{author_id}', response_model=AuthorDetailModel)
async def get_author(author_id: UUID, author_service: AuthorService = Depends()):
    print(author_id)
    return author_service.get_author_by_id(author_id)

@router.put('/{author_id}', response_model=AuthorViewModel)
async def update_author(
    author_id: UUID,
    request: AuthorModel,
    user: User = Depends(token_interceptor),
    author_service: AuthorService = Depends()
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Permission denied')
    return author_service.update_author(author_id, request.model_dump())

@router.delete('/{author_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: UUID,
    user: User = Depends(token_interceptor),
    author_service: AuthorService = Depends()
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Permission denied')

    author_service.delete_author(author_id)
