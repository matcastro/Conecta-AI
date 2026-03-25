import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv

from tools import listar_especialidades_tool, listar_horarios_disponiveis_tool, agendar_consulta_tool, enviar_email_notificacao_tool

load_dotenv()
config = dotenv.dotenv_values()
llm_model = config['LLM_MODEL']

llm = ChatOpenAI(
    model=llm_model,
    temperature=0
)


tools = [
    listar_especialidades_tool,
    listar_horarios_disponiveis_tool,
    agendar_consulta_tool
]


gerenciador_consultas = create_agent(
    llm,
    tools
)

notificador_tools = [
    enviar_email_notificacao_tool
]

notificador_consultas = create_agent(
    llm,
    notificador_tools
)