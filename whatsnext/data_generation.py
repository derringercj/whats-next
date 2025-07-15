from sentence_transformers import SentenceTransformer
from urllib.request import urlretrieve

import constants as constant
import pandas as pd

import bisect
import gzip
import jsonlines
import operator
import os



def download_data():
    # If data folder does not exist, create it and download the necessary json.gz files into it
    try:
        os.mkdir(constant.DIRECTORY_NAME)
        print(f"Directory '{constant.DIRECTORY_NAME}' CREATED SUCCESSFULLY.")
        
        print("Beginning Data Download")
        urlretrieve(constant.BOOKS_URL, constant.BOOKS_FILENAME)
        print("Books Dataset Downloaded")
        
        urlretrieve(constant.AUTHORS_URL, constant.AUTHORS_FILENAME)
        print("Authors Dataset Downloaded")
        
        urlretrieve(constant.GENRES_URL, constant.GENRES_FILENAME)
        print("Genres Dataset Downloaded")

    # Otherwise continue with program as normal
    except FileExistsError:
        print(f"Directory '{constant.DIRECTORY_NAME}' already exists. Continuing...")
    except Exception as e:
        print(f"An error occurred: {e}")

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
    download_data()
    
    # Open books json, and filter each object before saving it to the objects list
    with jsonlines.Reader(gzip.open(constant.BOOKS_FILENAME, mode="rt")) as reader:
        objects = []
        for book_obj in reader:
            try:
                # Disregard outlier books
                if(int(book_obj.get("ratings_count")) < 100):
                    continue
            except:
                # If ratings_count is empty, skip
                continue
            filtered_object = filter(book_obj)
            objects.append(filtered_object)    

    # Sorting our objects based on the value of the author_id, making replacement with author name easier
    sorted_objects = sorted(objects, key=lambda x: x.get("authors", ""))
    with jsonlines.Reader(gzip.open(constant.AUTHORS_FILENAME, mode="rt")) as reader:
        for author_obj in reader:
            # Returns the leftmost occurrence of the author_id in the books dataset of the current author object
            index = bisect.bisect_left(sorted_objects, author_obj.get("name"))
            author_name = author_obj.get("name")

            
            

if __name__ == "__main__":
    main()

