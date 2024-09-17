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
pushUpCount=0
health=4
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

    font = cv2.FONT_HERSHEY_SIMPLEX
    


    # Draw a rectangle on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        # Face tracker - sprite
        spriteX = x
        spriteY = y
        cv2.rectangle(frame, (x, y), (x + 100, y + 100), (0, 255, 0), -1)

    # Draw the obstacle
        image= cv2.rectangle(frame, (movX, movY), (movX + 100, height), (0, 255, 255), -1)
        cv2.putText(image, str(pushUpCount), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        movX -= 10  # Move the obstacle to the left

    if movX < 0:
        movX = 650
        obstacleHeight = random.randint(100, math.floor(height / 2))
        pushUpCount=pushUpCount+1

    # Check for collision
    if (spriteY>=movY-100  and spriteX>=movX-90 and spriteX<=movX+100 ):
        pushUpCount=0
        health= health-1
        
        print("Game Over")
        frame= cv2.putText(frame, str("Ouch") ,(200,151), font, 1,(0,0,255),2,cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if(health<=0):
            
            frame= cv2.putText(frame, str("Game Over") ,(200,151), font, 1,(0,0,255),2,cv2.LINE_AA)
            break
        # continue
        # cv2.imshow('frame', cv2.putText(image, 'OpenCV', cv2.LINE_AA))
        
    frame= cv2.putText(frame, str(f'PushUps:{pushUpCount}') ,(0,40), font, 1,(0,0,255),1,cv2.LINE_AA)
    frame= cv2.putText(frame, str(f'Health:{health}') ,(0,80), font, 1,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
vid.release()
cv2.imshow('frame', frame)
cv2.destroyAllWindows()
