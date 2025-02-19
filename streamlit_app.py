import streamlit as st
import brain
import random

# Initialize session state for chat messages and Prakriti calculation
if "messages" not in st.session_state:
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

# Function for the AYURBOT page
def ayurbot():
    st.markdown(
        """
        <h2 style="text-align: center; color: #D3D3D3; font-family: 'Times New Roman';">AYURBOT</h1>
        """,
        unsafe_allow_html=True
    )
    st.subheader('', divider='rainbow')
    st.markdown(
        """
        <h5 style="color: #D3D3D3,font-weight: normal;">Hi there! I am Chatbot specific to determine the Prakriti of an individual. So now lets determine your Prakriti!</h5>
        """,
        unsafe_allow_html=True
    )

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("Send a message"):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate bot response
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

# Function for the HOME page
def main():
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url(https://images.pexels.com/photos/66997/pexels-photo-66997.jpeg?cs=srgb&dl=pexels-no-name-66997.jpg&fm=jpg);
    height = 50%;
    background-position: center;
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
        <h2 style="text-align: center; color: black; font-family: 'Times New Roman', sans-serif;">PRAKRITI</h1>
        """,
        unsafe_allow_html=True
    )
    st.subheader('', divider='rainbow')
    st.markdown(
        """
        <h5 style="color: black;">It is a term used in traditional Indian philosophy, particularly in Ayurveda, to describe the inherent constitution or nature of an individual.</h5>
        <h5 style="color: black;">In Ayurveda, it is believed that every person has a unique combination of three fundamental energies or doshas known as VATA, PITTA and KAPHA, which make up their Prakriti.</h5>
        <h5 style="color: black;">These doshas represent different combinationof five elements (Earth, Water, Fire, Air and Ether) and play physical and physcological characteristics as well as their susceptibility to certain health issues.</h5>
        """,
        unsafe_allow_html=True
    )

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 5])
with col1:
    if st.button("HOME"):
        st.session_state.page = 'home'
with col2:
    if st.button("AYURBOT"):
        st.session_state.page = 'ayurbot'

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Display the appropriate page based on session state
if st.session_state.page == 'home':
    main()

if st.session_state.page == 'ayurbot':
    ayurbot()

# Embed the HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AyurBot</title>

    <script src="scripts.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        .body {
            background-image : url("https://wallpaperaccess.com/full/432582.jpg");
            background-size : cover;
            background-repeat:  no-repeat;
            color : white;
            height : 100vh;
        }
        h1 {
            font-size : 100px
        }
        .logo {
            border-radius : 700px;
            height : 70px;
        }
        .mainSection {
            height: 600px; 
            display: flex; 
            align-items: center; 
            justify-content: center;
        }
        .mainSectionContainer {
            width : 100%;
        }
        .navbarButton {
            color : white;
            background-color : white;
        }
        .navbar {
            background-color  : transparent;
        }
        h1 {
            font-weight : 0px;
            font-family : "Comic sans";
        }
        .getStartedButton {
            background-color : transparent;
            color : white;
            border-color :rgb(0, 158, 0);
            margin-top : 20px;
            border-width : 2px;
            border-radius : 20px;
        }
        .body, .navbar {
            color : white;
        }
        .getStartedButton:hover {
            background-color : rgb(0, 158, 0);
            color : white;
            border-color :rgb(0, 158, 0);
        }
        .buttonContainer {
            display : flex;
            flex-direction: row;
            margin : auto;
        }
        #aboutUs {
            display : none;
        }
        .footer {
            margin: auto;
        }
    </style>
</head>

<body class="container-fluid body">
    <header class="text-left">
        <nav class="navbar navbar-expand-lg navbar-light bg-light bg-transparent text-white">
            <a class="navbar-brand text-white" href="#">
                <img src="https://res.cloudinary.com/dopay7cbn/image/upload/c_crop,w_600,h_600,ar_1:1/v1739964879/Screenshot_2025-02-19_170355_dfekic.png"
                    alt="ayur chat bot logo" class="logo" />
            </a>
            <button class="navbarButton navbar-toggler" type="button" data-toggle="collapse"
                data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav ml-auto text-white">
                    <a class="nav-item nav-link active text-white" href="#">Home <span
                            class="sr-only">(current)</span></a>
                    <a class="nav-item nav-link text-white" href="#">Chat</a>
                    <a class="nav-item nav-link text-white" href="#aboutUs" id="aboutUsLink">About us</a>
                    <a class="nav-item nav-link text-white" href="#">Login</a>
                </div>
            </div>
        </nav>
    </header>

    <main class="mainSection" >
        <div class="mainSectionContainer text-center d-flex flex-column justify-content-center">
            <div class="d-flex flex-column justify-content-center">
                <div class="d-flex flex-column justify-content-center">
                    <div>
                        <h1 class="">AyurBot</h1>
                        <p>Discover your Prakruthi using AI based chatbot.</p>
                    </div>
                    <div class="buttonContainer">
                        <button onclick="changeStyle()" class="getStartedButton text-center btn btn-success">
                            Get Started
                        </button>
                    </div>
                </div>
            </div>
            <div class="aboutUsContainer text-center" id="aboutUs">
                <h1>About Us</h1>
                <p>We are B.tech students of Sreenidhi Institute of Science & Technology.</p>
            </div>
        </div>
    </main>
    
    <footer class="fixed-bottom">
        <div class="footer m-auto">
            <p>&copy; Rights reserved by AyurBot</p>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js"
        integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js"
        integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
        crossorigin="anonymous"></script>
</body>
</html>
"""

st.components.v1.html(html_content, height=600)
