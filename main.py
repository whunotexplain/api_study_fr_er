from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr
from items_views import router as items_router
from users.views import router as users_router
from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(users_router)




@app.get("/")
def hello_index():
    return {
        "message": "Hello world!!"
    }


@app.get("/hello/")
def hello(name: str):
    name = name.strip().title()
    return {"message": f"Hello, {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)