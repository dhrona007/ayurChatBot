import streamlit as st
import brain
import random

home = False
count = 0

def ayurbot():
    global count
    questions = False
    a = 0
    b = 0
    c = 0

    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://wallpaperaccess.com/full/432582.jpg");
    background-size: cover;
    }
    </style>
    """
    st.markdown(
        page_bg,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h2 style="text-align: center; color: white; font-family: 'Comic sans';">AyurBot</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h5 style="text-align: center; color: white;">Discover your Prakruthi using AI based chatbot.</h5>
        """,
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://wallpaperaccess.com/full/432582.jpg");
    background-size: cover;
    }
    </style>
    """
    st.markdown(
        page_bg,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h2 style="text-align: center; color: white; font-family: 'Comic sans';">AyurBot</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h5 style="text-align: center; color: white;">Discover your Prakruthi using AI based chatbot.</h5>
        """,
        unsafe_allow_html=True
    )

    if st.button("Get Started"):
        st.session_state.page = 'ayurbot'

if 'page' not in st.session_state:
    st.session_state.page
