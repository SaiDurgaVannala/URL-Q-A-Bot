import google.generativeai as genai
import streamlit as st 
import requests
from bs4 import BeautifulSoup

st.title("🤖 URL ChatBot")

# Reading the Gemini API Key
with open("apikey.txt", "r") as f:
    key = f.read().strip()

# Configuring the API Key
genai.configure(api_key=key) 

# Initializing a Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="""You are a helpful AI ChatBot. You can answer questions based on the content of a given URL including code"""
)

# initializing one,if there is no chat history in session.
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to extract text from a given URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract text from the webpage content
        text = ' '.join([p.get_text() for p in soup.find_all("p")])
        return text
    except Exception as e:
        return f"Error: {e}"

# Displaying the initial message
if "initial_message_displayed" not in st.session_state:
    st.write("Hi, I'm your URL ChatBot! Please provide a URL and ask your question.")
    st.session_state["initial_message_displayed"] = True

# User input: URL and question
url_input = st.text_input("Enter URL:")
question_input = st.text_input("Ask your question:")

# user input for url and question
if url_input and question_input:
    st.write("User:")
    st.write(f"URL: {url_input}")
    st.write(f"Question: {question_input}")
    
    # Extracting text from the URL
    url_text = extract_text_from_url(url_input)
    
    # If text is successfully extracted
    if url_text:
        # Initializing the chat object
        chat = model.start_chat(history=st.session_state["chat_history"])
        
        # Providing the text and question to the model for generating a response
        user_input = f"{url_text}\nQuestion: {question_input}"
        response = chat.send_message(user_input)
        st.write("ChatBot:")
        st.write(response.text)
    else:
        st.write("Failed to extract text from the provided URL. Please enter a valid URL.")


    st.write("Thank you for using the URL ChatBot! 😊")
    st.info("Please update the question if you want to ask questions from same url")
    st.info("Please refresh the page if you want to enter another url and question")