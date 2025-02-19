import streamlit as st
import brain
import random

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'messages' not in st.session_state:
    st.session_state.messages = []

home = False
count = 0

def ayurbot():
    global count
    questions = False
    a = 0
    b = 0
    c = 0

    # Set dark background for the chat interface
    page_bg_dark = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-color: #1E1E1E; /* Dark background */
    color: white; /* Light text */
    }
    [data-testid="stChatInput"] {
    background-color: #2E2E2E; /* Dark input background */
    color: white; /* Light text */
    }
    </style>
    """
    st.markdown(page_bg_dark, unsafe_allow_html=True)

    # Display AyurBot title and description
    st.markdown(
        """
        <h2 style="text-align: center; color: white; font-family: 'Comic sans';">AyurBot</h1>
        <h5 style="text-align: center; color: white;">Discover your Prakruthi using AI based chatbot.</h5>
        """,
        unsafe_allow_html=True
    )

    # Add a Home button to return to the home page
    if st.button("Home"):
        st.session_state.page = 'home'
        st.session_state.messages = []  # Clear chat history
        st.experimental_rerun()  # Rerun the app to go back to the home page

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Send a message"):
        st.session_state.messages.append({"role": "USER", "content": prompt})
        with st.chat_message("USER"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            bot_response = ""
            prompt = prompt.lower()

            if count == 0:
                bot_response = random.choice(brain.questions)
            if count == 1:
                bot_response = brain.questions[1]
            if prompt in brain.c_hi:
                bot_response = "Please answer the following questions honestly and accurately."
            if prompt in brain.c_yes:
                questions = True
            count += 1

            logic(prompt, a, b, c)

            message_placeholder.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

def result(a, b, c):
    if a > b and a > c:
        bot_response = "Congratulations your prakriti is VATA"
    if b > c and b > a:
        bot_response = "Congratulations your prakriti is PITTA"
    if c > a and c > b:
        bot_response = "Congratulations your prakriti is KAPHA"

def logic(user, x, y, z):
    if user in brain.ans_1:
        x += 1
    elif user in brain.ans_2:
        y += 2
    else:
        z += 3
    return user, x, y, z

def main():
    # Set background image for the home page
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://wallpaperaccess.com/full/432582.jpg");
    background-size: cover;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

    # Display AyurBot title and description
    st.markdown(
        """
        <h2 style="text-align: center; color: white; font-family: 'Comic sans';">AyurBot</h1>
        <h5 style="text-align: center; color: white;">Discover your Prakruthi using AI based chatbot.</h5>
        """,
        unsafe_allow_html=True
    )

    # Get Started button
    if st.button("Get Started"):
        st.session_state.page = 'ayurbot'
        st.experimental_rerun()  # Rerun the app to switch to the chat interface

# Page routing
if st.session_state.page == 'home':
    main()

if st.session_state.page == 'ayurbot':
    ayurbot()
