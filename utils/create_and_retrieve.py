import os
import shutil
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
See you are a mini chatbot and I will give you the context from where you need to answer and the question 
that the user asks please give relevant answers about it and have a good conversation with user.
If required analyze the chat history as well. In the chat_history you are Assistant and query is given by User.
The priority is to first look at chat history then look the question and then context if you didnot find any relevant answer from chat history then use context.
Chat_History: \n{chat_history}\n
Question: \n {question} \n
Context: \n {context}?\n
Answer: \n"""


def create_vector_db(chunks):
    """Create and persist a Chroma vector store."""
    # Ensure CHROMA_PATH directory exists
    CHROMA_PATH = "chroma"
    if not os.path.exists(CHROMA_PATH):
        os.makedirs(CHROMA_PATH)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", api_key=os.getenv('GOOGLE_API_KEY'))

    # Clear out the database if it exists
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    # Initialize Chroma with the correct settings
    db = Chroma.from_documents(chunks, embeddings)
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    return db

def retrieve_and_invoke(vectordb, query_text, context_history):
    # Retrieve documents relevant to the query
    results = vectordb.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0:
        return "Unable to find matching results.", []
    
    # Construct the context from the retrieved documents
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Combine existing context history with the new context
    context_history = "\n\n".join([context_history, context_text]) if context_history else context_text
    # Generate the prompt
    prompt = prompt_template.format(context=context_text, question=query_text, chat_history = context_history)
    
    model = genai.GenerativeModel(model_name="gemini-pro")
    response_text = model.generate_content(prompt).text
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    return response_text