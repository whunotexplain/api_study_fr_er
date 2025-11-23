from .schemas import Create_User
from fastapi import APIRouter
from users import crud


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/users/")
def create_usere(user: Create_User):
    return crud.create_user(user_in=user)