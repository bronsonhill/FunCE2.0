import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


st.title("FunCE Chatbot B")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        "This is an experimental teaching tool. It has not been refined in detail and may be prone to 'hallucinations' (providing false information). It's designed for fun and your personal interest but should not be treated as a reliable source of information. We're interested in experimenting with AI-based teaching tools in FunCE. Thank you for your understanding."
    )


def setup():

    # Select OpenAI model
    if "openai_model_b" not in st.session_state:
        st.session_state["openai_model_b"] = "gpt-3.5-turbo-0125"

    # Initialise chat history
    if "chat_history_b" not in st.session_state:
        st.session_state["chat_history_b"] = [{"role": "assistant", "content": "Hi, I'm AI Chris. I can help you with your questions about chemical engineering. What would you like to discuss?"}]
    
    with open("system_prompt.txt", "r") as file:
        system_prompt = file.read()
    
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = system_prompt
        
    Settings.llm = OpenAI(model=st.session_state["openai_model_b"], temperature=0.5, system_prompt=st.session_state["system_prompt"])

setup()


# Loads data from the "knowledge" directory
@st.cache_resource(show_spinner=False)
def load_data_b(): 
    with st.spinner(text="Loading knowledge base, please do not leave this page"):
        reader = SimpleDirectoryReader(input_dir="knowledge", recursive=True)
        docs = reader.load_data()
        index = VectorStoreIndex.from_documents(docs)
        return index

index = load_data_b()


# Initialize the chat engine
if "chat_engine_b" not in st.session_state.keys():
    st.session_state["chat_engine_b"] = index.as_chat_engine(chat_mode="condense_question", verbose=True)


# Chat logic
if prompt := st.chat_input("Ask questions here"):
    st.session_state["chat_history_b"].append({"role": "user", "content": prompt})


# Display the prior chat messages
for message in st.session_state["chat_history_b"]:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])


# If last message is not from the assistant, generate a new response
if st.session_state["chat_history_b"][-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Use the chat engine to generate a response
            response = st.session_state["chat_engine_b"].chat(prompt)
            st.markdown(response.response)

            # Add the response to the chat history
            message = {"role": "assistant", "content": response.response}
            st.session_state["chat_history_b"].append(message)