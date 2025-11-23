from .schemas import Create_User

def create_user(user_in: Create_User) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }