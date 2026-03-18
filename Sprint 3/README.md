# CliniFlow AI

CliniFlow AI é um projeto prático para aprendizado de **sistemas multiagentes com LangGraph e LangChain**.

O objetivo do projeto é construir um assistente de atendimento para uma clínica médica capaz de:

- listar especialidades médicas disponíveis
- listar médicos por especialidade
- consultar horários disponíveis
- agendar consultas
- cancelar consultas
- enviar notificações ao paciente

O sistema utiliza **múltiplos agentes especializados**, cada um responsável por uma etapa do fluxo.

---

# Arquitetura do projeto

A solução utiliza uma arquitetura baseada em **multiagentes orquestrados por um grafo**.

Cada agente possui uma responsabilidade específica:

| Agente | Responsabilidade |
|------|------|
| Gerenciador de Consultas | Gerir informações sobre médicos, consultas e pacientes |
| Notificador | Enviar notificações ao paciente |


---

# Estrutura do projeto

* `main.py`: Ponto de entrada da aplicação. Recebe a solicitação do usuário e executa o grafo de agentes.
* `graph.py`: Define o estado compartilhado entre agentes, os nós do grafo e o fluxo de execução entre os agentes.
* `agents.py`: Contém a implementação dos agentes do sistema.
* `tools.py`: Define as tools que os agentes podem utilizar. Essas tools utilizam funções do `database.py`.
* `database.py`: Contém a implementação do banco de dados. Contém a inicialização do banco SQLite, funções de acesso ao banco e operações de leitura e escrita.
* `banco/`: Pasta que contém os scripts SQL para criação e população do banco de dados.

---

# Banco de dados

O projeto utiliza **SQLite**.

## Tabelas
| Tabela | Descrição |
|------|------|
| pacientes | cadastro de pacientes |
| medicos | médicos da clínica |
| horarios | horários disponíveis |
| agendamentos | consultas marcadas |
