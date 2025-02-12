import os 
from langsmith import Client
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model= "deepseek-r1-distill-qwen-32b",
    temperature=0.7,
    max_retries=2
    # api_key = api_key
    # other params...
)

messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming.")
]
response = llm.invoke(messages)

print(response.content)
