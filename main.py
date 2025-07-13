from sentence_transformers import SentenceTransformer
import pandas as pd
import jsonlines

def filter(obj):
    pass


def main():
    data = []
    with jsonlines.open("goodreads_books.json") as reader:
        for i in range(5):
            print(i)
        


    model = SentenceTransformer("all-mpnet-base-v2")

