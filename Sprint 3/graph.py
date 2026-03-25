from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents import gerenciador_consultas


class AgentState(TypedDict):
    input: str
    output: str


def executar_agente(state: AgentState):
    resposta = gerenciador_consultas.invoke(
        {"messages": [("user", state["input"])]}
    )

    return {
        "output": resposta["messages"][-1].content
    }


builder = StateGraph(AgentState)

builder.add_node("gerenciador_consultas", executar_agente)

builder.set_entry_point("gerenciador_consultas")

builder.add_edge("gerenciador_consultas", END)

graph = builder.compile()