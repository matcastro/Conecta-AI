from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents import gerenciador_consultas, notificador_consultas


class AgentState(TypedDict):
    input: str
    output: str
    email_output: str


def executar_gerenciador(state: AgentState):
    resposta = gerenciador_consultas.invoke(
        {"messages": [("user", state["input"])]}
    )

    return {
        "output": resposta["messages"][-1].content
    }

def executar_notificador(state: AgentState):
    resposta = notificador_consultas.invoke(
        {"messages": [("user", f"Utilize os dados da mensagem a seguir para disparar o email de notificação:\n\n{state['output']}")]}
    )

    return {"email_output": resposta["messages"][-1].content}

# Router function
def decidir_proximo_passo(state: AgentState):
    output = state["output"].lower()
    
    if "agendada" in output or "cancelada" in output:
        return "notificar"

    return "fim"


builder = StateGraph(AgentState)

builder.add_node("gerenciador_consultas", executar_gerenciador)
builder.add_node("notificador_consultas", executar_notificador)

builder.set_entry_point("gerenciador_consultas")

builder.add_conditional_edges(
    "gerenciador_consultas",
    decidir_proximo_passo,
    {
        "notificar": "notificador_consultas",
        "fim": END
    }
)
builder.add_edge("notificador_consultas", END)

graph = builder.compile()