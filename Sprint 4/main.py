import asyncio
import dotenv
from dotenv import load_dotenv
from client import client
from langchain.agents import create_agent

load_dotenv()
config = dotenv.dotenv_values()

async def main():
    tools = await client.get_tools()
    agent = create_agent(
        config['LLM_MODEL'],
        tools
    )

    print("=== Sistema da Clínica ===")
    print("Digite sua mensagem ou 'sair' para encerrar.\n")

    while True:
        query = input("Você: ")
        if query.lower() == "sair":
            print("Encerrando...")
            break
        try:
            response = await agent.ainvoke(
                {
                    "messages": [
                        {"role": "user", "content": query}
                    ]
                }
            )

            resposta_final = response["messages"][-1].content

            print(f"\nAssistente: {resposta_final}\n")

        except Exception as e:
            print(f"\nErro: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())