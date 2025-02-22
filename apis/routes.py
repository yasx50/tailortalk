from fastapi import FastAPI



# yaha pr function import kar rha hu
from chatbot import get_response

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/req/{qustion}")
def read_root(qustion:str):
    return get_response(qustion)


