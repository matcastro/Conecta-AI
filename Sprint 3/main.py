from graph import graph

resposta = graph.invoke(
    {
        "input": "Quais especialidades a clínica atende?"
    }
)

print(resposta["output"])