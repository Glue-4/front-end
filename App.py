from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st
import requests
import json

def session_starter():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database.")
        ]

session_starter()
# Nama web pada tab
st.set_page_config(page_title='Chat with MySQL', page_icon=':left_speech_bubble:', layout='wide')

# Judul web
st.title("Chat with MySQL :left_speech_bubble:")
# Sidebar untuk connect database
with st.sidebar:
    st.subheader("Connect Database :floppy_disk:")
    st.write("Connect to the database and start chatting.")
    # User input
    st.text_input("Host", key="Host", value="127.0.0.1")
    st.text_input("Port", key="Port", value="3306")
    st.text_input("User", key="User", value="root")
    st.text_input("Password", type="password", key="Password", value="Qwerty123456#")
    st.text_input("Database", key="Database", value="chinook")

    st.write("")
    st.write("")
    st.write("")
    st.subheader("Change Database and Clear Chat History")
    st.write("Change the database and clear the chat history by click-ing the Reset button")
    if st.button("Reset"):
        with st.spinner("Cleaning chat history...."):
            del st.session_state["chat_history"]
            session_starter()

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Ask me about the database...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    response_json = requests.post("http://localhost:8000/query",
                                  json={'question': user_query,
                                        'host': st.session_state["User"],
                                        'port': st.session_state["Port"],
                                        'user': st.session_state["Host"],
                                        'password': st.session_state["Password"],
                                        'database': st.session_state["Database"]
                                        }
                                  )
    with st.chat_message("AI"):
        response = json.loads(response_json)
        st.markdown(response["jawaban"])

    st.session_state.chat_history.append(AIMessage(content=response["jawaban"]))

#tambah fitur
#login dengan google atau rds (secret.tombol
#=======
#masalah di session
#masalah di upload sql tiap database design tool berbeda walaupun dalam extension .sql yg sama
#jika upload .sql dimana query dijalankan,
#jika upload .sql 2x maka query dijalankan 2 kali -> database saling bertumpuk,
#cara mereset memory

#module request nerima json

#kirim data database
#nerima response
#tambah tombol reset
