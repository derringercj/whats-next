from sentence_transformers import SentenceTransformer

import re

def load_books():
    # Opening the saved books text file, reading the data, and splitting it on the title delimiter
    with open("data/formattedbookobjects.txt", "r") as file:
        text = file.read()
        books = re.split(r'(?=Title:)', text)

    return books
def main():
    books = load_books()
    # Generating embeddings for each book string in the text file
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences=books, batch_size=32, show_progress_bar=True)
    print(embeddings.shape)

if __name__ == "__main__":
    main()