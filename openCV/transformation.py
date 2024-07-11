import cv2 as cv
import numpy as np

img = cv.imread("photos\catWine.jpg")
cv.imshow('Gentleman', img)

# TRANSLATION
def translate (img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

# # -x --> Left
# # -y --> Up
# # x --> Right
# # y --> Down

translated = translate(img, 100, 100)
cv.imshow('Translated', translated)

# ROTATION
def rotate(img, angle, rotPoint=None):
    (height,width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2,height//2)
    
    roMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, roMat, dimensions)

rotated = rotate(img, 45)
cv.imshow("Rotated", rotated)

rotated_rotated = rotate(rotated, 45)
cv.imshow("Rotated rotated", rotated_rotated)

# Resizing
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC) # INTER_AREA=Shrinking image, INTER_LINEAR=Enlarge image, INTER_CUBIC=Enlarge image slower but higher result
cv.imshow("Resized", resized)

# FLIPPING
flip = cv.flip(img, 0) # 0=Flip horizontally, 1=Flip vertically, -1=Flip horizontally+vertically
cv.imshow("Flip", flip)

# CROPPING
cropped = img[200:600, 300:900]
cv.imshow("Croppped", cropped)

cv.waitKey(0)