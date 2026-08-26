from pydantic import BaseModel

class UsernameAndPreferences(BaseModel):

    username: str
    genres: list[str]