from pydantic import BaseModel


class RecommendationForm(BaseModel):

    book_id: int
    reason: str

class RecommendationOutputForm(BaseModel):

    recommendation: list[RecommendationForm]