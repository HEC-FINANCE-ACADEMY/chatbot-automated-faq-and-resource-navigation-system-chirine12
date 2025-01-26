AI Chat Assistant using specific dataset
:
This project implements an AI-powered chat assistant that uses a JSON dataset to provide context-aware responses. The system leverages Sentence Transformers for generating embeddings, Annoy for efficient similarity search, and Ollama for generating responses. Below is a detailed explanation of the code and its functionality.


Table of Contents
Overview

Dependencies

Code Structure

Key Functions

How It Works

Usage

Future Improvements


Overview :
The AI Chat Assistant is designed to:

Load a dataset from a JSON file.

Generate embeddings for the dataset using a pre-trained Sentence Transformer model.

Use Annoy to build an index for fast similarity search.

Detect the language of the user's query.

Provide context-aware responses using Ollama.

Refine responses based on user feedback.

Recommend programs based on user interests.


Dependencies
The following Python libraries are required to run this project:

sentence-transformers: For generating embeddings.

annoy: For building and querying the similarity index.

langdetect: For detecting the language of the user's query.

ollama: For generating responses using a language model.

json: For loading the dataset.

os: For file path operations.

Install the dependencies using:




Code Structure
The code is organized into the following sections:

Constants: Configuration variables like file paths and model names.

Embedding Model Initialization: Loads the Sentence Transformer model.

Helper Functions: Functions for loading data, generating embeddings, and managing the Annoy index.

Core Functions: Functions for searching relevant context, detecting language, building prompts, and refining responses.

Main Function: Handles user interaction and orchestrates the workflow.


Key Functions
1. load_json_data(json_path)
Loads the dataset from a JSON file.

Handles missing files or invalid JSON gracefully.

Returns the dataset key from the JSON file.

2. generate_query_embedding(query)
Generates embeddings for the user's query using the Sentence Transformer model.

Returns a NumPy array representing the query embedding.

3. build_embeddings(data)
Combines questions and answers from the dataset into text chunks.

Generates embeddings for all text chunks.

Returns embeddings and the corresponding text chunks.

4. store_embeddings_in_annoy(embeddings)
Builds an Annoy index for the embeddings.

Uses Euclidean distance as the metric for similarity search.

Returns the Annoy index.

5. load_or_build_index(json_path, annoy_index_path)
Loads an existing Annoy index if available.

Otherwise, builds a new index and saves it to disk.

6. search_relevant_context_with_annoy(query, annoy_index, chunks)
Finds the most relevant context for a query using the Annoy index.

Returns the closest matching text chunk.

7. detect_language(text)
Detects the language of the input text using langdetect.

Handles errors gracefully and returns "unknown" if detection fails.

8. build_prompt_with_context(query, index, chunks)
Builds a prompt for Ollama using the relevant context and detected language.

Includes instructions for translation if the query is in a non-English language.

9. refine_answer(query, index, chunks, previous_context)
Refines the response based on user feedback.

Uses the previous context to generate a clearer and more detailed answer.

10. recommend_program_based_on_interests(interests)
Recommends a program based on the user's interests.

Searches the dataset for a matching program and description.

11. main()
Orchestrates the chat assistant workflow.

Handles user input, generates responses, and refines answers based on feedback.

How It Works
Initialization:

The system loads the dataset and builds or loads the Annoy index for embeddings.

User Interaction:

The user enters a query.

The system detects the language of the query.

Context Search:

The query is converted into an embedding.

The Annoy index is used to find the most relevant context from the dataset.

Response Generation:

A prompt is built using the relevant context and language-specific instructions.

Ollama generates a response based on the prompt.

Feedback and Refinement:

The user provides feedback on the response.

If the response is unsatisfactory, the system refines the answer using the previous context.

Program Recommendation:

If the query is about finding a suitable program, the system recommends a program based on the user's interests.

Usage
Prepare the Dataset:Ensure the dataset is stored in a JSON file (dataset.json) with the following structure:

Run the Script:

Execute the script:
python rag.py

Interact with the Chat Assistant:
Enter your queries in the chat interface.
Type exit to quit the chat.




Sentiment Analysis & Question Classification Dashboard for IHEC
Overview
This project aims to provide an intelligent dashboard that classifies student queries and analyzes the sentiment of student feedback in real-time. By integrating a pre-trained BART-large-MNLI model, the system classifies student questions into predefined categories, and analyzes whether their responses are satisfied or not satisfied. The system helps universities, such as IHEC, gain valuable insights into the most common topics students inquire about and how they feel about the answers they receive.

Features
Zero-Shot Question Classification: The system classifies student queries into predefined categories such as:

Schedule
Registration
Course Content
Technical Support
Institutional Information
Programs and Courses
Student Life
Admissions
Technology and Facilities
Other
Sentiment Analysis of Responses: After each interaction, students provide feedback on whether they are satisfied with the answer. The system classifies these responses into satisfied or not satisfied categories to gauge the quality of the chatbot's performance.

Interactive Dashboards:

Pie Chart: Displays the distribution of classified questions across various categories.
Bar Chart: Shows sentiment distribution (satisfied vs not satisfied) based on student feedback.
Requirements
Python 3.7+
transformers library (for using pre-trained NLP models)
matplotlib (for visualizing data)
json (for storing classified data)
Install Dependencies
To set up the project, install the required libraries using pip:

bash
Copier
pip install transformers matplotlib
Usage
1. Running the Dashboard
Run the script to classify student questions and analyze sentiment:

bash
Copier
python sentiment_analysis_dashboard.py
This will:

Classify sample questions into predefined categories.
Analyze sentiment feedback (satisfied or not satisfied) from students.
Generate pie and bar charts to visualize the classification and sentiment distribution.
2. Interpreting the Output
Pie Chart: Displays the distribution of categorized questions. Each slice represents a different category, and the size of the slice corresponds to the number of questions in that category.

Bar Chart: Visualizes the sentiment of student feedback. It shows how many students are satisfied or not satisfied with the chatbot responses.

3. Modifying the Data
You can modify the questions and feedback variables in the script to include your own set of questions and responses. Just replace the sample content with new data.

4. Output Files
The classified data (i.e., the questions with their respective predicted categories) is saved in a file called classified_questions.json.
How It Works
Question Classification
The system uses the facebook/bart-large-mnli model from Hugging Face’s Transformers library. This model is a pre-trained BART (Bidirectional and Auto-Regressive Transformers) model optimized for zero-shot classification tasks. Zero-shot classification means the model can classify input data into categories it wasn't explicitly trained on by leveraging natural language inference.

Sentiment Analysis
The sentiment of feedback (whether students are satisfied or not with the chatbot’s response) is analyzed using the same BART model, fine-tuned to classify feedback into two categories: satisfied and not satisfied.

Data Visualization
The system generates:

A pie chart for showing the distribution of classified questions.
A bar chart for displaying the sentiment analysis results.
Potential Enhancements
Real-time Feedback Integration: Integrate the sentiment analysis directly into a chatbot interface where students can provide feedback after each query.
Extended Feedback Categories: Beyond just "satisfied" and "not satisfied," additional sentiment categories (like "neutral" or "mixed feelings") could be added for more detailed feedback analysis.
Larger Dataset: Use a larger and more diverse dataset to further train and optimize the model for better accuracy in specific areas (such as local education systems).
Contributing
If you'd like to contribute to the project:

Fork the repository
Create a new branch (git checkout -b feature-branch)
Make your changes
Commit the changes (git commit -m 'Added new feature')
Push to your fork (git push origin feature-branch)
Open a pull request with a description of the changes
License
This project is licensed under the MIT License.