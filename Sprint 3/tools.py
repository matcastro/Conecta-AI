from langchain_core.tools import tool
from database import listar_especialidades


@tool
def listar_especialidades_tool() -> str:
    """
    Lista todas as especialidades médicas disponíveis na clínica.
    """
    especialidades = listar_especialidades()

    if not especialidades:
        return "No momento não há especialidades cadastradas."

    resposta = "A clínica atende as seguintes especialidades:\n"

    for esp in especialidades:
        resposta += f"- {esp}\n"

    print("\n\n###")
    print("Listar especialidades tool resposta:")
    print(resposta)
    print("###\n\n")
    return resposta