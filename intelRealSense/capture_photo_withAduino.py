import pyrealsense2 as rs
import numpy as np
import cv2
import keyboard
import time
import serial



# Arduino serial port
PORT = 'COM3'
BAUDRATE = 9600
arduino = serial.Serial(port=PORT,baudrate=BAUDRATE)


# data label
numbers=['0','1','2','3','4','5','6','7','8','9']
numbers_index=0
distance=['0cm','5cm','10cm','15cm','20cm','25cm','30cm','35cm','40cm','45cm','50cm','55cm','60cm','65cm','70cm','75cm','80cm','85cm','90cm']
distance_index=0
distance_sw=True
degree=['-90deg','-80deg','-70deg','-60deg','-50deg','-40deg','-30deg','-20deg','-10deg','0deg','+10deg','+20deg','+30deg','+40deg','+50deg','+60deg','+70deg','+80deg','+90deg']
degree_index=0
degree_sw=True
brightness=['LOW','MID','HIGH']
brightness_index=0
brightness_sw=True

def send_command(command):
    try:
        # Send the command to the arduino
        arduino.write(command.encode()) 
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending command: {e}")


def photo_status(toShow: str):

    # Manual text
    manual1 = "keypad : number, distance : Q,E degree : A,D brightness : Z,C"
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
    global numbers, distance, degree,numbers_index,distance_index,degree_index,distance_sw,degree_sw,brightness,brightness_index,brightness_sw,arduino
    
    # Change the status
        # Change the number
    for i in range(10):
        if keyboard.is_pressed(str(i)):
            numbers_index = i
        # Change the distance
    if keyboard.is_pressed('e'):
        if distance_sw:
            distance_index = (distance_index + 1)%len(distance)
            distance_sw = False
    elif keyboard.is_pressed('q'):
        if distance_sw:
            distance_index = (distance_index - 1)
            if distance_index < 0:
                distance_index = len(distance)-1
            distance_sw = False
    else:
        distance_sw = True
        # Change the degree
    if keyboard.is_pressed('d'):
        if degree_sw:
            
            if (degree_index == len(degree)-1):
                arduino.write('r'.encode())
                degree_index = 0
            else:
                arduino.write('s'.encode())
                degree_index = (degree_index + 1)
            degree_sw = False
    elif keyboard.is_pressed('a'):
        if degree_sw:
            
            if degree_index == 0:
                arduino.write('r'.encode())
                degree_index = len(degree)-1
            else:
                arduino.write('b'.encode())
                degree_index = (degree_index - 1)
            degree_sw = False
    else:
        degree_sw = True
        # Change the brightness
    if keyboard.is_pressed('c'):
        if brightness_sw:
            brightness_index = (brightness_index + 1)%len(brightness)
            brightness_sw = False
    elif keyboard.is_pressed('z'):
        if brightness_sw:
            brightness_index = (brightness_index - 1)
            if brightness_index < 0:
                brightness_index = len(brightness)-1
            brightness_sw = False
    else:
        brightness_sw = True


def capture_photo():
    global numbers, distance, degree
    # Configure realsense color treams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    #config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    # file name
    
    try:
        n_sw=True
        i_sw=True
        while True:
            # Change the status
            change_status()
            fileName="Data/"+numbers[numbers_index]+"/"+distance[distance_index]+"_"+degree[degree_index]+"_"+brightness[brightness_index]+".png"
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

            # Quick process (next)
            if keyboard.is_pressed('n'):
                if(degree_index == 0) and n_sw:
                    n_sw = False
                    for i in range(len(degree)-1):
                        fileName="Data/"+numbers[numbers_index]+"/"+distance[distance_index]+"_"+degree[i]+"_"+brightness[brightness_index]+".png"
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

                        cv2.imwrite(fileName, color_image)
                        arduino.write('s'.encode())
                        time.sleep(7)
                    
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

                    fileName="Data/"+numbers[numbers_index]+"/"+distance[distance_index]+"_"+degree[len(degree)-1]+"_"+brightness[brightness_index]+".png"
                    cv2.imwrite(fileName, color_image)
                    arduino.write('r'.encode())
                    print("Save the image: ",fileName)
            else:
                n_sw = True

            # Degree check
            if(keyboard.is_pressed('i')):
                if i_sw:
                    i_sw = False
                    arduino.write('i'.encode())
            else:
                i_sw = True
                

            # Quit
            if keyboard.is_pressed('esc'):
                break


    finally:
        pipeline.stop()
        

capture_photo()
cv2.destroyAllWindows()
