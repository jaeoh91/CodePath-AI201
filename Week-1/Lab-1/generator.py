from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

DISTANCE_THRESHOLD = 0.6

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # 1. Filter low-relevance chunks (Hard Distance Threshold = 0.6)
    filtered_chunks = [c for c in retrieved_chunks if c["distance"] < DISTANCE_THRESHOLD]

    # If no chunks survive the distance threshold filter
    if not filtered_chunks:
        return "I cannot find the answer in the loaded rule books."

    # 2. Context Formatting (JSON-like metadata + text blocks)
    context_blocks = []
    for i, chunk in enumerate(filtered_chunks):
        block = (
            f"[METADATA]\n"
            f"{{\n"
            f"   \"GAME\": \"{chunk['game']}\",\n"
            f"   \"FILENAME\": \"{chunk.get('filename', 'unknown')}\",\n"
            f"   \"SIMILARITY_SCORE\": {chunk['distance']:.4f}\n"
            f"}}\n"
            f"[TEXT]\n"
            f"\"{chunk['text']}\""
        )
        context_blocks.append(block)

    context_string = "\n\n".join(context_blocks)

    # 3. System Prompt Construction
    system_prompt = (
        "You are a strict board game rules assistant. You must answer the user's question "
        "using ONLY the information provided in the [TEXT] blocks below. Do not use any "
        "outside knowledge or general information about board games.\n\n"
        "Note on Relevance: Each block includes a SIMILARITY_SCORE. A lower score indicates "
        "a more relevant match to the query, while a higher score indicates weaker relevance. "
        "Use this to prioritize conflicting information, but only provide answers that are "
        "explicitly stated in the text.\n\n"
        "Every factual statement must be followed by a citation referencing the FILENAME "
        "from the corresponding [METADATA] block in brackets. Example: 'Players build roads "
        "to connect settlements [Source: Catan.txt].'\n\n"
        "If the answer is not explicitly contained within the provided [TEXT] blocks, "
        "you must state: 'I cannot find the answer in the loaded rule books.' Do not attempt to guess."
    )

    # 4. Message Structure (System message + User message with context and query)
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user", 
            "content": f"CONTEXT:\n{context_string}\n\nQUESTION: {query}"
        }
    ]
    
    #print(messages)

    try:
        response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0  # Set to 0 for maximum grounding and consistency
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating the response: {str(e)}"
