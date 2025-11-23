from fastapi import FastAPI, APIRouter, Path
from typing import Annotated

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def list_items():
    return [
        "item 1",
        "item 2",
        "item 3",
        "item 4",
    ]

@router.get("/latest/")
def get_latest_item():
    return {"item": {"id":"0", "name": "latest"}}



@router.get("/{item_id}")
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {
        "item" : {
            "id": item_id
        }
    }

