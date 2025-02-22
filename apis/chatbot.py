import os
from dotenv import load_dotenv
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from fastapi.responses import JSONResponse


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")


llm = ChatGroq(api_key=api_key, model_name="llama-3.3-70b-versatile")

# system prompt
system_prompt = """
You are a Titanic data analyst and storyteller. Your expertise is limited to the Titanic dataset you have to understand hindi and english well . 
- If a user asks for general Titanic related information, provide a detailed answer. please do not give json response of general questions
- If the user asks for a chart,  or histogram and pie chart always return a JSON response containing numerical values.
For any queries strictly related to charts, graphs, or histograms, return a JSON response strictly in the following format, containing only expaliantion, x_axis and y_axis values and mean , media,mode  and just explain in 4-5 lines do not say i can not display images  :

- If a question is outside the Titanic context, respond with: 
  'My expertise is on the Titanic ship only.'
"""


prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt ),
    ("user", "{input}")
])


def get_response(user_query: str):
    chain = prompt | llm  
    response = chain.invoke({"input": user_query})
    return (response.content) 


