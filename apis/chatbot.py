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
- If a user asks for general Titanic related information, provide a detailed answer and  please do not give json response of general questions
-For any queries strictly related to charts, graphs,bar chart,scatter plot,box plot or histograms, return a JSON response strictly in the following format, containing only expaliantion of the details related to asked query in 5 lines, x_axis all values in array and y_axis all values in array values and mean , median,mode 

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


