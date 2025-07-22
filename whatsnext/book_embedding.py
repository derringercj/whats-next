from sentence_transformers import SentenceTransformer

import constants as constant

import json
import re

def load_books():
    # Opening the saved books text file, reading the data, and splitting it on the title delimiter
    with open(constant.BOOKS_TXT_FILENAME, "r") as file:
        text = file.read()
        books = re.split(r'(?=Title:)', text)

    return books

def create_embedding_lookup(books, embeddings):
    i = 0
    book_vector_dict = {}
    for book in books:
        book_vector_dict[book.split("\n")[0]] = embeddings[i].tolist()
        i += 1
    
    return book_vector_dict

def save_dictionary(book_dict):
    with open(constant.BOOKS_EMBEDDING_PAIRS_FILENAME, "w") as file:
        json.dump(book_dict, file, sort_keys=True)
    
def main():
    books = load_books()
    # Generating embeddings for each book string in the text file
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences=books, batch_size=32, show_progress_bar=True)
    print(embeddings.shape)

    # Function to create dictionary storing book name and vector embeddings
    embedding_lookup = create_embedding_lookup(books, embeddings)

    save_dictionary(embedding_lookup)

if __name__ == "__main__":
    main()