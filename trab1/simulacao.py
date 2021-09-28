import math
import random
import numpy as np

N_CLASSES = 10
N_AMOSTRAS = 100

TEMPO_ENTRE_CHEGADA = 5
TEMPO_ENTRE_SERVICO = 5
TAMANHO_MAX_FILA = 10

def gera_amostras_exponencial(tam, param_lambda):
    amostras = []
    for i in range(0, tam):
        amostras.append(math.floor(np.random.exponential(param_lambda)))
    return amostras

def gera_valor_aleatorio(p_classe, classes):
    n_classes = len(p_classe)
    p = random.uniform(0, 1)
    for i in range(0, n_classes):   
        p -= p_classe[i]
        if p <= 0:
            return random.choice(classes[i])
    return random.choice(classes[-1])

# Gera funcao de distribuicao acumulada apartir das amostras dadas
def gera_funcao_distribuicao_acumulada(amostras = [], n_classes = 1):
    n_amostras = len(amostras)

    valor_max = max(amostras)
    valor_min = min(amostras)
    amplitude = valor_max - valor_min
    intervalo_classe = amplitude / n_classes

    classes = [[0] for i in range(0, n_classes)]
    p_classe = [0 for i in range(0, n_classes)]
    indice = 0
    
    for amostra in amostras:
        indice = math.floor(amostra / intervalo_classe)
        if(amostra == valor_max):
            indice = n_classes - 1

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

    if(not tec_deterministico):
        amostras_TEC = gera_amostras_exponencial(N_AMOSTRAS, TEMPO_ENTRE_CHEGADA)
        p_classe_TEC, classes_TEC = gera_funcao_distribuicao_acumulada(amostras_TEC, N_CLASSES)

    if(not tes_deterministico):
        amostras_TES = gera_amostras_exponencial(N_AMOSTRAS, TEMPO_ENTRE_SERVICO)
        p_classe_TES, classes_TES = gera_funcao_distribuicao_acumulada(amostras_TES, N_CLASSES)

    
    TR, ES, TF, HC, HS  = 0, 0, 0, 0, 99999
    cliente_saindo = 0
    clientes = 0

    interacoes = 0
    sum_entidade_fila = 0

    tempo_fila, tempo_ocupado, tempo_sistema = 0, 0, 0
    tr_anterior, tf_anterior, es_anterior = 0, 0, 0


    print("\n\nEvento", "Cliente", "TR", "ES", "TF", "HC", "HS")
    print("Inicio", "-", TR, ES, TF, HC, HS)
    while(TR < tempo_maximo):
        if HC < HS: # Evento de chagada
            TR = HC
            if not fila_finita or (fila_finita and TF < TAMANHO_MAX_FILA):
                clientes += 1
                print("Chegada", clientes, tr_anterior, ES, TF, HC, HS)
                if ES == 0:
                    ES = 1
                    HS = TR + proximo_TES(tes_deterministico)
                else:
                    TF += 1
            HC = TR + proximo_TEC(tes_deterministico)

        else: # Evento de Saida 
            cliente_saindo += 1
            print("Saida", cliente_saindo, tr_anterior, ES, TF, HC, HS)
            
            TR = HS
            if TF > 0:
                TF -= 1
                HS = TR + proximo_TES(tes_deterministico)
            else:
                ES = 0
                HS = 99999


        # atualiza estatistica
        interacoes += 1
        sum_entidade_fila += TF # Número Médio de Entidades nas Filas
        if ES == 1:
            tempo_ocupado += (TR - tr_anterior)   # Taxa Média de Ocupação dos Servidores
        tempo_fila += (TR - tr_anterior)*tf_anterior
        tempo_sistema += (TR - tr_anterior)*(tf_anterior + es_anterior)

        tr_anterior = TR
        tf_anterior = TF
        es_anterior = ES

    a = sum_entidade_fila / interacoes
    b = tempo_ocupado / TR
    c = tempo_fila / clientes
    d = tempo_sistema / clientes

    print("\n\nNúmero Médio de Entidades nas Filas: ", a)
    print("Taxa Média de Ocupação dos Servidores: ", b)
    print("Tempo Médio de uma Entidade na Fila: ", c)
    print("Tempo Médio no Sistema: ", d)

def main():
    global TEMPO_ENTRE_CHEGADA, TEMPO_ENTRE_SERVICO, TAMANHO_MAX_FILA
    
    continuar = True
    while(continuar):
        flag = True
        while(flag) :
            tec_deterministico = input("TEC é deterministico (S/N)? ") in ("S", "s")
            if tec_deterministico :
                TEMPO_ENTRE_CHEGADA = int(input("Insira o valor de TEC: "))
            else :
                TEMPO_ENTRE_CHEGADA = int(input("Defina o valor de lambda para TEC: "))

            tes_deterministico = input("TES é deterministico (S/N)? ") in ("S", "s")
            if tes_deterministico :
                TEMPO_ENTRE_SERVICO = int(input("Insira o valor de TES: "))
            else :
                TEMPO_ENTRE_SERVICO = int(input("Defina o valor de lambda para TES: "))
            
            if(TEMPO_ENTRE_CHEGADA < TEMPO_ENTRE_SERVICO):
                flag = False
            else:
                print("É necessário que o valor TEC seja MENOR que o valor TES (estado estacionário)")

        fila_finita = input("Fila é finita (S/N)? ") in ("S", "s")
        if fila_finita:
            TAMANHO_MAX_FILA = int(input("Tamanho máximo da fila: "))

        simulacao(100, tec_deterministico, tes_deterministico, fila_finita)

        continuar = input("\n\nDeseja continuar com outra simulacao(S/N)? ") in ("S", "s")

main()
