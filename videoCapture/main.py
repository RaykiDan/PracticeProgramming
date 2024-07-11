import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Output.mp4', fourcc, 20.0, (640,480))

while (cap.isOpened()):
    ret, frame = cap.read()
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if (ret==True):
        # copy video window to multiple video
        # smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        # image = np.zeros(frame.shape, np.uint8)
        # image[:height//2, :width//2] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
        # image[height//2:, :width//2] = smaller_frame
        # image[:height//2, width//2:] = cv2.rotate(smaller_frame, cv2.ROTATE_180)
        # image[height//2:, width//2:] = smaller_frame

        cv2.imshow('frame', frame) # change variable 'frame' to 'image' if wanna show multiple videos

        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
    
    else:
        break

cap.release()
cv2.destroyAllWindows