from graph import graph

while True:
    print("Digite sua mensagem abaixo ou digite sair para fechar o programa.")
    user_input = input("\nVocê: ")

    if user_input.lower() == "sair":
        break

    result = graph.invoke({
        "input": user_input
    })

    print("\nAssistente:")
    print(result["output"])