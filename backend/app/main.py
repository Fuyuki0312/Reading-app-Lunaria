from .api.router import router
from .services.book_services import get_book_services

from fastapi import FastAPI
from pydantic import BaseModel

# Initialize ---------------------------------------------

app = FastAPI()
app.include_router(router)

book_services = get_book_services()


class UserPreference(BaseModel):
    genres: list[str]


@app.get("/")
def home():
    return {
        "message": "Welcome to Lunaria!"
    }

