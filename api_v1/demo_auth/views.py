import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from typing import Annotated, Any
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
from time import time


router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()

@router.get("/basic-auth/")
def demo_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)] 
):
    return {
        "Message":"Hi",
        "username": credentials.username,
        "password": credentials.password,
    }

usernames_to_passwords = {
    "egor": "egor",
    "admin": "admin"
}

static_auth_token_to_username = {
    "097c2495935308b65ecf51e897a9e97fd314331bc1ce1370f9562e156bb3929a": "egor",
    "37306fac390125eee625f496355641fd96e845f796579fcae7ef5ef077781549": "admin"
}

def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token")
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )
    


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauhted_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauhted_exc

    #secrets
    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        correct_password.encode('utf-8'),
    ):
        raise unauhted_exc
    
    return credentials.username


@router.get("/basic-auth-username/")
def demo_auth_some_http_header(
    auth_username: str = Depends(get_auth_user_username)
):
    return {
        "Message": f"Hi, {auth_username}!",
        "username": auth_username
    }

@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "Message": f"Hi, {username}!",
        "username": username
    }

COOKIES: dict[str, dict[str, Any]]= {}
COOKIE_SESSION_ID_KEY = "web-app-cookie-session-id"

def generate_session_id() -> str:
    return uuid.uuid4().hex

def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY), 
):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not authenticated',
        )
    return COOKIES[session_id]


@router.post("/login-cookie/")
def demo_auth_login_set_cookie(
    response: Response,
    username: str = Depends(get_auth_user_username),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
    "username": username,
    "login_at":int(time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"Result": "successfull"}

@router.get("/check-cookie/")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return{
        "username": f"Hello, {username}!",
        **user_session_data
    }
