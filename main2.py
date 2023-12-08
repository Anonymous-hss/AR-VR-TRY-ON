import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)  # 0 or 1
detector = PoseDetector()

clothFolderPath = "Resources/Clothes"
listClothes = os.listdir(clothFolderPath)
print(listClothes)

fixedRatio = 262 / 190  # widthcloth/widthPoints 11 to 12
clothRatioHeightWidth = 581 / 440

imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

    if lmList:
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgCloth = cv2.imread(os.path.join(clothFolderPath, listClothes[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfCloth = int((lm11[0] - lm12[0]) * fixedRatio)
        imgCloth = cv2.resize(imgCloth, (widthOfCloth, int(widthOfCloth * clothRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = (int(44 * currentScale), int(48 * currentScale))

        try:
            h, w, c = imgCloth.shape
            imgClothResized = cv2.resize(imgCloth, (w + offset[0], h + offset[1]))
            imgRGB = imgClothResized[:, :, :3]
            imgMask = imgClothResized[:, :, 3:]

            img[pos[1]:pos[1] + h, pos[0]:pos[0] + w, :] = imgRGB
            img = imgMask * img + (1 - imgMask) * img
        except:
            pass

        # Adjust the button positions
        button_right_pos = (1074, 293)
        button_left_pos = (72, 293)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
