import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv

from tools import listar_especialidades_tool

load_dotenv()
config = dotenv.dotenv_values()
llm_model = config['LLM_MODEL']

llm = ChatOpenAI(
    model=llm_model,
    temperature=0
)


tools = [
    listar_especialidades_tool
]


gerenciador_consultas = create_agent(
    llm,
    tools
)