# Kütüphaneler
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

# Telefon kamerası
cap = cv2.VideoCapture("http://192.168.1.44:8080/video")

# El bulmak kullanılan modül
detector = HandDetector(detectionCon=0.8)

# Harf kutuları(kareler) için kullanacağımız alfabe listesi
# 3 liste halinde
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
finalText = ""

def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + h, y + h), (255, 0, 255), cv2.FILLED)  # mor kutu
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)  # beyaz harf
    return img

# Harflerin listesi
class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos= pos
        self.size = size
        self.text = text
buttonList = []

# Harf kutuların(karelerin) listesi
# 3 listeyi almak için for döngüsü kullanıyoruz
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img=cap.read()
    img= detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img) # Eli bulmak için

    img = drawALL(img, buttonList)

    # Elimiz var mı yok mu kontrolü (?)
    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            # HandDetector modülüne göre el noktaların seçimi
            if x<lmList[5][0]<x+w and y<lmList[5][1]<y+h:
                cv2.rectangle(img, button.pos, (x + h, y + h), (175, 0, 175), cv2.FILLED)  # koyu mor renk
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)

                # Seçilen nokta uzaklığına göre tıklama yapma
                l,_,_=detector.findDistance(5,8,img,draw=False)
                print(l)

                # Tıklandığı zaman
                if l<30:
                    cv2.rectangle(img, button.pos, (x + h, y + h), (0, 255, 0), cv2.FILLED)  # yeşil renk
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),4)
                    finalText += button.text
                    sleep(0.5)

    # Metin kutusu oluşturma
    cv2.rectangle(img, (50,350), (700,450), (175,0,175), cv2.FILLED)  # koyu mor renk
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # q tuşuyla kameradan çıkış yapılır
    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
