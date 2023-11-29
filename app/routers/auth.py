from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService, token_exception, create_access_token

router = APIRouter(prefix="/auth", tags=["Author"])

@router.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise token_exception()

    return {
        "access_token":  create_access_token(user, timedelta(minutes=60)),
        "token_type": "bearer"
    }
