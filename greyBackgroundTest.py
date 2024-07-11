# Contoh pengolahan citra

import cv2

path = r'C:/Users/ASUS/Documents/College/FTDC/Latihan/baboon.png'
citraRGB = cv2.imread(path)
citraAbu2 = cv2.cvtColor(citraRGB, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gambar berwarna', citraRGB)
cv2.imshow('Gambar berskala keabu-abuan', citraAbu2)
cv2.waitKey(0)
cv2.destroyAllWindows()