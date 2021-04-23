import numpy as np
from turtle import Pen, colormode, mainloop

class No:

    # Classe Nó para a busca A*
    # pai é o nó que gerou o nó atual
    # posição é a posição do nó no labirinto
    # g é o custo do nó inicial até o atual
    # h é a heuristica baseado na distancia do nó atual até o no final
    # f é o custo total do nó atual : f = g + h 
    def __init__(self, pai = None, posicao = None):
        self.pai = pai
        self.posicao = posicao

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, outro):
        return self.posicao == outro.posicao

# Está função retorna o caminho da busca
def retorna_caminho(no_atual, labirinto):

    caminho = []
    n_linhas, n_colunas = np.shape(labirinto)

    resultado = [[-1 for i in range(n_colunas)] for x in range(n_linhas)]

    atual = no_atual

    while atual is not None:
        caminho.append(atual.posicao)
        atual = atual.pai

    caminho = caminho[:: -1]
    valor_inicial = 0

    for i in range(len(caminho)):
        resultado[caminho[i][0]][caminho[i][1]] = valor_inicial
        valor_inicial += 1

    return resultado

#Retorna um lista de tuplas que são o caminho do nó inicial dado, até o nó final dado
def busca(labirinto, custo, inicio, fim):
    
    no_inicial = No(None, tuple(inicio))
    no_inicial.g = no_inicial.h = no_inicial.f = 0
    no_final = No(None, tuple(fim))
    no_final.g = no_final.h = no_final.f = 0

    para_visitar = []
    visitado = []
    

    para_visitar.append(no_inicial)

    ii = 0
    mi = (len(labirinto) // 2) ** 10

    movimentos = [[-1, 0 ], #cima
                  [ 0, -1], #esquerda
                  [ 1, 0 ], #baixo
                  [ 0, 1 ]] #direita
    

    n_linhas, n_colunas = np.shape(labirinto)

    while len(para_visitar) > 0:

        ii += 1

        no_atual = para_visitar[0]
        ind_atual = 0

        for ind, item in enumerate(para_visitar):

            if item.f < no_atual.f:
                no_atual = item
                ind_atual = ind


        #condição de parada
        if ii > mi:
            print("Muitas interações desistindo de achar o caminho")
            return retorna_caminho(no_atual, labirinto)
        

        para_visitar.pop(ind_atual)
        visitado.append(no_atual)


        #testa se não é o nó final
        if  no_atual == no_final:
            return retorna_caminho(no_atual, labirinto)

        filhos = []

        for nova_posicao in movimentos:


            posicao_no = (no_atual.posicao[0] + nova_posicao[0], no_atual.posicao[1] + nova_posicao[1])
            
            #testa se o nó está dentro do lábirinto
            if(posicao_no[0] > (n_linhas -1) or posicao_no[0] < 0 or posicao_no[1] > (n_colunas -1) or posicao_no[1] < 0):
               continue

            #testa se não é uma parede
            if labirinto[posicao_no[0]][posicao_no[1]] != 0:
                continue


            novo_no = No(no_atual, posicao_no)

            filhos.append(novo_no)

        for filho in filhos:
            

            #Testa se esse nó já foi visitado
            if len([filho_visitado for filho_visitado in visitado if filho_visitado == filho]) > 0:
                continue

            filho.g = no_atual.g + custo

            filho.h = (((filho.posicao[0] - no_final.posicao[0]) ** 2) + ((filho.posicao[1] - no_final.posicao[1]) ** 2))
            
            filho.f = filho.g + filho.h


            #Testa se esse filho já foi adicionado no lista mas com um custo menor
            if len([i for i in para_visitar if filho == i and filho.g > i.g]) > 0:
                continue

            para_visitar.append(filho)

def quadrado(ncor):
    colormode(255)
    cor = ncor
    if cor == 1:
        pen.fillcolor(255, 0, 0)
        pen.begin_fill()
    elif cor == 2:
        pen.fillcolor(0, 255, 0)
        pen.begin_fill()
    elif cor == 3:
        pen.fillcolor(0, 0, 255)
        pen.begin_fill()
    else:
        pen.fillcolor(105, 255, 255)
        pen.begin_fill()
    for i in range(4):
        pen.forward(50)
        pen.lt(90)
    pen.end_fill()

def desenharlab():
    pen.hideturtle()
    pen.speed('fastest')    
    pen.up()
    pen.setposition(0, 150)
    pen.down()

    for i, linha in enumerate(labirinto):
            pen.up()
            pen.goto(0, pen.position()[1] - 50)
            pen.down()
            for l,item in enumerate(linha):
                    if [i, l] == inicio:
                        quadrado(2)
                        pen.forward(50)
                    elif [i, l] == fim:
                        quadrado(3)
                        pen.forward(50)
                    else:
                        quadrado(item)
                        pen.forward(50)


def moveturt():
    turt = Pen()
    turt.shape("circle")
    turt.shapesize(1 / 2)
    turt.up()
    turt.goto((25 + (50* inicio[1])), (150 - (50 * inicio[0] + 25)))
    turt.down()

    x = 0
        
    while x <= np.max(caminho)  :
        for i, linha in enumerate(caminho):
            for l ,item in enumerate(linha):
                if item == x:
                    turt.goto(25 + (50*l),(150 - (50 * i + 25)))
                        
        x+=1



labirinto = [[0, 1, 0, 0, 0, 0, 1, 0],
             [0, 1, 0, 0, 0, 0, 1, 0],
             [0, 1, 0, 1, 1, 0, 1, 0],
             [0, 1, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]
    
inicio = [7, 0]
fim = [4,7]
custo = 1
caminho = busca(labirinto,custo, inicio, fim)

pen = Pen()

if caminho is not None:
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in col]) 
        for col in caminho]))

    desenharlab()
    moveturt()

else:
    print("Caminho não encontrado")
    pen.write("Caminho Não encontrado")

mainloop()
