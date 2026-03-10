from rag import ask_a_question

def ask_and_format_answer(question):
    answer = ask_a_question(question)

    print(f"\nResposta: {answer["answer"]}")

    print("\nFontes")

    for i, context in enumerate(answer["context"]):
        print(f"Fonte {i+1}: {context.metadata['fonte']}")
        print(f"Conteúdo {i+1}: {context.page_content}\n")

def get_user_input():
    print('---\n')
    return input('# PERGUNTA (digite "sair" para encerrar) \n')

def start_chat():
    print('### BEM-VINDO AO ASSISTENTE JURÍDICO! FAÇA SUAS PERGUNTAS SOBRE O CDC E A LGPD. ###')

    question = get_user_input()
    
    while question.strip().lower() != "sair":
        ask_and_format_answer(question)

        question = get_user_input()
    
    print('### OBRIGADO POR USAR O ASSISTENTE JURÍDICO! ATÉ LOGO! ###')

if __name__ == "__main__":
    start_chat()
# ask_and_format_answer("O consumidor pode desistir da compra feita pela internet?")
# ask_and_format_answer("Quais são os direitos do titular de dados pessoais?")
# ask_and_format_answer("Como posso cozinhar um salmão?")