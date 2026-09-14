import streamlit as st
import nltk
import re

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download("stopwords", quiet=True)

# Page settings
st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 FAQ Chatbot")
st.write("Ask a question about Python. The chatbot will find the most similar FAQ answer.")

# FAQ dataset
faqs = [
    {
        "question": "What is Python?",
        "answer": "Python is a high-level, interpreted programming language used for web development, AI, data science, and automation."
    },
    {
        "question": "What are the features of Python?",
        "answer": "Python is simple, readable, open-source, portable, dynamically typed, and supports object-oriented programming."
    },
    {
        "question": "How do I install Python?",
        "answer": "You can install Python from the official Python website: https://www.python.org/downloads/"
    },
    {
        "question": "What is a variable in Python?",
        "answer": "A variable is a name used to store a value in Python."
    },
    {
        "question": "What is a list in Python?",
        "answer": "A list is an ordered and changeable collection that can store multiple values."
    },
    {
        "question": "What is a function?",
        "answer": "A function is a reusable block of code designed to perform a particular task."
    },
    {
        "question": "What is artificial intelligence?",
        "answer": "Artificial Intelligence is the ability of machines to perform tasks that normally require human intelligence."
    },
    {
        "question": "What is machine learning?",
        "answer": "Machine learning is a branch of AI that allows computers to learn patterns from data."
    },
    {
        "question": "What is Streamlit?",
        "answer": "Streamlit is a Python library used to create interactive web applications quickly."
    },
    {
        "question": "How can I learn Python?",
        "answer": "You can learn Python by studying basic syntax, variables, loops, functions, and by practicing small projects."
    }
]

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    words = text.split()

    stop_words = set(stopwords.words("english"))
    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# Prepare FAQ questions
faq_questions = [
    preprocess_text(faq["question"])
    for faq in faqs
]

# Create TF-IDF vectors
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)


# Find best matching answer
def get_answer(user_question):
    cleaned_question = preprocess_text(user_question)

    user_vector = vectorizer.transform([cleaned_question])

    similarity_scores = cosine_similarity(
        user_vector,
        faq_vectors
    )

    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_match_index]

    # Minimum similarity threshold
    if best_score < 0.15:
        return (
            "Sorry, I could not find a suitable answer. "
            "Please ask a question related to Python or AI."
        )

    return faqs[best_match_index]["answer"]


# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input
user_question = st.chat_input("Ask your question here...")

if user_question:
    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.write(user_question)

    # Get chatbot answer
    answer = get_answer(user_question)

    # Display chatbot answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.write(answer)