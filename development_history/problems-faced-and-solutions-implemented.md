# Lunaria — Problem-Solving Journal

This documentation shows what problems I faced and what solutions I implemented accordingly (including successful and failed ones) during the development of Lunaria.


### 4. LLM Intent Extractor Frequently Returned Incomplete Entity Intents (Oct 2026)

**Problem:** Qwen3.5:4B frequently returned empty or incomplete entity intent lists, even when entities were provided. This caused the intent extractor to reject the entire response.

**Hypothesis about the cause:**

- The prompt did not clearly require the LLM to return an intent for every provided entity.
- Qwen3.5:4B might not be capable enough for this task.

**Successful Solutions:**

- Improved the prompt to require exactly one intent for each provided entity, including those with neutral intent.
- Replaced Qwen3.5:4B with Qwen3.5:9B after comparing their evaluation results. The new model results in slightly increased latency (approximately +0.5s/user) for intent extraction.

**Results:**

- Qwen3.5:4B's Exact Match Accuracy increased from 45% to 89% after prompt improvements.
- Qwen3.5:9B achieved 98% Exact Match Accuracy on the same 100-user evaluation dataset.

**Limitations:**

- The evaluation dataset was AI-generated, then manually reviewed and corrected by the developer.
- The prompt was improved using the same dataset, so the results do not yet demonstrate performance on unseen data.


### 3. RAG Failed to Reliably Retrieve Books by Author Names or Book Titles (Sep 2026)

**Problem:** Entities such as author names and book titles were not processed. With users who say they love any specific authors, RAG usually did not retrieve books of the authors.

**Causes:**
- Cosine similarity does not ensure to retrieve books with exact word matches.

**Solutions:**
- Implemented intent extractor using another LLM and Regex (regular expression). While build the extractor, there was problem #4
- Implemented an eval dataset and the intent extractor which achieved an Exact Match Accuracy of 0.98 across all type of simulated user (not including misspelled author names or misspelled titles in user description). However, this is just an evaluation for intent extraction, not necessarily its performance with real users.

**Limitaion:** The intent extractor cannot extract intents of misspelled author names or misspelled titles.

### 2. Baseline Outperformed LLM-Based Methods (Sep 2026)

**Problem:** The simple baseline performed better than Qwen-2B LLM-only and RAG, even for complex user preferences.

**Hypothesis about the cause:**
- The eval dataset was biased for Baseline.
- The prompt for Qwen-2B was not sufficient.
- There was data leakage.
- Qwen-2B was not capable enough for this task.

**Unsuccessful Attempts:**
- Adjusted the eval dataset to better evaluate how well a recommender understand user's free-text description.
- Did Prompt Engineering stuff to enable Qwen-2B to have a better understanding about the task.

**Successful Solutions:**
- Detected data leakage was caused by Baseline and fixed it, but doing this alone did not help LLM-based methods win Baseline.
- Switched to a more capable LLM, which is GPT-5 nano costing some API credits.

**Result:** LLM-based methods overshadowed Baseline for most of the users, but the LLM cost some API credits.


### 1. Lunaria's Release Build Crashed on Launch (Sep 2026)

**Problem:** The released Lunaria crashed immediately when opened.

**Investigation:**
- Inspected Android Logcat.
- Checked which port the backend was listening on.
- Tested whether the Android app could connect to the backend API.

**Successful Solutions:**
- Checked my laptop's local IPv4 address and updated the backend URL in the Android app accordingly.