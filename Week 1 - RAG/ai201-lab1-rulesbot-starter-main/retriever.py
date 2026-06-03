import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Embedding function and ChromaDB client are initialized once at module load.
# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used by app.py during ingestion."""
    return _collection


def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in the vector database.

    This function is already implemented — read through it before moving on.

    _collection.add() takes three parallel lists built from the chunks
    returned by chunk_document():
      - documents : raw text strings — ChromaDB's embedding function converts
                    these to vectors automatically using sentence-transformers
      - metadatas : one dict per chunk, stored alongside the vector so that
                    retrieve() can surface which game a result came from
      - ids       : the unique chunk_id strings used to identify each entry

    You don't generate embeddings manually here — you hand over the text
    and ChromaDB handles the vector math.
    """
    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"game": c["game"]} for c in chunks],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, n_results=N_RESULTS):
    """
    Find the most relevant rule chunks for a user's question.

    TODO — Milestone 2:

    Use _collection.query() to run a semantic search. It takes:
      - query_texts : a list containing your query string
      - n_results   : how many results to return
      - include     : what to return — use ["documents", "metadatas", "distances"]

    Return a list of dicts, each with:
      - "text"     : the chunk text
      - "game"     : the game name (pull this from metadatas)
      - "distance" : the similarity score (lower = more similar for cosine)

    Note: _collection.query() returns nested lists (one per query). You only
    have one query, so you'll want index [0] to get the actual results.
    """
    if _collection.count() == 0:
        return []
    
    results = _collection.query(
        query_texts = [query], # need to wrap in a list, ChromaDB allows us to pass multiple queries at once
        n_results = n_results,
        include = ["documents", "metadatas", "distances"]
    )

    # results["documents"] is a list of lists: [['chunk1 text', 'chunk2 text', ...]]
    # Since we only sent one query, we grab index 0.
    texts = results["documents"][0]
    # same principle applies to metadatas & distances
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # python's zip() function is a really elegant solution to this
    formatted_results = []
    for text, meta, dist in zip(texts, metadatas, distances):
        formatted_results.append({
            "text": text,
            "game": meta["game"],
            "distance": dist
        })


    for chunk in formatted_results:
        print(f"[{chunk['game']}] (dist: {chunk['distance']:.3f}) {chunk['text'][:80].replace("\n","")}...")

    # Your implementation here.
    return formatted_results


if __name__ == "__main__":
    # Ensure the database has been populated first
    if _collection.count() == 0:
        print("Vector database is empty! Please run 'python ingest.py' first.")
    else:
        # Define a sample query
        test_query = "What happens if I roll a 7 in Catan?"
        print(f"\nSearching for: '{test_query}'...\n")
        
        # Call the retrieve function
        results = retrieve(test_query)
        
        # Display the formatted results
        if not results:
            print("No results returned.")
        else:
            for i, result in enumerate(results):
                print(f"Result {i+1} | Game: {result['game']} | Distance: {result['distance']:.4f}")
                print("-" * 50)
                print(result["text"])
                print("-" * 50)
                print()