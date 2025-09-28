from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

from src.prompts import SUMMARIZE_PROMPT_SYSTEM, SUMMARIZE_PROMPT_USER
from src.utils import setup_logger
from src.tools import wiki_search

from typing_extensions import TypedDict, Annotated

class State(TypedDict):
    question: str
    search_results: str
    answer: str
    messages: Annotated[list[AnyMessage], add_messages]

# Free local model using Hugging Face

    # Use a lightweight, free model that runs locally
hf_pipeline = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-medium",  # Free, lightweight model
    tokenizer="microsoft/DialoGPT-medium",
    max_length=512,
    temperature=0.7,
    do_sample=True,
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)
print("✅ Using Hugging Face DialoGPT model (free, local)")
llm.invoke("Hello, how are you?")


logger = setup_logger("graph")