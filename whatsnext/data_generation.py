from urllib.request import urlretrieve

import constants as constant
import pandas as pd

import gzip
import jsonlines
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
        os.chdir(constant.DIRECTORY_NAME)

    except Exception as e:
        print(f"An error occurred: {e}")

def is_complete_data(obj):
    # Removing books that are missing any of the required fields
    required_fields = ["title", "authors", "publication_year", "num_pages", "description"]
    if any(not obj.get(field) for field in required_fields):
        return False
    else:
        return True

def load_books():
    print("Loading books...")
    # Open books json, and filter each object before saving it to the objects list
    with jsonlines.Reader(gzip.open(constant.BOOKS_FILENAME, mode="rt")) as reader:
        objects = []
        for book_obj in reader:
            try:
                # Disregard outlier books
                if(int(book_obj.get("ratings_count")) < 100) or (not (is_complete_data(book_obj))):
                    continue
            except:
                # If ratings_count is empty, skip
                continue

            # Call function to filter out unnecessary book info and add that filtered object to list
            filtered_object = filter_book_object(book_obj)
            objects.append(filtered_object)
    
    return objects

def filter_book_object(obj):
    # Saving only relevant information from each object
    title = obj.get("title")
    author = obj.get("authors")
    if type(author) == list:
        author = ", ".join(author.get("author_id") for author in obj["authors"])
    date = obj.get("publication_year")
    length = obj.get("num_pages")
    desc = obj.get("description")

    # Need to save book id for genre assignment later
    id = obj.get("book_id")

    # Creating new object with only wanted info
    new_object = {
        "title": title,
        "author": author,
        "year": date,
        "num_pages": length,
        "description": desc,
        "book_id": id
    }

    # Returning filtered object
    return new_object

def add_author_and_genre_names(book_objects):
    print("Adding author names and genre tags to books...")
    
    author_lookup = {}
    # For each author in author file, add them to a dictionary indexed by author id.
    with jsonlines.Reader(gzip.open(constant.AUTHORS_FILENAME, mode="rt")) as reader:
        for author in reader:
            author_lookup[author["author_id"]] = author["name"]

    genre_lookup = {}
    with jsonlines.Reader(gzip.open(constant.GENRES_FILENAME, mode="rt")) as reader:
        for genre in reader:
            genre_lookup[genre["book_id"]] = genre["genres"]
    # For each book in book_objects list, retreive author id from book, then lookup that author's name and add it to book object
    for book in book_objects:
        author_ids = book.get("author")
        if author_ids:
            book["author"] = ", ".join(author_lookup.get(author_id, "Unknown") for author_id in author_ids.split(", "))
        
        book_id = book.get("book_id")
        if book_id:
            genres = ", ".join(f"{value}" for value in genre_lookup.get(book_id))
            book.update({"genres": genres})

def format_data(objects_list):
    formatted_strings = []

    # Using information in each object, create contextual string for generating vector embedding
    for object in objects_list:        
        compiled_string = (
            f"Title: {object.get("title")}\n"
            f"Author: {object.get("author")}\n"
            f"Publication Year: {object.get("year")}\n"
            f"Page Length: {object.get("num_pages")}\n"
            f"Genres: {object.get("genres")}\n"
            f"Synopsis: {object.get("description")}\n"
        )

        formatted_strings.append(compiled_string)
    
    # Return list of formatted strings
    return formatted_strings

def save_data(strings):
    # Writing strings
    with open(constant.BOOKS_TXT_FILENAME, "w") as file:
        file.writelines(strings)

def main():
    download_data()
    books = load_books()

    # Replace author id in each book object with their actual name
    add_author_and_genre_names(books)

    # Generate list of strings represnting each book object
    books_strings = format_data(books)    

    save_data(books_strings)
            
if __name__ == "__main__":
    main()