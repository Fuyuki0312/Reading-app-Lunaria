# Lunaria — RAG Development Notes

**Last updated:** 2026-10-09  
**Status:** Planning — Not implemented yet.

## 1. Goal

Upgrade Lunaria's RAG to handle explicit author names, book titles, negative preferences, and complex user requests.

The system should be **production-oriented, modular, and independently evaluable**.

## 2. Current Problem

Lunaria uses E5 + Chroma to retrieve Top-10 books through cosine similarity.

- **Semantic similarity ≠ exact matching:** E5 may miss books by an explicitly preferred author.
- **Negation problem:** "I hate Dark Fantasy" can still retrieve Dark Fantasy books.
- **Retrieval bottleneck:** GPT-5 nano cannot recommend books missing from the candidate set.

## 3. Proposed Architecture

Combine **semantic retrieval** with **entity-aware retrieval**.

```text
User free-text
     ↓
Entity + Preference Extraction
     ↓
 ┌───────────┴───────────┐
 ↓                       ↓
E5 + Chroma        Metadata matching
(Semantic)         (Author / Title)
 ↓                       ↓
 └───────────┬───────────┘
             ↓
     Merge + Filter
             ↓
      GPT-5 nano
             ↓
    Backend Validation
```

**Implementation direction:**

- Start with dictionary matching using known authors/titles from MySQL instead of immediately introducing a NER model.
- Explore intent extraction to distinguish liked, disliked, historical, and conditional preferences.
- Use structured intermediate data to avoid mixing different intentions.
- Reuse the same retrieval components in production and evaluation.

*This architecture is proposed, not finalized.*

## 4. Important Production Edge Cases

| Situation | Engineering insight |
|---|---|
| User liked a book but now dislikes its author | Still use the book as a semantic reference, but exclude its author from recommendations |
| "I used to love Iris Vale" | Historical preference ≠ current preference |
| "I love Nora Vale, but only if..." | Author preference is conditional, not an absolute requirement |
| Only 3 eligible books remain | Never violate hard constraints just to return exactly 5 |
| Top-10 contains 7 excluded books | Filtering only after Top-10 may discard hundreds of valid candidates outside Top-10 |
| LLM recommends an excluded book | Backend must validate outputs rather than trusting the prompt |

**Important distinction:** A book can be useful for retrieval without being eligible for recommendation.

## 5. Design Principles

- **Entity recognition ≠ intent extraction.**
- **Cosine similarity ≠ logical filtering.**
- **Hard constraints take priority over recommendation count.**
- Separate retrieval logic from FastAPI and evaluation scripts.
- Evaluate dense-only vs hybrid retrieval independently.
- Prefer simple, testable solutions before introducing more models or frameworks.
- Do not treat untested architectural assumptions as proven results.

## 6. Open Questions

- How should intent extraction represent conflicting, historical, and conditional preferences?
- Should metadata filtering happen before retrieval, after retrieval, or through over-retrieval?
- How should semantic and metadata candidates be merged and ranked?
- How should the system recover when too few eligible books remain?
- How should retrieval quality and latency be evaluated separately?

## 7. Current Checkpoint

**Production Challenge: The Retrieval Filtering Trap**

Database: 1,000 books. Chroma Top-10 contains 7 excluded books, but many eligible books exist outside Top-10.

**Challenge:** Design a retrieval pipeline that respects hard constraints without losing valid candidates or introducing excessive latency.

**Next step:** Discuss filtering strategies and trade-offs **before writing code**.