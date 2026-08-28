from app.services.book_services import get_book_services
from app.services.user_services import get_user_services
from .model.user_account import UserAccount
from .model.username_and_genre_preference import UsernameAndPreferences
from .model.username import Username
from .model.preference_description import PreferenceDescription
from app.ai.recommendation import recommend_books


from fastapi import APIRouter


# Initialize --------------------------------------------

router = APIRouter()

book_services = get_book_services()
user_services = get_user_services()


# Router for books -----------------------------------------------------

@router.get("/book-brief-info")
def get_book_brief_info():

    return book_services.get_books_with_genres()


@router.post("/recommend-books")
def recommend(username: Username):

    genre_preferences = user_services.get_genre_preferences_from_username(
        username=username.username
    )

    preference_description = user_services.get_preference_description_from_username(
        username=username.username
    )

    json_book_id_list = recommend_books(
        user_genre_preference=genre_preferences,
        user_preference_description=preference_description
    )

    recommended_books = book_services.index_books_with_id_list(json_book_id_list)

    return recommended_books


# Router for users ----------------------------------------------------

@router.post("/register-user")
def add_user_to_database(account: UserAccount):

    user_services.register_user_account_to_database(
        username=account.username,
        password=account.password,
        genre_preferences=account.genre_preferences
    )


@router.post("/register-genre-preferences")
def add_genre_preferences_to_database(user_preference: UsernameAndPreferences):

    user_services.register_genre_preferences_to_database(
        preferences=user_preference.genres,
        username=user_preference.username
    )


@router.post("/register-preference-description")
def add_preference_description_to_database(preference_description: PreferenceDescription):

    user_services.register_preference_description_to_database(
        username=preference_description.username,
        description=preference_description.description
    )


@router.get("/get-all-username")
def get_all_username_from_database():

    return user_services.get_all_username_from_database()
