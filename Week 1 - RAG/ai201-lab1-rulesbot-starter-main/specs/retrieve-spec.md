# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
The query, n_results, and `["documents", "metadatas", "distances"]` to the `include` parameter
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
retrieved[0]...
{
   "text": "Lorem ipsum....",
   "game": "catan",
   "distance": 0.1
}
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
The nesting exists because ChromaDB's .query() function allows us to pass multiple queries at once for the semantic search. We only want to pass one query at a time, so we are only interested in the data at the 0th index of each value in the dictionary returned by _collection.query()
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
At the application level / from an overall perspective, filtering above a certain distance score is absolutely a feature that would benefit RuleBot to ensure only relevant context is fed to the LLM at the generation stage. 

However, at the module level / from the perspective of the retrieve() function, I believe a wise design choice would be to not implement distance filtering here, and instead delegate it to generator.py. The specs of retrieve mention n_results as the # of results to return, and implementing distance filtering on top of it would violate this spec. Additionally, it would be a better choice to delegate the responsibility of filtering to n_results to the retrieval phase, and give the responsibility of filtering to a specific distance value to the generation phase.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
(a) If empty, returns empty list.
(b) Even if the query doesn't match chunks well, it will still return the n chunks with lowest distance scores.
(c) It will return chunks irrespective of the game.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: What happens if I roll a 7 in Catan?
Top result game: Catan
Distance score: 0.4785
Does it make sense? 
-> yes, it outputted a chunks containing an excerpt from the game rules that specifically mentioned what to do when rolling a 7.
```

**One thing about the query results that surprised you:**

```
As the distance score increased (~>0.5), the results quickly became irrelevant. The second and third query results for the above prompt were for monopoly and contained information completely unrelated to the query. I could see the importance of filtering by distance score, and how easily we could feed junk data to the LLM. 
```
