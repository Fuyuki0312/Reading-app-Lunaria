# TODO backend:
#  1. (DONE) Ask ChatGPT to write more books and add them to my database
#  2. (DONE) Send the books and user's preferences (make them up by hard-coding at first) to Qwen and ask for json-formated recommendation (prompt engineering)
#  3. (DONE-HALF (metrics not included)) Do Machine-Learning-Engineer stuff to improve model (prompt engineering, fine-tune if needed, calculate metrics). Note: read Designing Machine Learning Systems
#  3.1. Create a baseline for the recommendation system and prove a LLM is better than the baseline
#  4. Use another LLM to do Semantic Search
#  5. Add RAG to search a larger number of books
#  6. Make Qwen become an agent (before that, figure out if this is actually useful)

# TODO frontend:
#  1. Make Lunaria functionable: enable users to scroll, choose a book and read it
#  2. (DONE) Display the recommendation on the app
#  3. (DONE) Learn how to get users' inputs from the app
#  3.1. (DONE) Create a search bar to search book title
#  4. (DONE) Log-in: Create something for log-in stuff (maybe only username and insecured_password is fine for the time being)
#  5. (DONE) Collect user preferences: Create a test to get users' preferences in their first log-in
#  6. Add settings: enable users to configure font size, background color (maybe I need something to store user's settings)
#  7. Style: Decorate app with Lunaria style

# TODO model evaluation:
#  metrics: Precision@K, NDCG@K, Diversity, Coverage, Constraint Violation Rate
#  Note: hãy lưu lại những cuốn sách khác nhau mà system đã recommend để tính Coverage

import random

a = [1, 2, 3, 4]
random.shuffle(a)
print(a)