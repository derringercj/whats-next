from sentence_transformers import SentenceTransformer

import numpy as np

import jsonlines

def load_data():
    with open("data/blahblahblah.json", "r") as file:
        pass

def main():

    books_db = load_data()

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Please enter a title:")
    title = input()
    
    running = True
    while running:
        pass



if __name__ == "__main__":
    main()