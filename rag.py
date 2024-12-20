from sentence_transformers import SentenceTransformer
import pickle
import numpy as np

# Load titles and abstracts
with open('dictionary_abstracts.pkl', 'rb') as f:
    dictionary_abstracts = pickle.load(f)

abstracts = list(dictionary_abstracts.values())
titles = list(dictionary_abstracts.keys())

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Use a lightweight embedding model

# Embed abstracts
abstract_embeddings = model.encode(abstracts, convert_to_tensor=True)

# Save embeddings for reuse
with open('abstract_embeddings.pkl', 'wb') as f:
    pickle.dump((abstract_embeddings, titles, abstracts), f)

from sentence_transformers.util import semantic_search

def search_papers(query, top_k=20):
    # Load embeddings and data
    with open('abstract_embeddings.pkl', 'rb') as f:
        abstract_embeddings, titles, abstracts = pickle.load(f)
    
    # Encode query
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Retrieve top_k papers
    search_results = semantic_search(query_embedding, abstract_embeddings, top_k=top_k)
    results = []
    for hit in search_results[0]:
        idx = hit['corpus_id']
        results.append((titles[idx], abstracts[idx], hit['score']))
    return results

def format_results(results):
    response = "Here are the most relevant papers:\n"
    for i, (title, abstract, score) in enumerate(results, 1):
        response += f"\n{i}. **{title}** (Score: {score:.2f})\n{abstract[:300]}...\n"
    return response

# Example interactive conversation
conversation_context = []

while True:
    user_query = input("Enter your query (or type 'exit' to quit): ")
    if user_query.lower() == 'exit':
        break
    
    results = search_papers(user_query)
    response = format_results(results)
    print(response)
    
    # Store in conversation context
    conversation_context.append({"query": user_query, "response": response})
