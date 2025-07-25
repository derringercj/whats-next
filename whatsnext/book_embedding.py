from sentence_transformers import SentenceTransformer

import constants as constant

import gzip
import json
import re

def load_books():
    # Opening the saved books text file, reading the data, and splitting it on the title delimiter
    with open(constant.BOOKS_TXT_FILENAME, "r") as file:
        text = file.read()
        books = [book for book in re.split(r'(?=Title:)', text) if book.strip()]

    return books

def create_embedding_lookup(books, embeddings):
    i = 0
    book_vector_dicts = []
    for book in books:
        book_vector = {}
        book_vector["title"] = book.split("\n")[0]
        book_vector["vector"] = embeddings[i].tolist()
        book_vector_dicts.append(book_vector)
        i += 1
    
    return book_vector_dicts

def save_dictionary(book_dict):
    with gzip.open(constant.BOOKS_EMBEDDING_PAIRS_FILENAME, "wb") as file:
        content = []
        for dict in book_dict:
            content.append((json.dumps(dict)+'\n').encode('utf-8'))
        file.writelines(content)
    
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