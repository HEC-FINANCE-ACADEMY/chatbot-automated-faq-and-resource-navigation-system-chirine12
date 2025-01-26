import json
import os
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from langdetect import detect
import ollama
import speech_recognition as sr
import pyttsx3

# Constants
JSON_PATH = "dataset.json"  # Path to the JSON file
MODEL = "minicpm-v"  # Change to the actual model you're using
ANNOY_INDEX_PATH = "annoy_index.ann"  # Path to save/load the Annoy index

# Initialize SentenceTransformer model for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """
    Converts text to speech and prints the text to the console.
    """
    print(f"Assistant: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

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
    print(f"Detected language for query '{query}': {language}")  # Debug log
    
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

# Function to get audio input
def get_audio_input():
    with sr.Microphone() as source:
        speak("Please say something...")
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        audio = recognizer.listen(source)
        print("Processing...")
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("I couldn't understand what you said. Please try again.")
        except sr.RequestError as e:
            speak(f"Speech recognition service is unavailable: {e}")
        return None

def main():
    print("Welcome to the AI Chat Assistant with Speech and JSON dataset support!")
    speak("Welcome to the AI Chat Assistant with Speech and JSON dataset support!")

    try:
        index, chunks = load_or_build_index(JSON_PATH, ANNOY_INDEX_PATH)
        speak("Index loaded and ready!")
    except Exception as e:
        speak(f"Error during initialization: {e}")
        return

    while True:
        print("\nPlease speak your query or type 'exit' to quit.")
        query = get_audio_input()  # Get user input via microphone
        if not query:
            continue

        if "exit" in query.lower():
            speak("Goodbye!")
            break

        prompt = build_prompt_with_context(query, index, chunks)
        response = ollama.chat(**prompt)
        answer = response['message']['content']
        speak(f"The AI says: {answer}")

if __name__ == "__main__":
    main()