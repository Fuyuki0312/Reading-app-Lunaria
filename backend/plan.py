# TODO backend:
#  1. (DONE) Ask ChatGPT to write more books and add them to my database
#  2. (DONE) Send the books and user's preferences (make them up by hard-coding at first) to Qwen and ask for json-formated recommendation (prompt engineering)
#  3. (DONE-HALF (RAG's metrics not included)) Do Machine-Learning-Engineer stuff to improve model (prompt engineering, fine-tune if needed, calculate metrics). Note: read Designing Machine Learning Systems
#  3.1. (DONE BUT FAIL) Create a baseline for the recommendation system and prove a LLM is better than the baseline
#  4. Use another LLM to do Semantic Search
#  5. Add RAG to search a larger number of books

# TODO frontend:
#  1. Make Lunaria functionable: enable users to scroll, choose a book and read it
#  2. (DONE) Display the recommendation on the app
#  3. (DONE) Learn how to get users' inputs from the app
#  3.1. (DONE) Create a search bar to search book title
#  4. (DONE) Log-in: Create something for log-in stuff (maybe only username and insecured_password is fine for the time being)
#  5. (DONE) Collect user preferences: Create a test to get users' preferences in their first log-in
#  6. Add settings: enable users to configure font size, background color (maybe I need something to store user's settings)
#  7. Style: Decorate app with Lunaria style

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os
import json

env_path = Path(__file__).resolve().parent / "app" / ".env"

load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")

with open("evaluation\\eval_dataset\\books.json", "r") as f:

    books = json.load(f)

system_prompt = f"""You are the book recommendation AI of Lunaria, an e-book application on mobile devices.
            Your task is to recommend books based on the user's reading preferences.
            You MUST return only valid JSON.

            Output format:

            {{
                "recommendations": [
                    {{
                        "book_id": int
                    }}
                ]
            }}


            List of all available books that can be recommended:
            {books}


            Output's format rules:
            - Recommend exactly 5 books. If there is no relevant book left, you have to recommend other irrelevant books to reach this number.
            - Only recommend books that exist in the provided book list.
            - book_id must exactly match the provided ID.
            - Keep each reason short.
            - Do not output Markdown.
            - Do not output any text before or after the JSON.

            HARD EXCLUSION RULE — HIGHEST PRIORITY:

                1. Identify any genre that the user explicitly says they dislike,
                   hate, do not want, or are not interested in.

                2. NEVER recommend a book if ANY of that book's genres matches
                   one of those disliked genres.

                3. This rule has higher priority than all relevance and ranking rules.

                4. If necessary, recommend a completely irrelevant but non-violating
                   book rather than a relevant book that violates this rule.

                5. Before returning the final JSON, verify that every recommended book
                   satisfies this exclusion rule.

                Example:
                User likes: ["Fantasy"]
                User dislikes: ["Dark Fantasy"]

                Book genres: ["Fantasy", "Dark Fantasy"]

                -> Do not recommend this book, because user will not like it even when the book may have genres the user like. Instead, recommend other books even when other books seem irrelevant.

            Other rules:

            - If user's genre preferences do not match exactly any book's genres, recommend books that are the most relevant.
            - The recommendations must be ordered from most suitable to least suitable."""
client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    instructions= system_prompt,
    input="My genre preferences: ['Fantasy', 'Mystery']\nOther descriptions of preferences: None"
)

print(response.output_text)
print(response.output_text)
print(response.usage)