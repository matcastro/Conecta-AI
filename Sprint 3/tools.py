from langchain_core.tools import tool
from database import listar_especialidades, listar_horarios_disponiveis, agendar_consulta


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
            f"{h['horario_id']} - {h['medico_nome']}: {h['data']} às {h['hora']}\n"
        )

    print("\n\n###")
    print("Listar horários tool resposta:")
    print(resposta)
    print("###\n\n")
    return resposta

@tool
def agendar_consulta_tool(
    cpf: str,
    horario_id: int,
    observacoes: str | None = None
) -> str:
    """
    Agenda uma consulta para um paciente usando CPF e o ID do horário disponível.
    """

    resultado = agendar_consulta(cpf, horario_id, observacoes)

    if not resultado["sucesso"]:
        return resultado["mensagem"]

    agendamento = resultado["agendamento"]

    paciente = agendamento["paciente_nome"]
    medico = agendamento["medico_nome"]
    especialidade = agendamento["especialidade"]
    data = agendamento["data"]
    hora = agendamento["hora"]

    print("\n\n###")
    print("Agendar consulta tool resposta:")
    print(f"Paciente: {paciente}")
    print(f"Médico: {medico}")
    print(f"Especialidade: {especialidade}")
    print(f"Data: {data}")
    print(f"Hora: {hora}")
    print("###\n\n")

    return (
        f"Consulta agendada com sucesso para {paciente} "
        f"com {medico}, especialidade {especialidade}, "
        f"no dia {data} às {hora}."
    )