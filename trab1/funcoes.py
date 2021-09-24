import sys
import math
import statistics
import numpy as np

N_CLASSES = 20
N_AMOSTRAS = 100

TEMPO_ENTRE_CHEGADA = 5
TEMPO_ENTRE_SERVICO = 5
TAMANHO_MAX_FILA = 10

def gera_amostras_exponencial(tam, param_lambda):
    amostras = []
    for i in range(0, tam):
        amostras[i] = np.random.exponential(param_lambda)
    return amostras

def gera_valor_aleatorio(p_classe, classes):
    n_classes = len(p_classe)
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
    

p_classe_TEC = []
classes_TEC = []
def proximo_TEC(deterministico):
    if deterministico:
        return TEMPO_ENTRE_CHEGADA
    return gera_valor_aleatorio(p_classe_TEC, classes_TEC)

p_classe_TES = []
classes_TES = []
def proximo_TES(deterministico):
    if deterministico:
        return TEMPO_ENTRE_SERVICO
    return gera_valor_aleatorio(p_classe_TES, classes_TES)


def simulacao(tempo_maximo, tec_deterministico, tes_deterministico, fila_finita):
    global p_classe_TEC, classes_TEC 
    global p_classe_TES, classes_TES 

    if(tec_deterministico):
        amostras_TEC = gera_amostras_exponencial(N_AMOSTRAS, TEMPO_ENTRE_CHEGADA)
        p_classe_TEC, classes_TEC = gera_funcao_distribuicao_acumulada(amostras_TEC, N_CLASSES)

    if(tes_deterministico):
        amostras_TES = gera_amostras_exponencial(N_AMOSTRAS, TEMPO_ENTRE_SERVICO)
        p_classe_TES, classes_TES = gera_funcao_distribuicao_acumulada(amostras_TES, N_CLASSES)

    TR, ES, TF, HC, HS  = 0, 0, 0, 0, sys.maxint
    tes, tec = 0, 0, 0

    interacoes = 0
    sum_entidade_fila = 0
    tempo_ocupado = 0
    tes = 0
    while(TR < tempo_maximo):
        if HC < HS: # Evento de chagada
            TR = HC
            if ES == 0:
                ES = 1
                tes = proximo_TES(tes_deterministico)
                HS = TR + tes
            else:
                TF += 1
            # (fila_finita and fila < TAMANHO_MAX_FILA or not fila_finita)
            HC = TR + proximo_TEC(tes_deterministico)

        else: # Evento de Saida  
            TR = HS
            if TF > 0:
                TF -= 1
                tes = proximo_TES(tes_deterministico)
                HS = TR + tes
            else:
                ES = 0
                HS = sys.maxint

        # atualiza estatistica
        interacoes += 1
        sum_entidade_fila += TF # Número Médio de Entidades nas Filas
        if ES == 1:
            tempo_ocupado += tes    # Taxa Média de Ocupação dos Servidores
        

        
        



    


'''
    - Gerar valores aleatorio [x]
    - Calcular o Tempo entre chegadas [x]
        - Deterministico: C
        - Aleatorio:  

'''