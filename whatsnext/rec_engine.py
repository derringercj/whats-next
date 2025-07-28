
import constants as constant
import numpy as np

import faiss
import gzip
import jsonlines

def load_data():
    with jsonlines.Reader(gzip.open(constant.BOOKS_EMBEDDING_PAIRS_FILENAME, "rt")) as reader:
        pairs = []
        # For each embedding, populate a vector pair to append to the list of pairs
        for pair in reader:
            title_vector_pair = {}
            title_vector_pair["title"] = pair.get("title")
            title_vector_pair["vector"] = pair.get("vector")
            pairs.append(title_vector_pair)
        
        return pairs

def generate_index(books_db):
    # Isolating our book titles and their embeddings from each dictionary
    embeddings = np.array([book["vector"] for book in books_db], dtype = "float32")
    titles = [book["title"] for book in books_db]
    
    # Dimensionality of our embedding vectors and number of nearest neighbors to return
    dim = embeddings.shape[1]
    
    # Creating our Flat Index with Inner Product similarity calculations, then returning the index
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    return index, titles

def user_prompt():
    # Prompting user for information related to search
    print("How many books are you looking for today?")
    k = int(input())
    
    print("Please enter a title:")
    query_title = input()
    query_title = "Title: " + query_title
    
    return query_title, k

def search(query_title, books_db, index, k):
    # Retreiving the query embedding from the user's selected book
    print(f"Searching for books similar to {query_title}")
    query_embedding = None
    for book in books_db:
        if book["title"] == query_title:
            query_embedding = book["vector"]

    if query_embedding is None:
        raise ValueError(f"Book '{query_title}' not found in dataset")
    

    # Creating np array of our query's embedding
    query = np.array([query_embedding], dtype="float32")

    # Performing a search of our index with our query embedding, returning k nearest neighbors, then returning the scores and indicies
    scores, indicies = index.search(query, k)
    return scores, indicies

def compile_results(indicies, scores, titles, k):
    # Compiling our results into a user-readable list then returning the list
    results = []
    for i in range(k):
        index = indicies[0, i]
        score = scores[0, i]
        title = titles[index]
        results.append((title, score))

    return results

def main():
    print("loading data")
    books_db = load_data()
    
    index, titles = generate_index(books_db)
    
    query_title, k = user_prompt()

    scores, indicies = search(query_title, books_db, index, k)

    results = compile_results(indicies, scores, titles, k)

    # Printing our compiled results
    for i, (title, score) in enumerate(results):
        print(f"{i+1}. {title} (similarity: {score:.6f})")


if __name__ == "__main__":
    main()