import streamlit as st
import pandas as pd


if 'chat_histories' not in st.session_state:
    st.session_state['chat_histories'] = []
if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = []


def handle_input():
    user_input = st.session_state['user_input']
    if user_input:
        st.session_state['current_chat'].append(("User", user_input))
        response = generate_response(user_input)  
        st.session_state['current_chat'].append(("Bot", response))
        st.session_state['user_input'] = ''  


def generate_response(user_input):
    return "This is a placeholder response to: " + user_input


def new_chat():
 
    if st.session_state['current_chat']:
        st.session_state['chat_histories'].append(st.session_state['current_chat'])

    st.session_state['current_chat'] = []

def read_csv_file(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

def get_chat_title(chat):
    for user, message in chat:
        if user == "User": 
            return message.split()[0] if message else "Chat"
    return "Chat"


st.title("Chat Interface")

st.sidebar.header("Chat History")
for i, chat in enumerate(st.session_state['chat_histories']):
    title = get_chat_title(chat) 
    with st.sidebar.expander(f"{title}"):  
        for user, message in chat:
            if user == "User":
                st.markdown(f"**You:** {message}")
            else:
                st.markdown(f"**Bot:** {message}")


if st.sidebar.button("New Chat"):
    new_chat()

if st.session_state['current_chat']:
    st.markdown("### Current Chat")
    for user, message in st.session_state['current_chat']:
        if user == "User":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Bot:** {message}")

st.text_input("Type your message:", key='user_input', on_change=handle_input)


st.markdown("### Upload a file")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])


csv_data = read_csv_file(uploaded_file)
if csv_data is not None:
    st.subheader("CSV Content")
    st.dataframe(csv_data)
