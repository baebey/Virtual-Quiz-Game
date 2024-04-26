import cv2
import csv
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
detector = HandDetector(staticMode=False, maxHands=200, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)


class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)



pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]


mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))

print("Total MCQ Objects Created:", len(mcqList))

qNo = 0
qTotal = len(dataAll)


while True:
    point = 0
    choice1 = 0
    choice2 = 0
    choice3 = 0
    choice4 = 0

    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    cv2.putText(img, "student : " + str(len(hands)), (1000, 70), 
        cv2.FONT_HERSHEY_COMPLEX, 1.25, 
        (0, 255, 0), 4)

    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 4, 3, offset=20, border=2)
        img, bbox1 = cvzone.putTextRect(img, '1.'+ mcq.choice1, [100, 175], 2, 2, offset=20, border=2)
        img, bbox2 = cvzone.putTextRect(img, '2.' + mcq.choice2, [380, 175], 2, 2, offset=20, border=2)
        img, bbox3 = cvzone.putTextRect(img, '3.' + mcq.choice3, [660, 175], 2, 2, offset=20, border=2)
        img, bbox4 = cvzone.putTextRect(img, '4.' + mcq.choice4, [940, 175], 2, 2, offset=20, border=2)

        if hands:
            num = len(hands)
            for i in range(num):
                hand = hands[i]
                lmList = hand["lmList"]
                bbox = hand["bbox"]
                conter = hand["center"]
                handType = hand["type"]

                fingers = detector.fingersUp(hand)

                if fingers.count(1) == mcq.answer:
                    point += 1  
                if fingers.count(1) == 1:
                    choice1 += 1
                if fingers.count(1) == 2:
                    choice2 += 1
                if fingers.count(1) == 3:
                    choice3 += 1
                if fingers.count(1) == 4:
                    choice4 += 1
                if fingers.count(1) == 0:
                    time.sleep(1)
                    qNo += 1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score / qTotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [500, 300], 2, 2, offset=50, border=5)

        if hands:
            num = len(hands)
            for i in range(num):
                hand = hands[i]
                lmList = hand["lmList"]
                bbox = hand["bbox"]
                conter = hand["center"]
                handType = hand["type"]

                fingers = detector.fingersUp(hand)
                print(f'H{i} = {fingers.count(1)}', end=" ")

                if fingers.count(1) == 5:
                    time.sleep(0.5)
                    qNo = 0
    
    cv2.putText(img, "correct : " + str(point) + "/" +  str(len(hands)), (650, 70), 
        cv2.FONT_HERSHEY_COMPLEX, 1.25, 
        (0, 255, 0), 4)
    
    cv2.putText(img, "answer 1 : " + str(choice1), (60, 700), 
        cv2.FONT_HERSHEY_COMPLEX, 1,
        (0, 255, 0), 2)
    
    cv2.putText(img, "answer 2 : " + str(choice2), (320, 700), 
        cv2.FONT_HERSHEY_COMPLEX, 1,
        (0, 255, 0), 2)
    
    cv2.putText(img, "answer 3 : " + str(choice3), (620, 700), 
        cv2.FONT_HERSHEY_COMPLEX, 1,
        (0, 255, 0), 2)
    
    cv2.putText(img, "answer 4 : " + str(choice4), (920, 700), 
        cv2.FONT_HERSHEY_COMPLEX, 1,
        (0, 255, 0), 2)


    cv2.imshow("To Be No.0", img)
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break
