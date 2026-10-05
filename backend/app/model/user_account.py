from pydantic import BaseModel


class UserAccount(BaseModel):
    username: str
    password: str
    genre_preferences: list = []