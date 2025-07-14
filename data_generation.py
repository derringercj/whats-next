from urllib.request import urlretrieve
from sentence_transformers import SentenceTransformer

import pandas as pd

import os
import jsonlines
import gzip

BOOKS_URL = "https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/goodreads_books.json.gz"
BOOKS_FILENAME = "books.json.gz"
AUTHORS_URL = "https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/goodreads_book_authors.json.gz"
AUTHORS_FILENAME = "authors.json.gz"
GENRES_URL = "https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/goodreads_book_genres_initial.json.gz"
GENRES_FILENAME = "extracted_genres.json.gz"
DIRECTORY_NAME = "data"

def download_data():
    try:
        os.mkdir(DIRECTORY_NAME)
        print(f"Directory '{DIRECTORY_NAME}' CREATED SUCCESSFULLY.")
    except FileExistsError:
        print(f"Directory '{DIRECTORY_NAME}' already exists. Continuing...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        urlretrieve(BOOKS_URL, BOOKS_FILENAME)
        urlretrieve(AUTHORS_URL, AUTHORS_FILENAME)
        urlretrieve(GENRES_URL, GENRES_FILENAME)


def filter(obj):
    # Saving only relevant information from each object
    title = obj.get("title")
    author = obj.get("authors")
    if type(author) == list:
        author = ", ".join(author.get("author_id") for author in obj["authors"])
    date = obj.get("publication_year")
    length = obj.get("num_pages")
    desc = obj.get("description")

    # Creating new object with only wanted info
    new_object = {
        "title": title,
        "author": author,
        "year": date,
        "num_pages": length,
        "description": desc
    }

    # Returning filtered object
    return new_object

def format_data(objects_list):
    formatted_strings = []

    # Using information in each object, create contextual string for generating vector embedding
    for object in objects_list:
        compiled_string = "Title: " + object.get("title") + "\nAuthor: " + object.get("author") + "\nPublication Year: " + object.get("year") + \
                            "\nPage Length: " + object.get("num_pages") + "\nSynopsis: " + object.get("description") + "\n"
        formatted_strings.append(compiled_string)
    
    # Return list of formatted strings
    return formatted_strings

def main():
    # Open books json, and filter each object before saving it to the objects list
    with jsonlines.Reader(gzip.open(BOOKS_FILENAME, mode="rt")) as reader:
        objects = []
        for obj in reader:
            try:
                # Disregard outlier books
                if(int(obj.get("ratings_count")) < 100):
                    continue
            except:
                # If ratings_count is empty, skip
                continue
            filtered_object = filter(obj)
            objects.append(filtered_object)    

    formatted_strings = format_data(objects)    

    print(formatted_strings[0])

    with jsonlines.Reader(gzip.open(AUTHORS_FILENAME, mode="rt")) as reader:
        for obj in reader:
            print(obj.keys())
            break

if __name__ == "__main__":
    main()

