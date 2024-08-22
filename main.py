import cv2
import math
import random

# Initialize video capture
vid = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('trainedMl.xml')

# Initialize X, Y coordinates
X, Y = 10, 10
movX, movY = 650, math.floor(480 / 2)
spriteX, spriteY = 0, 10
obstacleHeight = 200

# Define a callback function to update the cursor location
def print_cursor_location(event, x, y, flags, param):
    global X, Y
    if event == cv2.EVENT_MOUSEMOVE:
        X = x
        Y = y

# Create a window and bind the callback function to it
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', print_cursor_location)

while True:
    ret, frame = vid.read()
    height, width, _ = frame.shape
    movY = height - obstacleHeight

    # Draw a rectangle on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        # Face tracker - sprite
        spriteX = x
        spriteY = y
        cv2.rectangle(frame, (x, y), (x + 100, y + 100), (0, 255, 0), -1)

    # Draw the obstacle
    cv2.rectangle(frame, (movX, movY), (movX + 100, height), (0, 255, 255), -1)

    movX -= 10  # Move the obstacle to the left
    if movX < 0:
        movX = 650
        obstacleHeight = random.randint(0, math.floor(height / 2))

    # Check for collision
    if (spriteY>=movY  and spriteX>=movX and spriteX<=movX+100 ):
        print("Game Over")
        break

    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
vid.release()
cv2.destroyAllWindows()
