import pyrealsense2 as rs
import numpy as np
import cv2
import keyboard

# data label
numbers=['0','1','2','3','4','5','6','7','8','9']
distance=['10cm','15cm','20cm','25cm','30cm']
degree=['+45deg','+30deg','+15deg','0deg','-15deg','-30deg','-45deg']


def photo_status(toShow: str):

    # Manual text
    manual1 = "A : number, S : distance, D : degree"
    manual2 = "Space : capture, Q : quit"

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

def capture_photo():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    # Stack both images horizontally
    images = np.hstack((color_image, depth_colormap))

    # Show images
    cv2.imshow('RealSense', images)

    # Save images
    cv2.imwrite("4000LUX_10cm_-15deg.jpg", images)

    # Stop streaming
    pipeline.stop()

for i in range(3):
    photo_status("4000LUX_10cm_-15deg")
    cv2.waitKey(0)
    


cv2.destroyAllWindows()
