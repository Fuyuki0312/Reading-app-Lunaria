from app.config import Config
from app.services.book_services import get_book_services
from app.services.user_services import get_user_services
from .model.user_account import UserAccount
from .model.username_and_genre_preference import UsernameAndPreferences
from .model.username import Username
from .model.preference_description import PreferenceDescription
from app.recommender.rag.llm.recommendation import recommend_books
from app.recommender.rag.retrieval import retrieve_books
from app.recommender.baseline.baseline import Baseline


from fastapi import APIRouter


# Initialize --------------------------------------------

router = APIRouter()

config = Config()

book_services = get_book_services()
user_services = get_user_services()

baseline = Baseline()

# Router for books -----------------------------------------------------

@router.get("/book-brief-info")
def get_book_brief_info():

    return book_services.get_books_with_genres()


@router.post("/recommend-books")
def recommend(username: Username):

    genre_preferences = user_services.get_genre_preferences_from_username(
        username=username.username
    )

    preference_description = (
        user_services.get_preference_description_from_username(
            username=username.username
        ) or ""
    ).strip()

    # If there is no text-free description from users, baseline will recommend books
    if preference_description == "":
        # Baseline's recommendations
        json_book_id_list = baseline.score_books(user_genre_preferences=genre_preferences)

    # Otherwise,
    else:

        # if there are more than a certain number of books in database, RAG comes in
        if book_services.get_the_number_of_books_in_database() >= config.NUM_OF_BOOKS_THRESHOLD_TO_TRIGGER_RAG:

            retrieved_books = retrieve_books(
                genre_preferences,
                preference_description
            )

            books_for_llm = book_services.index_books_with_id_list(
                retrieved_books
            )

            # LLM's recommendations at the end of RAG
            json_book_id_list = recommend_books(
                user_genre_preference=genre_preferences,
                user_preference_description=preference_description,
                books=books_for_llm
            )

        # Otherwise, give LLM all books in database without any retriever (LLM-only recommendation)
        else:

            json_book_id_list = recommend_books(
                user_genre_preference=genre_preferences,
                user_preference_description=preference_description,
                books=book_services.get_books_with_genres()
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


@router.post("/get-password-by-username")
def get_password_from_database_by_username(username: Username):

    password = user_services.get_password_by_username_from_database(
        username=username.username
    )
    account = UserAccount(
        username=username.username,
        password=password
    )

    return account


@router.post("/get-genre-preferences-by-username")
def get_genre_preferences_by_username(username: Username):

    genres = user_services.get_genre_preferences_from_username(
        username=username.username
    )

    return UsernameAndPreferences(
        username=username.username,
        genres=genres
    )


@router.post("/get-preference-description-by-username")
def get_preference_description_by_username(username: Username):

    description = user_services.get_preference_description_from_username(
        username=username.username
    )
    
    if description is None:
        description = ""

    return PreferenceDescription(
        username=username.username,
        description=description
    )