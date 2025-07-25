from sentence_transformers import SentenceTransformer

import constants as constant
import numpy as np

import faiss
import gzip
import jsonlines

def load_data():
    with jsonlines.Reader(gzip.open(constant.BOOKS_EMBEDDING_PAIRS_FILENAME, "rt")) as reader:
        pairs = []
        for pair in reader:
            title_vector_pair = {}
            title_vector_pair["Title"] = pair.get("title")
            title_vector_pair["Vector"] = pair.get("vector")
            pairs.append(title_vector_pair)
        
        print(len(pairs))
        return pairs

def main():

    books_db = load_data()

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Please enter a title:")
    title = input()
    
if __name__ == "__main__":
    main()