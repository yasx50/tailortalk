import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from fastapi.responses import JSONResponse

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


if not api_key:
    raise ValueError("api key not found")
    

# Initialize OpenAI client with the correct model name

llm = ChatOpenAI(api_key=api_key, model_name="gpt-4o-mini")

# System prompt
system_prompt = """
You are a Titanic data analyst and storyteller. Your expertise is limited to the Titanic dataset you have to understand hindi and english well.

- If a user asks for general Titanic related information, provide a detailed answer not in json and nothing else
-For any queries strictly related to charts, graphs, bar chart, scatter plot, box plot or histograms, return a JSON response strictly in the following format, containing only explanation in 400 words, x_axis all values in array and y_axis all values in array not in json and mean, median, mode and do not add ``` this in starting and at ending just give simple json
- If a question is outside the Titanic context, respond with:
   My expertise is on the Titanic ship only.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

def get_response(user_query: str):
    chain = prompt | llm
    response = chain.invoke({"input": user_query})
    print(response.content)
    return response.content