import cv2
import numpy as np
# o cvzone permite fazer track nas mão é o que vamos usar para controlar objetos
from cvzone.HandTrackingModule import HandDetector
import cvzone

# inicia a camera
cap = cv2.VideoCapture(0)
cap.set(3, 750)
cap.set(4, 450)
# configurações do cvzone
detector = HandDetector(detectionCon=0.8)

# cor do quadrado inicial
colorR = (244, 0, 144)

# controlador
cx, cy, w, h = 40, 40, 100, 100

# 2 parte cirando uma classe para trabalhar com multiplos objetos

class DragRect():
    def __init__(self, posicaoCentral, tamanho=None):
        if tamanho is None:
            tamanho = [100, 100]
        self.posicaoCentral = posicaoCentral
        self.tamanho = tamanho

    def atualiza(self, cursor):
        cx, cy = self.posicaoCentral
        w, h = self.tamanho

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            # caso o dedo esteja no centro do retangulo colorir o retangulo
            colorR = (0, 0, 244)
            # aplicando a posição do dedo ao retangulo
            self.posicaoCentral = cursor

# parte 2 multiplos objetos
rectLista = []
for x in range(5):
    rectLista.append(DragRect([x * 150 + 50, 50]))

# enquanto verdadeiro a camera é iniciada
while True:
    succes, img = cap.read()
    # usando o cvzone para detectar mãos no video
    # usando o video invertido verticalmente
    maos, img = detector.findHands(img, flipType=False)

    # analisando a posição da mão
    lmList, _ = detector.findPosition(img)

    # aplicando um check de dedos
    if lmList:
        # analisando a distancia entre os dedos para função de pegar e soltar
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)  # distancia entre os dedos para simular o click, ajustar conforme a necessidade da distancia da camera
        if l < 25:
            # numero do ponto do dedo <- ver a documentação do mediapipe
            cursor = lmList[8]
            # parte 2 chamando o atualiza aqui
            for rect in rectLista:
                rect.atualiza(cursor)

    # parte 2 para outros tipos de objetos
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectLista:
        # parte 2 atribuido objeto na tela
        cx, cy = rect.posicaoCentral
        w, h = rect.tamanho
        # lembrando que pode ser outras coisas como teclas
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        # parte 2 marcadores do retangulo
        cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    saida = img.copy()
    tranparencia = 0.4
    mascara = imgNew.astype(bool)
    saida[mascara] = cv2.addWeighted(img, tranparencia, imgNew, 1 - tranparencia, 0)[mascara]

    #criação da tela de video
    cv2.imshow("trak", saida)
    cv2.waitKey(1)
