import math
import statistics
import numpy as np

N_CLASSES = 20
N_AMOSTRAS = 100

TEMPO_DE_CHEGADA = 5
TEMPO_DE_SERVICO = 5
TAMANHO_FILA = 10

def gera_amostras_exponencial(tam, param_lambda):
    amostras = []
    for i in range(0, tam):
        amostras[i] = np.random.exponential(param_lambda)
    return amostras

def gera_valor_aleatorio(p_classes, classes):
    n_classes = len(p_classes)
    p = uniform(0, 1)
    for i in range(0, n_classes):
        p -= p_classe[i]
        if p <= 0:
            return statistics.mean(classes[i])
    return statistics.mean(classes[-1])

# Gera funcao de distribuicao acumulada apartir das amostras dadas
def gera_funcao_distribuicao_acumulada(amostras = [], n_classes = 1):
    n_amostras = len(amostras)
    amostras = amostras.sort()
    
    valor_max = amostras[-1]
    valor_min = amostras[0]
    amplitude = valor_max - valor_min
    intervalo_classe = amplitude / n_classes

    classes = [[] for i in range(0, n_classes)]
    p_classe = [0 for i in range(0, n_classes)]

    for amostra in amostras:
        indice = math.floor(amostra / intervalo_classe)
        classes[indice].append(amostra)
        p_classe[indice] += (1 / n_amostras)

    return p_classe, classes
    

def proximo_TEC(deterministico, p_classe = [], classes = []):
    if deterministico:
        return TEMPO_DE_CHEGADA
    return gera_valor_aleatorio(p_classes, classes)

def proximo_TES(deterministico, p_classe = [], classes = []):
    if deterministico:
        return TEMPO_DE_CHEGADA
    return gera_valor_aleatorio(p_classes, classes)


def simulacao(n_passos, tec_deterministico, tes_deterministico, fila_finita):
    amostras_TEC = gera_amostras_exponencial(TEMPO_DE_CHEGADA)
    amostras_TES = gera_amostras_exponencial(TEMPO_DE_SERVICO)
    

'''
    - Gerar valores aleatorio [x]
    - Calcular o Tempo entre chegadas [x]
        - Deterministico: C
        - Aleatorio:  

'''