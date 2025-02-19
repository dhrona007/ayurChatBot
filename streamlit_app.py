import streamlit as st
import brain
import random

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'messages' not in st.session_state:
    st.session_state.messages = []

if "count" not in st.session_state:
    st.session_state.count = 0
if "a" not in st.session_state:
    st.session_state.a = 0
if "b" not in st.session_state:
    st.session_state.b = 0
if "c" not in st.session_state:
    st.session_state.c = 0

# Function to calculate Prakriti
def logic(user, x, y, z):
    if user in brain.ans_1:
        x += 1
    elif user in brain.ans_2:
        y += 2
    else:
        z += 3
    return x, y, z

# Function to display the result
def result(a, b, c):
    if a > b and a > c:
        return "Congratulations, your Prakriti is **VATA**."
    elif b > c and b > a:
        return "Congratulations, your Prakriti is **PITTA**."
    else:
        return "Congratulations, your Prakriti is **KAPHA**."

def ayurbot():
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
        st.session_state.count = 0  # Reset question count
        st.session_state.a = 0  # Reset VATA score
        st.session_state.b = 0  # Reset PITTA score
        st.session_state.c = 0  # Reset KAPHA score

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Send a message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            bot_response = ""
            prompt = prompt.lower()

            # Logic for bot responses
            if st.session_state.count == 0:
                bot_response = random.choice(brain.questions)
            elif st.session_state.count == 1:
                bot_response = brain.questions[1]
            elif prompt in brain.c_hi:
                bot_response = "Please answer the following questions honestly and accurately."
            elif prompt in brain.c_yes:
                bot_response = "Great! Let's continue."
            
            # Update Prakriti scores
            st.session_state.a, st.session_state.b, st.session_state.c = logic(
                prompt, st.session_state.a, st.session_state.b, st.session_state.c
            )
            st.session_state.count += 1

            # Display bot response
            message_placeholder.markdown(bot_response)
        
        # Add bot response to session state
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display the result if all questions are answered
    if st.session_state.count >= len(brain.questions):
        with st.chat_message("assistant"):
            st.markdown(result(st.session_state.a, st.session_state.b, st.session_state.c))

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

# Page routing
if st.session_state.page == 'home':
    main()

if st.session_state.page == 'ayurbot':
    ayurbot()
