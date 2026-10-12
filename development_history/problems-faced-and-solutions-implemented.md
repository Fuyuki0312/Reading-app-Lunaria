# Lunaria — Problem-Solving Journal

This documentation shows what problems I faced and what solutions I implemented accordingly (including successful and failed ones) during the development of Lunaria.


### 1. Baseline Outperformed LLM-Based Methods (Sep 2026)

**Problem:** The simple baseline performed better than Qwen-2B LLM-only and RAG, even for complex user preferences.

**Hypothesis about the cause:**
- The eval dataset was biased for baseline.
- The prompt for Qwen-2B was not sufficient.
- Qwen-2B was not capable enough for this task.

**Attempts:**
- Adjust the eval dataset to better evaluate how well a recommender understand user's free-text description.
- Do Prompt Engineering stuff to enable Qwen-2B to have a better understanding about the task.

**Successful solutions:**
- Switch to a more capable LLM, which is GPT-5 nano costing some API credits.

**Result:** LLM-based methods overshadowed Baseline for most of the users, but the LLM cost some API credits.


### 2. RAG Failed to Reliably Retrieve Books by Author Names or Book Titles (Sep 2026)

**Problem:** Entities such as author names and book titles were not processed. With users who say they love any specific authors, RAG usually did not retrieve books of the authors.

**Causes:**
- Cosine similarity does not ensure to retrieve books with exact word (author names or book titles) matches.