from ultralytics import YOLO
import cv2
import cvzone
import math
from ThreeCardsFunction import *

# For WebCam
capture = cv2.VideoCapture(0)  # 0 for single webcam
capture.set(3, 1280)  # Prop ID no 3 is for width
capture.set(4, 720)  # Prop ID no 4 is for height

model = YOLO("playingCards.pt")  # To create object model
classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']
resultArray = []  # Create an empty array
commonElements = []  # Create an empty array for common element

while True:
    success, img = capture.read()
    results = model(img, stream=True)  # Stream for video
    hand = []
    # Bordered Object in CVzone
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # x and y-axis then x=Width y= Height (box.xywy )
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert tensor values into Integer
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            # Class-name
            cls = int(box.cls[0])
            currentClass = classNames[cls] # {int(confidence * 100)}%
            cvzone.putTextRect(img, f'{currentClass}', (max(0, x1), max(35, y1)), scale=1,
                               thickness=2, font=cv2.FONT_HERSHEY_SIMPLEX)  # Classification by label

            if confidence > 0.5:
                hand.append(currentClass)

    hand = list(set(hand))

    if len(hand) == 3:
        results = findThreeCardsHand(hand)
        if results == ThreeCardsHandRanks[6]:
            resultArray.append(6)
        elif results == ThreeCardsHandRanks[5]:
            resultArray.append(5)
        elif results == ThreeCardsHandRanks[4]:
            resultArray.append(4)
        elif results == ThreeCardsHandRanks[3]:
            resultArray.append(3)
        elif results == ThreeCardsHandRanks[2]:
            resultArray.append(2)
        elif results == ThreeCardsHandRanks[1]:
            resultArray.append(1)

    print(resultArray)

    commonElements = []
    for element in resultArray:
        if element not in commonElements:
            commonElements.append(element)

    print("Common Elements: ", commonElements)

    if len(resultArray) >= 1:
        for i in range(len(commonElements)):
            cvzone.putTextRect(img,
                               f'Player({i + 1}) Hand is: {ThreeCardsHandRanks[commonElements[i]]}({commonElements[i]})',
                               (0, 40*(i+1)),
                               font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, thickness=2, colorT=(0, 0, 0),
                               colorR=(0, 255, 255))
            if commonElements[i] == max(commonElements):
                cvzone.putTextRect(img, f'The Winner is Player({i + 1})', (650, 40), font=cv2.FONT_HERSHEY_SIMPLEX,
                                   scale=1, thickness=2, colorT=(0, 0, 0),
                                   colorR=(0, 255, 0))
                cvzone.putTextRect(img,
                                   f'Winner Hand is: {ThreeCardsHandRanks[max(commonElements)]}({max(commonElements)})',
                                   (650, 80),
                                   font=cv2.FONT_HERSHEY_SIMPLEX, scale=1, thickness=2, colorT=(0, 0, 0),
                                   colorR=(0, 255, 0))
    cv2.imshow("Three Cards Hand Detector Agent", img)

    if cv2.waitKey(1) == 27 or cv2.getWindowProperty("Three Cards Hand Detector Agent", cv2.WND_PROP_VISIBLE) < 1:
        # Terminate by Esc button or Close Window
        break

capture.release()
cv2.destroyAllWindows()