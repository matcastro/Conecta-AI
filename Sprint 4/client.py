import asyncio
import dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()
config = dotenv.dotenv_values()
client = MultiServerMCPClient(
    {
        "clinica": {
            "transport": "stdio",
            "command": "python",
            "args": ["mcp_server/clinica_mcp.py"],
        }
    }
)

async def main():
    tools = await client.get_tools()
    agent = create_agent(
        config['LLM_MODEL'],
        tools
    )

    clinica_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Busque o paciente com CPF 11111111111"}]}
    )
    
    print(clinica_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())