from langchain_core.tools import tool
from database import listar_especialidades, listar_horarios_disponiveis


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

@tool
def listar_horarios_disponiveis_tool(
    especialidade: str,
    data: str | None = None
) -> str:
    """
    Lista os horários disponíveis para uma especialidade médica.
    Pode opcionalmente receber uma data específica (YYYY-MM-DD).
    """

    horarios = listar_horarios_disponiveis(especialidade, data)

    if not horarios:
        return f"Não há horários disponíveis para {especialidade}."

    resposta = f"Os horários disponíveis para {especialidade.title()} são:\n\n"

    for h in horarios:
        resposta += (
            f"{h['medico_nome']}: {h['data']} às {h['hora']}\n"
        )

    print("\n\n###")
    print("Listar horários tool resposta:")
    print(resposta)
    print("###\n\n")
    return resposta