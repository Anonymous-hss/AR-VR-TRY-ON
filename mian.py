import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0) #0 or 1
cap.set(3, 1760)
cap.set(4, 1080)
detector = PoseDetector()


clothFolderPath = "Resources/Clothes"
listClothes = os.listdir(clothFolderPath)
print(listClothes)
fixedRatio = 262/190 #widthcloth/widthPoints 11 t0 12 
clothratioHeightWidth = 581/440

imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight,1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img  = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgCloth = cv2.imread(os.path.join(clothFolderPath,listClothes[imageNumber]),cv2.IMREAD_UNCHANGED)

        widthOfCloth = int((lm11[0]-lm12[0])*fixedRatio)
        print(widthOfCloth)
        imgCloth = cv2.resize(imgCloth,(widthOfCloth, int(widthOfCloth*clothratioHeightWidth)))
        currentScale = (lm11[0]-lm12[0])/190
        offset = int(44 * currentScale),int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img,imgCloth,(lm12[0]-offset[0],lm12[1]-offset[1]))
        except:
            pass
        
        imgButtonRight1 = cv2.resize(imgButtonRight,(0,0),None,0.2,0.2)
        imgButtonLeft1 = cv2.resize(imgButtonRight,(0,0),None,0.2,0.2)

        
        try:
            cvzone.overlayPNG(img,imgButtonRight1,(1274,293))
            cvzone.overlayPNG(img,imgButtonLeft1,(42,293))
        except:
            pass
        # ,(1074,293))
        # ,(72,293))
 

        # cvzone.overlayPNG(img,imgButtonRight1,(1374,293))
        # cvzone.overlayPNG(img,imgButtonLeft1,(42,293))

        if lmList[16][1] < 300:
            counterRight+=1
            cv2.ellipse(img,(139,360),(66,66),0,0,counterRight*selectionSpeed,(0.255,0),20)
            if counterRight*selectionSpeed>360:
                counterRight = 0
                if imageNumber < len(listClothes)-1:
                    imageNumber+=1
        elif lmList[15][1]>900:
            counterLeft+=1
            cv2.ellipse(img,(1138,360),(66,66),0,0,counterLeft*selectionSpeed,(0.255,0),20)
            if counterLeft*selectionSpeed>360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber-=1
        else:
            counterRight = 0
            counterLeft =0

        #center = bboxInfo["center"]
        #cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
    cv2.imshow("Image", img)
    cv2.waitKey(1)