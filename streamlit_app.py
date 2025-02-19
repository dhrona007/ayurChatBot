import streamlit as st
import brain
import random

def main():
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    
    if not st.session_state.chat_started:
        show_home()
    else:
        ayurbot()

def show_home():
    st.markdown(
        """
        <style>
        .body {
            background-image: url("https://wallpaperaccess.com/full/432582.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            color: white;
            height: 100vh;
            text-align: center;
        }
        .getStartedButton {
            background-color: transparent;
            color: white;
            border-color: rgb(0, 158, 0);
            margin-top: 20px;
            border-width: 2px;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 20px;
        }
        .getStartedButton:hover {
            background-color: rgb(0, 158, 0);
            color: white;
            border-color: rgb(0, 158, 0);
        }
        </style>
        <div class="body">
            <h1>AyurBot</h1>
            <p>Discover your Prakruthi using an AI-based chatbot.</p>
            <button class="getStartedButton" onclick="start_chat()">Get Started</button>
        </div>
        <script>
            function start_chat() {
                fetch("/start_chat").then(() => location.reload());
            }
        </script>
        """,
        unsafe_allow_html=True
    )

@st.cache_resource
def start_chat():
    st.session_state.chat_started = True

def ayurbot():
    st.title("AyurBot Chat")
    
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
            bot_response = random.choice(brain.questions)
            st.markdown(bot_response)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    main()
