from pydantic import BaseModel

class PreferenceDescription(BaseModel):

    description: str
    username: str