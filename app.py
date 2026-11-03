from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
# from langchain.chat_models import ChatOpenAI
from importlib import import_module

# Load LangServe dynamically so static analyzers do not flag the optional dependency.
add_routes = import_module("langserve").add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

# LangChain automatically sends traces to LangSmith when these environment
# variables are configured. Keep credentials in .env, never in source control.
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "ollama-api")

# Initialize FastAPI app
app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description=f"A simple API Server ({LANGCHAIN_PROJECT})"

)

# Optional OpenAI route for later use. Uncomment the import and this route
# after installing/configuring langchain-openai and an OpenAI API key.
# add_routes(
#     app,
#     ChatOpenAI(),
#     path="/openai"
# )

# Ollama model used by the active routes.
llm=Ollama(model="llama3.2")

# Prompt templates for essay and poem generation
prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")


# Generate an essay / route 1
add_routes(
    app,
    prompt1|llm,
    path="/essay"
)

# Generate a poem / route 2
add_routes(
    app,
    prompt2|llm,
    path="/poem"


)

# Run the FastAPI app
if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
