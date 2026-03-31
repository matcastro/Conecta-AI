from typing import Any

from fastmcp import FastMCP
import requests

mcp = FastMCP("clinica")

@mcp.tool()
async def buscar_paciente_por_cpf(cpf: str) -> dict[str, Any]:
    """
    Busca um paciente pelo CPF.

    Args:
        cpf: CPF do paciente (somente números)

    Returns:
        Dados do paciente
    """
    response = requests.get(f"http://localhost:8000/pacientes/{cpf}")

    if not response.ok:
        return {"erro": f"Erro ao chamar API: {response.status_code}"}

    return response.json()

@mcp.tool()
async def cadastrar_paciente(nome: str, cpf: str, telefone: str, convenio: str) -> dict[str, Any]:
    """
    Cadastra paciente.

    Args:
        nome: Nome do paciente
        cpf: CPF do paciente (somente números)
        telefone: Telefone do paciente (somente números)
        convenio: Convênio de saúde do paciente

    Returns:
        Dados do paciente
    """
    payload = {
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone,
        "convenio": convenio
    }
    response = requests.post(f"http://localhost:8000/pacientes", json=payload)

    if not response.ok:
        return {"erro": f"Erro ao chamar API: {response.status_code} {response.text}"}

    return response.json()

@mcp.tool()
async def consulta_horarios(especialidade: str, data: str) -> dict[str, Any]:
    """
    Consulta horários disponíveis.

    Args:
        especialidade: Especialidade dos médicos a serem consultados horários
        data: (opcional) Data para consulta de horários no formato YYYY-MM-DD

    Returns:
        Objeto com um array de horários disponíveis
    """
    query_string_date = ""
    data = data.strip()
    if (data is not None):
        query_string_date = f"&data={data}"
    response = requests.get(f"http://localhost:8000/horarios?especialidade={especialidade}{query_string_date}")

    if not response.ok:
        return {"erro": f"Erro ao chamar API: {response.status_code}"}

    return response.json()

@mcp.tool()
async def agendar_consulta(cpf: str, horario_id: int, observacoes: str) -> dict[str, Any]:
    """
    Agenda consulta.

    Args:
        cpf: CPF do paciente (somente números)
        horario_id: Id numérico do agendamento
        observacoes: Informações para adicionar ao agendamento

    Returns:
        Dados do agendamento
    """
    payload = {
        "cpf": cpf,
        "horario_id": horario_id,
        "observacoes": observacoes
    }
    response = requests.post(f"http://localhost:8000/consultas/agendar", json=payload)

    if not response.ok:
        return {"erro": f"Erro ao chamar API: {response.status_code} {response.text}"}

    return response.json()

if __name__ == "__main__":
    mcp.run()