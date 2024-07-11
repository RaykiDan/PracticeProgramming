import cv2 as cv

img = cv.imread('photos/catWine.jpg')
cv.imshow('Gentleman', img)

# Converting to grayscale
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('Vintage', gray)

# Blur
blur = cv.GaussianBlur(img, (5,5), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

# Edge Cascade
canny = cv.Canny(blur, 125, 175)
cv.imshow('Cascade', canny)

# Dilating the Image
# dilated = cv.dilate(canny, (7,7), iterations=3)
# cv.imshow('Dilated', dilated)

# Eroding
# eroded = cv.erode(dilated, (7,7), iterations=3)
# cv.imshow('Eroded', eroded)

# Resizing
# resize = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)
# cv.imshow('Resize', resize)

# Cropping
cropped = img[300:500, 300:500]
cv.imshow('Cropped', cropped)

cv.waitKey(0)