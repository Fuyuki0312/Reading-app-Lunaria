from pathlib import Path
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from test.llm_reponse_model import RecommendationOutputForm

env_path = Path(__file__).resolve().parent.parent / "app" / ".env"
load_dotenv(env_path)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the book recommendation AI of Lunaria." +
        """Recommend 2 books from this list:

        1. Moonlit Archive - Fantasy
        2. Silent Algorithm - Science Fiction
        3. Crimson Manor - Mystery"""
    ),
    (
        "human",
        "My favorite genre is {genre}."
    )
])

model = init_chat_model("openai:gpt-5-nano").with_structured_output(
    RecommendationOutputForm
)

chain = prompt | model

response = chain.invoke({
    "genre": ["Fantasy", "Mystery"]
})

print(type(response))
print(response.recommendation)

