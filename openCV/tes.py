import cv2 as cv

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def changeRes(width, height):
    # Only works for live videos
    capture.set(3, width)
    capture.set(4, height)

capture = r'Videos/randomWindows7.mp4'

fullColor = cv.imread(capture)
greyColor = cv.cvtColor(fullColor, cv.COLOR_BGR2GRAY)

while True:
    isTrue, frame = greyColor.read()

    frame_resized = rescaleFrame(frame)

    cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()