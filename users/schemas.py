from pydantic import BaseModel, EmailStr, Field


class Create_User(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
