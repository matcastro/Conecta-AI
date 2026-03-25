from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(f"{BASE_DIR}/clinica.db")
SCHEMA_PATH = Path(f"{BASE_DIR}/schema.sql")
SEED_PATH = Path(f"{BASE_DIR}/data.sql")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def read_sql_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def run_sql_script(conn: sqlite3.Connection, script: str) -> None:
    conn.executescript(script)
    conn.commit()


def initialize_database(force_reset: bool = False) -> None:
    """
    Cria e popula o banco de dados.

    Args:
        force_reset: se True, apaga o banco atual e recria do zero.
    """
    if force_reset and DB_PATH.exists():
        DB_PATH.unlink()

    conn = get_connection()
    try:
        schema_sql = read_sql_file(SCHEMA_PATH)
        data_sql = read_sql_file(SEED_PATH)

        run_sql_script(conn, schema_sql)
        run_sql_script(conn, data_sql)

        print(f"Banco inicializado com sucesso em: {DB_PATH}")
    finally:
        conn.close()


def database_exists() -> bool:
    return DB_PATH.exists()


if __name__ == "__main__":
    initialize_database(force_reset=True)