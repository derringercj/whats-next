from sentence_transformers import SentenceTransformer

import constants as constant
import numpy as np

import faiss
import gzip
import jsonlines

def load_data():
    with jsonlines.Reader(gzip.open(constant.BOOKS_EMBEDDING_PAIRS_FILENAME, "rt")) as reader:
        pass

def main():

    i = 0
    books_db = load_data()
    for book_title in books_db["title"]:
        print(book_title)
        i += 1
        if i == 5:
            break

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Please enter a title:")
    title = input()
    

    # running = True
    # while running:
    #     similarities_list = []
    #     title_similarity_pair = {}
    #     title_embedding = books_db[title]
    #     for book in books_db:
    #         similarity = model.similarity(title_embedding, books_db[book])
    #         title_similarity_pair[title] = similarity
    #         similarities_list.append(title_similarity_pair)



if __name__ == "__main__":
    main()