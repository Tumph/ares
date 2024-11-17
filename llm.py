#This microservice will handle all the LLM calls to OpenAI.

from dotenv import load_dotenv
from openai import OpenAI
import os
from flask import Flask

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


# Helper function for OpenAI responses
def get_openai_response(context, question):
    # If context is a list of message dicts, use directly
    if isinstance(context, list):
        messages = context
    # Otherwise wrap the context in a system message
    else:
        messages = [{"role": "system", "content": str(context)}]
    
    # Add the user question
    messages.append({"role": "user", "content": str(question)})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response = completion.choices[0].message.content
    return response