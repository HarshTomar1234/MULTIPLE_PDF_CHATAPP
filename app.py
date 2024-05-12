import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub


def get_pdf_text(pdf_docs):
    text = ""    # Stores all the text content from the pdf
    for pdf in pdf_docs:
        # PdfReader object is used to read the contents of a PDF file. Here's a basic example of how you can use it:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()   # Extracts all the raw text from the pdf

    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  # Every Chunk is divide into 1000 words
        chunk_overlap=200,  # Protect chunks from overlapping
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
    # embeddings = HuggingFaceInstructEmbeddings( model = hkunlp/instructor-large)

    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorscore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.5, "max_length": 512})
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorscore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.error("Conversation chain is not initialized. Please upload PDFs and click 'Process' first.")


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner('Processing'):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the test chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)

                # In Streamlit, session_state is a feature that allows you to store and access session-specific state across different components and interactions within a Streamlit app.
                # It helps you manage the state of your app without relying on global variables or relying on the user's browser for storage.

                # Session State: Streamlit's session_state is essentially a dictionary-like object that persists throughout the entire duration of a user's session with the app.
                # Usage: You can use session_state to store and retrieve values that you want to persist across different interactions or components within your Streamlit app.
                # Initialization: To use session_state, you need to initialize it at the beginning of your Streamlit script using st.session_state. Once initialized, you can access it like any other Python dictionary.
                # Persistent Data: Any data you store in session_state will be retained as long as the user's session is active. This means that even if the user interacts with different parts of your app or refreshes the page, the data will still be available.


if __name__ == '__main__':
    main()

