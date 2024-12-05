import os

# Função principal que resolve uma instância
def resolve_instancia(arq_instancia, arq_solucao):
    def ler_instancia(instancias):
        distancias = []
        with open(instancias, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if linha and not any(char.isalpha() for char in linha):
                    distancias.append(list(map(float, linha.split(';'))))
        return distancias

    def escrever_solucao(solucoes, custo_total, atribuicoes):
       with open(solucoes, "w+", encoding="utf8") as f:
        f.write(f"Valor objetivo;{custo_total:.2f}\n")  # Valor objetivo no cabeçalho

        # Verifica se há atribuições para cada centro
        for centro, pontos in atribuicoes.items():
            if pontos:  # Garante que a linha não seja vazia
                f.write(f"{centro};" + ";".join(map(str, pontos)) + "\n")
            else:
                f.write(f"{centro};\n")  # Centro sem pontos atribuídos

    def heuristica_p_centros(distancias, p, conexoes_min, conexoes_max):
        n = len(distancias)
        centros = list(range(p))
        atribuicoes = {centro: [centro] for centro in centros}
        custo_total = 0

        for i in range(n):
            if i in centros:
                continue

            melhor_centro = None
            menor_distancia = float('inf')

            for centro in centros:
                if len(atribuicoes[centro]) < conexoes_max:
                    if distancias[i][centro] < menor_distancia:
                        melhor_centro = centro
                        menor_distancia = distancias[i][centro]

            if melhor_centro is None:
                melhor_centro = min(centros, key=lambda c: distancias[i][c])
                menor_distancia = distancias[i][melhor_centro]

            atribuicoes[melhor_centro].append(i)
            custo_total += menor_distancia

        return custo_total, atribuicoes

    distancias = ler_instancia(arq_instancia)

    # Ajuste dos parâmetros conforme a necessidade
    p = 2
    conexoes_min = 4
    conexoes_max = 6

    custo_total, atribuicoes = heuristica_p_centros(distancias, p, conexoes_min, conexoes_max)
    escrever_solucao(arq_solucao, custo_total, atribuicoes)

def processar_pasta_instancias(pasta_instancias, pasta_solucoes):
    os.makedirs(pasta_solucoes, exist_ok=True)

    for arquivo in os.listdir(pasta_instancias):
        if arquivo.endswith('.csv'):
            caminho_entrada = os.path.join(pasta_instancias, arquivo)
            caminho_saida = os.path.join(pasta_solucoes, f"solucao_{arquivo}")
            try:
                resolve_instancia(caminho_entrada, caminho_saida)
                print(f"Processado: {arquivo} -> {caminho_saida}")
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

# Caminhos das pastas (ajuste conforme seu ambiente)
pasta_instancias = r'instancias'
pasta_solucoes = r'solucoes'

processar_pasta_instancias(pasta_instancias, pasta_solucoes)
