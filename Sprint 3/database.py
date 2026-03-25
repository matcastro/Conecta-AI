from typing import Any

from pathlib import Path
import sqlite3


DB_PATH = Path(f"banco/clinica.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return dict(row)


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


# =========================
# Leitura
# =========================

def buscar_paciente_por_cpf(cpf: str) -> dict[str, Any] | None:
    query = """
        SELECT
            id,
            nome,
            cpf,
            telefone,
            convenio,
            criado_em
        FROM pacientes
        WHERE cpf = ?
    """

    with get_connection() as conn:
        row = conn.execute(query, (cpf,)).fetchone()
        return row_to_dict(row)


def listar_especialidades() -> list[str]:
    query = """
        SELECT DISTINCT especialidade
        FROM medicos
        WHERE ativo = 1
        ORDER BY especialidade
    """

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
        return [row["especialidade"] for row in rows]


def listar_medicos_por_especialidade(especialidade: str) -> list[dict[str, Any]]:
    query = """
        SELECT
            id,
            nome,
            especialidade,
            ativo
        FROM medicos
        WHERE LOWER(especialidade) = LOWER(?)
          AND ativo = 1
        ORDER BY nome
    """

    with get_connection() as conn:
        rows = conn.execute(query, (especialidade,)).fetchall()
        return rows_to_dicts(rows)


def listar_horarios_disponiveis(
    especialidade: str,
    data: str | None = None
) -> list[dict[str, Any]]:
    query = """
        SELECT
            h.id AS horario_id,
            h.data,
            h.hora,
            m.id AS medico_id,
            m.nome AS medico_nome,
            m.especialidade
        FROM horarios h
        JOIN medicos m ON m.id = h.medico_id
        WHERE LOWER(m.especialidade) = LOWER(?)
          AND m.ativo = 1
          AND h.disponivel = 1
    """
    params: list[Any] = [especialidade]

    if data:
        query += " AND h.data = ?"
        params.append(data)

    query += """
        ORDER BY h.data, h.hora, m.nome
    """

    with get_connection() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()
        return rows_to_dicts(rows)


def listar_consultas_do_paciente(cpf: str) -> list[dict[str, Any]]:
    query = """
        SELECT
            a.id AS agendamento_id,
            a.status,
            a.observacoes,
            a.criado_em,
            p.nome AS paciente_nome,
            p.cpf,
            m.nome AS medico_nome,
            m.especialidade,
            h.data,
            h.hora
        FROM agendamentos a
        JOIN pacientes p ON p.id = a.paciente_id
        JOIN horarios h ON h.id = a.horario_id
        JOIN medicos m ON m.id = h.medico_id
        WHERE p.cpf = ?
        ORDER BY h.data, h.hora
    """

    with get_connection() as conn:
        rows = conn.execute(query, (cpf,)).fetchall()
        return rows_to_dicts(rows)


def buscar_horario_por_id(horario_id: int) -> dict[str, Any] | None:
    query = """
        SELECT
            h.id AS horario_id,
            h.data,
            h.hora,
            h.disponivel,
            m.id AS medico_id,
            m.nome AS medico_nome,
            m.especialidade
        FROM horarios h
        JOIN medicos m ON m.id = h.medico_id
        WHERE h.id = ?
    """

    with get_connection() as conn:
        row = conn.execute(query, (horario_id,)).fetchone()
        return row_to_dict(row)


####
# Funções de escrita (criação, atualização, exclusão)
##

def cadastrar_paciente(
    nome: str,
    cpf: str,
    telefone: str,
    convenio: str | None = None
) -> dict[str, Any]:
    paciente_existente = buscar_paciente_por_cpf(cpf)
    if paciente_existente:
        return {
            "sucesso": False,
            "mensagem": "Já existe um paciente cadastrado com esse CPF.",
            "paciente": paciente_existente,
        }

    query = """
        INSERT INTO pacientes (nome, cpf, telefone, convenio)
        VALUES (?, ?, ?, ?)
    """

    with get_connection() as conn:
        cursor = conn.execute(query, (nome, cpf, telefone, convenio))
        conn.commit()

        paciente_id = cursor.lastrowid
        paciente = conn.execute(
            """
            SELECT id, nome, cpf, telefone, convenio, criado_em
            FROM pacientes
            WHERE id = ?
            """,
            (paciente_id,),
        ).fetchone()

    return {
        "sucesso": True,
        "mensagem": "Paciente cadastrado com sucesso.",
        "paciente": row_to_dict(paciente),
    }


def agendar_consulta(
    cpf: str,
    horario_id: int,
    observacoes: str | None = None
) -> dict[str, Any]:
    with get_connection() as conn:
        paciente = buscar_paciente_por_cpf(cpf)
        if not paciente:
            return {
                "sucesso": False,
                "mensagem": "Paciente não encontrado para o CPF informado.",
            }

        horario = buscar_horario_por_id(horario_id)
        if not horario:
            return {
                "sucesso": False,
                "mensagem": "Horário não encontrado.",
            }

        if horario["disponivel"] == 0:
            return {
                "sucesso": False,
                "mensagem": "O horário informado não está disponível.",
            }

        cursor = conn.execute(
            """
            INSERT INTO agendamentos (paciente_id, horario_id, status, observacoes)
            VALUES (?, ?, 'agendado', ?)
            """,
            (paciente["id"], horario_id, observacoes),
        )

        conn.execute(
            """
            UPDATE horarios
            SET disponivel = 0
            WHERE id = ?
            """,
            (horario_id,),
        )

        conn.commit()

        agendamento_id = cursor.lastrowid

        agendamento = conn.execute(
            """
            SELECT
                a.id AS agendamento_id,
                a.status,
                a.observacoes,
                p.nome AS paciente_nome,
                p.cpf,
                m.nome AS medico_nome,
                m.especialidade,
                h.data,
                h.hora
            FROM agendamentos a
            JOIN pacientes p ON p.id = a.paciente_id
            JOIN horarios h ON h.id = a.horario_id
            JOIN medicos m ON m.id = h.medico_id
            WHERE a.id = ?
            """,
            (agendamento_id,),
        ).fetchone()

    return {
        "sucesso": True,
        "mensagem": "Consulta agendada com sucesso.",
        "agendamento": row_to_dict(agendamento),
    }


def cancelar_consulta(agendamento_id: int) -> dict[str, Any]:
    with get_connection() as conn:
        agendamento = conn.execute(
            """
            SELECT
                a.id,
                a.status,
                a.horario_id
            FROM agendamentos a
            WHERE a.id = ?
            """,
            (agendamento_id,),
        ).fetchone()

        if not agendamento:
            return {
                "sucesso": False,
                "mensagem": "Agendamento não encontrado.",
            }

        if agendamento["status"] == "cancelado":
            return {
                "sucesso": False,
                "mensagem": "A consulta já está cancelada.",
            }

        conn.execute(
            """
            UPDATE agendamentos
            SET status = 'cancelado'
            WHERE id = ?
            """,
            (agendamento_id,),
        )

        conn.execute(
            """
            UPDATE horarios
            SET disponivel = 1
            WHERE id = ?
            """,
            (agendamento["horario_id"],),
        )

        conn.commit()

        consulta_cancelada = conn.execute(
            """
            SELECT
                a.id AS agendamento_id,
                a.status,
                p.nome AS paciente_nome,
                p.cpf,
                m.nome AS medico_nome,
                m.especialidade,
                h.data,
                h.hora
            FROM agendamentos a
            JOIN pacientes p ON p.id = a.paciente_id
            JOIN horarios h ON h.id = a.horario_id
            JOIN medicos m ON m.id = h.medico_id
            WHERE a.id = ?
            """,
            (agendamento_id,),
        ).fetchone()

    return {
        "sucesso": True,
        "mensagem": "Consulta cancelada com sucesso.",
        "agendamento": row_to_dict(consulta_cancelada),
    }

if __name__ == "__main__":
    ### TESTE RÁPIDO DAS FUNÇÕES
    print("Especialidades:")
    print(listar_especialidades())

    print("\nPaciente por CPF:")
    print(buscar_paciente_por_cpf("11111111111"))

    print("\nMédicos de Cardiologia:")
    print(listar_medicos_por_especialidade("Cardiologia"))

    print("\nHorários disponíveis em Dermatologia:")
    print(listar_horarios_disponiveis("Dermatologia"))

    print("\nConsultas do paciente 11111111111:")
    print(listar_consultas_do_paciente("11111111111"))