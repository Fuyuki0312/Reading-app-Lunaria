from pathlib import Path


class Config:

    def __init__(self):

        # Model
        self.LLM = "openai:gpt-5-nano" # used with LangChain
        self.EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
        self.NUM_OF_RECOMMENDED_BOOK = 5 # the K number
        self.LLM_FOR_INTENT_EXTRACTION = "qwen3.5:4b-q4_K_M"

        # RAG
        self.NUM_OF_BOOKS_THRESHOLD_TO_TRIGGER_RAG = 15
        self.NUM_OF_BOOKS_RETURNED_FROM_RAG = 10
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.CHROMA_DB_PATH = BASE_DIR / "chroma_db"

        if not self.NUM_OF_BOOKS_RETURNED_FROM_RAG > self.NUM_OF_RECOMMENDED_BOOK:
            raise Exception("RAG must return more books than the number of books that the LLM would recommend.")

        # Seed
        self.RANDOM_SEED = 123456789
        self.TORCH_SEED = 42

        # Evaluation
        self.RELEVANCE_THRESHOLD = 2 # if a book's relevance score is higher than this value, the book will be seen as relevant to be recommended to the related user
        self.NUM_DIGITS_ROUNDED_FOR_METRICS = 4


    def get_system_prompt_for_model(
            self,
            books: list
        ):

        system_prompt = f"""You are the book recommendation AI of Lunaria, an e-book application on mobile devices.
            Your task is to recommend books based on the user's reading preferences.
            
            List of all available books that can be recommended:
            {books}
            
            
            Output's format rules:
            - Recommend exactly {self.NUM_OF_RECOMMENDED_BOOK} books. If there is no relevant book left, you have to recommend other irrelevant books to reach this number.
            - Only recommend books that exist in the provided book list.
            - book_id must exactly match the provided ID. Caution: book_id is discontinuous in order (e.g. book_id 6 does NOT exist).
            - Only give book_id and reason.
            - Keep each reason short.
            
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

        return system_prompt


    def get_prompt_for_llm_in_intent_extraction(self):

        prompt = """
        You are a preference extraction component in a book recommendation system.
        Your task is to extract structured preferences from the user's text.
        Your output will be used to retrieve relevant books and filter out books that violate the user's explicit exclusions.

        Entity intent rules:
        - If the user explicitly refuses to read books by an author, label that author as "exclude".
        - If the user currently prefers an author, label that author as "prefer".
        - If the user mentions a book they enjoyed as an example of their taste, label that book as "reference".
        - If no entities are provided, return results as an empty list [].
        - If no genres are explicitly disliked or rejected, return excluded_genres as an empty list [].
        - Use "neutral" only when the user's intent toward the entity cannot be determined.
        - Current preferences override past preferences.
        
        Genre exclusion rules:
        - Extract explicitly disliked genres into excluded_genres.
        - Only use exact names from known_genres.
        - Do not infer exclusions from vague descriptions.
        
        Rules:
        1. Consider negation, past preferences, and changes in preference.
        2. Only extract excluded genres from the provided known_genres.
        3. Never infer hard exclusions from vague descriptions.
        4. Do not invent entities or genre names.
        6. Return empty lists when no matching information exists.
        7. Do not recommend books.
        
        Examples:
        "I don't want Iris Vale anymore."
        -> Iris Vale: exclude
        
        "I loved The Silence Between Stars."
        -> The Silence Between Stars: reference
        
        "I hate Mystery."
        -> excluded_genres: ["Mystery"]
        
        "I want something interesting to read."
        -> Output: {"results": [], "excluded_genres": []}
        """

        return prompt