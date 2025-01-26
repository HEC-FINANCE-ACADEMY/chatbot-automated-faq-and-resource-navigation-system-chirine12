import json
import os
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from langdetect import detect
import ollama

# Constants
JSON_PATH = "dataset.json"
MODEL = "minicpm-v"
ANNOY_INDEX_PATH = "annoy_index.ann"  # Path to save the Annoy index
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # Embedding model name

# Initialize SentenceTransformer model for embeddings
embedder = SentenceTransformer(EMBEDDING_MODEL)

# Function to load data from JSON file
def load_json_data(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"The JSON file '{json_path}' was not found.")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('dataset', [])  # Safely handle missing 'dataset' key

# Function to generate query embeddings
def generate_query_embedding(query):
    return embedder.encode(query, convert_to_numpy=True)  # Return NumPy array

# Function to build embeddings for the dataset
def build_embeddings(data):
    if not data:
        raise ValueError("The dataset is empty or invalid.")
    
    text_chunks = [f"Q: {item['question']} A: {item['answer']}" for item in data]
    embeddings = embedder.encode(text_chunks, convert_to_numpy=True)
    return embeddings, text_chunks

# Function to store embeddings in Annoy
def store_embeddings_in_annoy(embeddings, num_trees=10):
    dimension = embeddings.shape[1]
    annoy_index = AnnoyIndex(dimension, metric='euclidean')

    for i, embedding in enumerate(embeddings):
        annoy_index.add_item(i, embedding)

    annoy_index.build(num_trees)
    return annoy_index

# Function to load or build the Annoy index
def load_or_build_index(json_path, annoy_index_path):
    if os.path.exists(annoy_index_path):
        print("Loading existing Annoy index...")
        data = load_json_data(json_path)
        embeddings, _ = build_embeddings(data)
        dimension = embeddings.shape[1]
        annoy_index = AnnoyIndex(dimension, metric='euclidean')
        annoy_index.load(annoy_index_path)
        return annoy_index, data
    else:
        print("Building new Annoy index...")
        data = load_json_data(json_path)
        embeddings, chunks = build_embeddings(data)
        annoy_index = store_embeddings_in_annoy(embeddings)
        annoy_index.save(annoy_index_path)
        return annoy_index, chunks

# Function to search for relevant context
def search_relevant_context_with_annoy(query, annoy_index, chunks):
    query_embedding = generate_query_embedding(query)
    nearest_neighbor_idx = annoy_index.get_nns_by_vector(query_embedding, n=1, include_distances=False)
    return chunks[nearest_neighbor_idx[0]]

# Function to detect language
def detect_language(text):
    try:
        return detect(text)  # Returns 'en' for English, 'fr' for French, etc.
    except Exception as e:
        print(f"Language detection error: {e}")
        return "unknown"

# Function to build the prompt dynamically
def build_prompt_with_context(query: str, index, chunks) -> dict:
    relevant_context = search_relevant_context_with_annoy(query, index, chunks)
    language = detect_language(query)
    print(f"Detected language for query '{query}': {language}")  
    
    if language == "en":
        translation_instruction = "Translate the answer to English."
    elif language == "fr":
        translation_instruction = "Répondez en français."
    else:
        translation_instruction = "Répondez dans la langue du contexte ou détectée."

    messages = [
        {
            "role": "user",
            "content": (
                "You are an expert AI assistant that will answer the following query strictly based on the context provided. "
                "Do not use any external knowledge or make assumptions beyond the provided content. "
                "Your answer should strictly reference and use the provided context."
            )
        },
        {
            "role": "system",
            "content": f"Relevant context from the dataset: {relevant_context}"
        },
        {
            "role": "user",
            "content": query
        },
        {
            "role": "system",
            "content": translation_instruction
        }
    ]
    
    return {
        "model": MODEL,
        "messages": messages
    }

# Function to refine the answer based on feedback
def refine_answer(query, index, chunks, previous_context):
    messages = [
        {
            "role": "user",
            "content": (
                "You are an AI assistant refining a response based on user feedback. "
                "The previous answer was unsatisfactory. Please provide a clearer and more detailed response."
            )
        },
        {
            "role": "system",
            "content": f"Previous context: {previous_context}"
        },
        {
            "role": "user",
            "content": query
        }
    ]
    
    return {
        "model": MODEL,
        "messages": messages
    }

# Function to recommend a program based on interests
def recommend_program_based_on_interests(interests):
    # Load the dataset to find the program recommendation
    data = load_json_data(JSON_PATH)
    for item in data:
        if item.get("id") == 76:  # The entry for program recommendation
            for option in item["follow_up"]["options"]:
                if option["interest"].lower() in interests.lower():
                    return option["recommended_program"], option["description"]
    return None, None

# Function to handle schedule-related queries
def handle_schedule_query():
    print("Schedule-related functionality is not implemented yet.")

# Main function
def main():
    print("Welcome to the AI Chat Assistant with JSON dataset support!")
    print(f"Using JSON file: {JSON_PATH}")
    print("Type 'exit' to quit the chat.")

    try:
        index, chunks = load_or_build_index(JSON_PATH, ANNOY_INDEX_PATH)
        print("Index loaded/built and ready for searching relevant context!")
    except Exception as e:
        print(f"Error during initialization: {e}")
        return

    print("\nInteractive Chat Started! Ask your questions below.")

    while True:
        query = input("\nYour Query: ").strip()
        if query.lower() == "exit":
            print("Goodbye!")
            break

        try:
            # Check if the query is about finding a suitable program
            if "programme me convient" in query.lower() or "suitable program" in query.lower():
                print("Je peux vous aider à trouver le programme qui correspond le mieux à vos intérêts. Pouvez-vous me dire ce qui vous passionne ou les domaines dans lesquels vous aimeriez travailler ?")
                interests = input("\nVos intérêts: ").strip()
                program, description = recommend_program_based_on_interests(interests)
                if program:
                    print(f"\nEn fonction de vos intérêts, je vous recommande le programme en *{program}*. {description}")
                else:
                    print("Désolé, je n'ai pas trouvé de programme correspondant à vos intérêts.")
            
            else:
                # Get the initial response
                prompt = build_prompt_with_context(query, index, chunks)
                response = ollama.chat(**prompt)
                answer = response['message']['content']
                
                print("\nAI Response:")
                print(answer)

                # Get user feedback
                feedback = input("\nWas this answer helpful? (yes/no): ").strip().lower()
                if feedback == "no":
                    print("Let me refine the answer for you.")
                    refined_prompt = refine_answer(query, index, chunks, prompt['messages'][1]['content'])
                    refined_response = ollama.chat(**refined_prompt)
                    print("\nRefined AI Response:")
                    print(refined_response['message']['content'])

        except Exception as e:
            print(f"Error during query processing: {e}")

if __name__ == "__main__":
    main()