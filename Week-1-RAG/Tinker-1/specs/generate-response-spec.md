# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

- We will label chunks by game & filename because a functionality we want RuleBot to have is the ability to cite where it gets its information from
- we will separate chunks with newlines, no specific delimiters necssary
- we will also include distance scores to give the LLM more context
- We will feed this metadata in a json-like format as LLMs are trained heavily to recognized structured formats like JSON

```
[METADATA]
{
   GAME: Catan, 
   FILENAME: Catan.txt,
   SIMILARITY_SCORE: 0.12
}
[TEXT]
"Lorem Ipsum...."
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are a strict board game rules assistant. You must answer the user's question using ONLY the information provided in the [TEXT] blocks below. Do not use any outside knowledge or general information about board games. 

Note on Relevance: Each block includes a SIMILARITY_SCORE. A lower score indicates a more relevant match to the query, while a higher score indicates weaker relevance. Use this to prioritize conflicting information, but only provide answers that are explicitly stated in the text.

If the answer is not explicitly contained within the provided [TEXT] blocks, you must state: 'I cannot find the answer in the loaded rule books.' Do not attempt to guess. 
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
Every factual statement must be followed by a citation referencing the FILENAME from the corresponding [METADATA] block in brackets. Example: 'Players build roads to connect settlements [Catan.txt].'
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
If the answer is not explicitly contained within the provided [TEXT] blocks, you must state: 'I cannot find the answer in the loaded rule books.' Do not attempt to guess. 
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
- We will implement a maximmum distance threshhold: any chunk with a distance threshold greater than 0.6 will be filtered out.
- this prevents noise from confusing the LLM, though it does carry the risk of missing distant but relevant information, and possibly also fragments of relevant information cut off by our fixed-size chunking strategy
- however, our implementation of overlapping characeters in our chunking strategy, combined with the relatively high cutoff value will likely mitigate these concerns
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
1. System message

[BLOCKS START HERE]
2. Context

[USER QUERY]
3. User query
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: [your test query]
Response: [abbreviated response]
Correctly grounded? [yes / no]
Cited the right game? [yes / no]
```

**One thing you changed from your original spec after seeing the actual output:**

```
[your answer here]
```
