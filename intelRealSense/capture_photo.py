import pyrealsense2 as rs
import numpy as np
import cv2
import keyboard

# data label
numbers=['0','1','2','3','4','5','6','7','8','9']
numbers_index=0
distance=['10cm','15cm','20cm','25cm','30cm']
distance_index=0
degree=['+45deg','+30deg','+15deg','0deg','-15deg','-30deg','-45deg']
degree_index=0


def photo_status(toShow: str):

    # Manual text
    manual1 = "keypad : number, Q ~ T : distance, A ~ J : degree"
    manual2 = "Space : capture, ESC : quit"

    # Create a black image
    backGround = np.zeros((128,512,3), np.uint8)

    # Define the text settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (10, 50)  # Bottom-left corner of the text string in the image
    fontScale = 1
    fontColor = (255,255,255)  # White color
    lineType = 2

    # Put the text on the screen
    image = cv2.putText(backGround, toShow, position, font, fontScale, fontColor, lineType)

    # Put the manual on the screen
    position = (10, 80)
    fontScale = 0.5
    image = cv2.putText(image, manual1, position, font, fontScale, fontColor, lineType)
    position = (10, 100)
    image = cv2.putText(image, manual2, position, font, fontScale, fontColor, lineType)


    # Display the image
    cv2.imshow("file status", image)

def change_status():
    global numbers, distance, degree,numbers_index,distance_index,degree_index
    # key maps
    distance_map = ['q','w','e','r','t']
    degree_map = ['a','s','d','f','g','h','j']
    # Change the status
    for i in range(10):
        if keyboard.is_pressed(str(i)):
            numbers_index = i
    for i in range(5):
        if keyboard.is_pressed(distance_map[i]):
            distance_index = i
    for i in range(7):
        if keyboard.is_pressed(degree_map[i]):
            degree_index = i

def capture_photo():
    global numbers, distance, degree
    # Configure realsense color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    # file name
    
    try:
        while True:
            # Change the status
            change_status()
            fileName="Data/"+numbers[numbers_index]+"/"+distance[distance_index]+"_"+degree[degree_index]+".png"
            # show the status
            photo_status(fileName)

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())

            # Show images
            cv2.imshow('RealSense', color_image)
            cv2.waitKey(1)

            # Save images
            if keyboard.is_pressed('space'):
                print("Save the image: ",fileName)
                cv2.imwrite(fileName, color_image)

            # Quit
            if keyboard.is_pressed('esc'):
                break


    finally:
        pipeline.stop()
        


capture_photo()
cv2.destroyAllWindows()
