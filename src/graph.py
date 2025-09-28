from langgraph.graph import StateGraph, START, END, add_messages
from langchain_ollama import OllamaLLM
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage

from src.prompts import SUMMARIZE_PROMPT_SYSTEM, SUMMARIZE_PROMPT_USER
from .utils import setup_logger
from .tools import wiki_search

from typing_extensions import TypedDict, Annotated

class State(TypedDict):
    question: str
    search_results: str
    answer: str
    messages: Annotated[list[AnyMessage], add_messages]

    

llm = OllamaLLM(model="llama2", temperature=0.7)
logger = setup_logger("graph")

def search_node(state: State) -> State:
    query = state["question"]
    
    # Search tool call

    result_list = wiki_search(query)
    result = "\n".join(result_list) if result_list else "No results found."

    state["search_results"] = result

    search_message = AIMessage(content=f"Search results:\n{result}")
    state["messages"].append(search_message)

    return state

def summarize_node(state: State) -> State:
    result = state["search_results"]
    
    summarize_prompt_system = SUMMARIZE_PROMPT_SYSTEM
    summarize_prompt_user = SUMMARIZE_PROMPT_USER.format(search_results=result)

    system_message = AIMessage(content=summarize_prompt_system)
    user_message = HumanMessage(content=summarize_prompt_user)

    state["messages"].extend([system_message, user_message])

    # try:
    full_prompt = f"{summarize_prompt_system}\n\nUser:\n{summarize_prompt_user}"
    response = llm.invoke(full_prompt)
    cleaned_response = response.strip() if hasattr(response, 'strip') else str(response)
    # except Exception as e:
    #     logger.error(f"LLM invocation failed: {e}")
    #     cleaned_response = "Error generating summary."
    
    logger.info(f"LLM response: {cleaned_response}")
    state["answer"] = cleaned_response

    ai_response = AIMessage(content=cleaned_response)
    state["messages"].append(ai_response)

    return state

def build_graph() -> StateGraph:
    graph = StateGraph(State)

    graph.add_node("search", search_node)
    graph.add_node("summarize", summarize_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()

if __name__ == "__main__":
    study_graph = build_graph()

    init_state: State = {
        "messages": [HumanMessage(content="What is Newton's second law?")],
        "question": "What is Newton's second law?",
        "search_results": "",
        "answer": "",
    }

    result = study_graph.invoke(init_state)

    print("\n--- Structured Variables ---")
    print("Question:", result["question"])
    print("Search Results:", result["search_results"])
    print("Answer:", result["answer"])

    print("\n--- Conversation History ---")
    for msg in result["messages"]:
        role = msg.__class__.__name__.replace("Message", "").upper()
        print(f"{role}: {msg.content}")
