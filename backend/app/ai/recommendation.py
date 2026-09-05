from .model import get_model_and_processor
from app.config import Config
from app.services.book_services import get_book_services

import torch
import json

config = Config()
book_services = get_book_services()

def recommend_books(
        user_genre_preference=[],
        user_preference_description=None
) -> list[dict]:

    model, processor = get_model_and_processor()
    books = book_services.get_books_with_genres()

    if user_genre_preference == []:
        user_genre_preference = "Any"

    messages = [

        {
            "role": "system",
            "content": [
                {"type": "text", "text": config.get_system_prompt_for_model(books)}
            ]
        },

        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"My genre preferences: {user_genre_preference}\nOther descriptions of preferences: {user_preference_description}"
                }
            ]
        },

    ]

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        enable_thinking=False
    ).to(model.device)


    with torch.inference_mode():
        raw_outputs = model.generate(**inputs, max_new_tokens=500)
    decoded_outputs = processor.decode(raw_outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
    json_outputs = json.loads(decoded_outputs)

    recommendations = json_outputs["recommendations"]

    return recommendations # List

