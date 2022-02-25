import cv2
# o cvzone permite fazer track nas mão é o que vamos usar para controlar objetos
from cvzone.HandTrackingModule import HandDetector

#inicia a camera
cap = cv2.VideoCapture(0)

#configurações do cvzone
detector = HandDetector(detectionCon=0.8)

# cor do quadrado inicial
colorR = (244, 0, 144)

# controlador
cx, cy, w, h = 40, 40, 100, 100

# enquanto verdadeiro a camera é iniciada
while True:
    succes, img = cap.read()
    img = cv2.flip(img, 0)
    #usando o cvzone para detectar mãos no video
    # usando o video invertido verticalmente
    maos, img = detector.findHands(img, flipType=False)

    #analisando a posição da mão
    lmList, _ = detector.findPosition(img)

    #aplicando um check de dedos
    if lmList:
        #analisando a distancia entre os dedos para função de pegar e soltar
        l, _, _ = detector.findDistance(8, 12, img=img)
        print(l)#distancia entre os dedos para simular o click, ajustar conforme a necessidade da distancia da camera
        if l < 25:
            # numero do ponto do dedo <- ver a documentação do mediapipe
            cursor = lmList[8]
            if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                # caso o dedo esteja no centro do retangulo colorir o retangulo
                colorR = (0, 0, 244)
                # aplicando a posição do dedo ao retangulo
                cx, cy = cursor
            else:
                colorR = (244, 0, 144)

    #pondo blocos na tela para interação
    #lembrando que pode ser outras coisas como teclas
    cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)

    cv2.imshow("trak", img)
    cv2.waitKey(1)