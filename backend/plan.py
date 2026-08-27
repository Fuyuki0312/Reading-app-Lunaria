# TODO backend:
#  1. (DONE) Ask ChatGPT to write more books and add them to my database
#  2. (DONE) Send the books and user's preferences (make them up by hard-coding at first) to Qwen and ask for json-formated recommendation (prompt engineering)
#  3. (DONE-HALF (metrics not included)) Do Machine-Learning-Engineer stuff to improve model (prompt engineering, fine-tune if needed, calculate metrics). Note: read Designing Machine Learning Systems
#  4. Use another LLM to do Semantic Search
#  5. Add RAG to search a larger number of books
#  6. Make Qwen become an agent (before that, figure out if this is actually useful)

# TODO frontend:
#  1. Make Lunaria functionable: enable users to scroll, choose a book and read it (make a searching algorithm)
#  2. (DONE) Display the recommendation on the app
#  3. (DONE) Learn how to get users' inputs from the app
#  3.1. (DONE) Create a search bar to search book title
#  4. Log-in: Create something for log-in stuff (maybe only username and insecured_password is fine for the time being)
#  5. (DONE) Collect user preferences: Create a test to get users' preferences in their first log-in
#  6. Add settings: enable users to configure font size, background color (maybe I need something to store user's settings)
#  7. Style: Decorate app with Lunaria style

# TODO first:
#  1. (DONE) Truyền genre_preferences từ database sang prompt của Qwen
#  2. (DONE but not tested yet) Prompt Engineering: Let Qwen knows it can encounter user's genre preferences that do not exist in all available books
#  3. Thêm điều kiện để Register Account (không được trùng username với user khác)
#  4. Complete login process


