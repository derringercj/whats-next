from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence = "University of Alabama"

embeddings = model.encode(sentence)

print(embeddings.shape)