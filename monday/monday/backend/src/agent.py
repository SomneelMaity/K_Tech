import os
from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END


ANTHROPIC_API_KEY = "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"
ANTHROPIC_MODEL = "claude-sonnet-5"


class AgentState(TypedDict, total=False):
    user_text: str
    route: str
    answer: str
    final_answer: str


def get_llm():
    os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY

    return init_chat_model(
        ANTHROPIC_MODEL,
        model_provider="anthropic",
    )

def message_text(message):
    content = message.content
    if isinstance(content, str):
        return content
    return str(content)

def router_node(state:AgentState):
    llm = get_llm()
    prompt = """You are a router agent.
                route the user request into exactly one of these categories:
                coding - programming, debugging, software, terminal comands, project structure
                cooking - recipes, food, ingredients, kitchen help
                tarot - tarot reading, cards, spritual interpretation
                unknown - anything else
                return only one word: coding, cooking, tarot, unknown"""
    response = llm.invoke([
        ("system", prompt),
        ("human", state["user_text"])
    ])
    route = message_text(response).strip().lower()
    if "coding" in route:
        route = "coding"
    elif "cooking" in route:
        route = "cooking"
    elif "tarot" in route:
        route = "tarot"
    else:
        route = "unknown"
    return {"route": route}


def coding_agent_node(state:AgentState):
    llm = get_llm()
    prompt = """You are a coding agent.
                you are given a user request and you need to answer the user request.
                return the answer in a short and concise manner."""
    response = llm.invoke([
        ("system", prompt),
        ("human", state["user_text"])
    ])
    return {"answer": message_text(response)}

def validator_agent_node(state:AgentState):
    llm = get_llm()
    prompt = """
             1. check the coding agent answer for bugs, wrong comands, missing steps or unsafe
             2. if it is correct, return the improved final answer
             3. if it has mistakes, fix them and return the correct final answer
             4. Do not mention that you are validating unless needed"""
    response = llm.invoke([
        ("system", prompt),
        ("human", f"User request:\n{state['user_text']}\n\nCoding agent answer:\n{state['answer']}")
    ])
    return {"final_answer": message_text(response)}

def cooking_agent_node(state:AgentState):
    llm = get_llm()
    prompt = """You are a cooking agent.
                you are given a user request and you need to answer the user request.
                return the answer in a short and concise manner."""
    response = llm.invoke([
        ("system", prompt),
        ("human", state["user_text"])
    ])
    return {"final_answer": message_text(response)}

def tarot_agent_node(state:AgentState):
    llm = get_llm()
    prompt = """You are a tarot agent.
                you are given a user request and you need to answer the user request.
                return the answer in a short and concise manner."""
    response = llm.invoke([
        ("system", prompt),
        ("human", state["user_text"])
    ])
    return {"final_answer": message_text(response)}

def unknown_node(state:AgentState):
    return {"final_answer": "I'm sorry, I don't know how to help with that."}

def choose_next_node(state:AgentState):
    return state["route"]

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("coding", coding_agent_node)
    graph.add_node("validator", validator_agent_node)
    graph.add_node("cooking", cooking_agent_node)
    graph.add_node("tarot", tarot_agent_node)
    graph.add_node("unknown", unknown_node)

    graph.add_edge(START,"router")
    graph.add_conditional_edges("router", choose_next_node,{
        "coding": "coding",
        "cooking": "cooking",
        "tarot": "tarot",
        "unknown": "unknown"
    })
    graph.add_edge("coding", "validator")
    graph.add_edge("validator", END)
    graph.add_edge("cooking", END)
    graph.add_edge("tarot", END)
    graph.add_edge("unknown", END)

    return graph.compile()