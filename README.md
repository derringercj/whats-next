# book-rec-engine

## Why?
Two things about me: I love books and I love reading. As such, I am always revisiting the question of "What to read next?" as my tastes evolve and my interests bounce from one subject to another. I use tools like Goodreads as much as I use actual social media sites. But as most people know, Goodreads sucks. This is for a myriad of reasons, but most importantly to this project, their recommendation system is lousyyyyyy. Their are so many advancements in the field of ML and NLP that have improved the efficacy of recommendation systems across the media spectrum. My goal is to use one of these techniques to implement a new and more robust algorithm for recommending new books to read. 

## How?
This program leverages the UCSD Book Graph Goodreads dataset to represent a vast array of novels acorss all genres, centuries, and authors. This information is aggregated and stored in a vector space via embedding generation. This allows us to more adeptly examine and identify the similarities between books in regards to style, semantics, and feeling, providing recommendations far less surface level than other availble recommendation services currently available.