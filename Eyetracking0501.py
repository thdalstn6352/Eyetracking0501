"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import time
import threading
import cv2
import numpy as np
from gaze_tracking import GazeTracking

webcam = cv2.VideoCapture(0)
R_top = 0
L_top = 0
C_top = 0

R_bottom = 0
L_bottom = 0
C_bottom = 0

avg_top_right = 0
avg_top_left = 0
avg_bottom_right = 0
avg_bottom_left = 0
avg_top_center = 0
avg_bottom_center = 0

total_left_hor_gaze = 0
total_right_hor_gaze = 0
total_top_ver_gaze = 0
total_bottom_ver_gaze = 0

sectionA =0
sectionB =0
sectionC =0
sectionD =0
sectionE =0
sectionF =0

section = "None"

count = 1
test_count = 1
flag = 0
gaze = GazeTracking()


def Section(where):
        global sectionA, sectionB, sectionC, sectionD, sectionE, sectionF
        if where == "A":
            sectionA += 1
            return sectionA
        elif where == "B":
            sectionB += 1
            return sectionB
        elif where == "C":
            sectionC += 1
            return sectionC
        elif where == "D":
            sectionD += 1
            return sectionD
        elif where == "E":
            sectionE += 1
            return sectionE
        elif where == "F":
            sectionF += 1
            return sectionF


def Thread_run():
    if section != "None":
        print(section, ":", Section(section))
    thread = threading.Timer(1, Thread_run)
    thread.daemon = True
    thread.start()


Thread_run()

while True:
    _, frame = webcam.read()
    new_frame = np.zeros((500, 500, 3), np.uint8)

    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    text = ""

    if test_count < 50:
        cv2.circle(frame, (25, 25), 25, (0, 0, 255), -1)
        if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
            total_left_hor_gaze += gaze.horizontal_ratio()
            total_top_ver_gaze += gaze.vertical_ratio()
            test_count += 1

    elif 50 <= test_count < 100:
        cv2.circle(frame, (610, 25), 25, (0, 0, 255), -1)
        if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
            total_right_hor_gaze += gaze.horizontal_ratio()
            total_top_ver_gaze += gaze.vertical_ratio()
            test_count += 1

    elif 100 <= test_count < 150:
        cv2.circle(frame, (25, 450), 25, (0, 0, 255), -1)
        if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
            total_left_hor_gaze += gaze.horizontal_ratio()
            total_bottom_ver_gaze += gaze.vertical_ratio()
            test_count += 1

    elif 150 <= test_count < 200:
        cv2.circle(frame, (610, 450), 25, (0, 0, 255), -1)
        if gaze.horizontal_ratio() != None and gaze.vertical_ratio() != None:
            total_right_hor_gaze += gaze.horizontal_ratio()
            total_bottom_ver_gaze += gaze.vertical_ratio()
            test_count += 1
    else:
        if flag == 0:
            avg_left_hor_gaze = total_left_hor_gaze / 100
            avg_right_hor_gaze = total_right_hor_gaze / 100
            avg_top_ver_gaze = total_top_ver_gaze / 100
            avg_bottom_ver_gaze = total_bottom_ver_gaze / 100
            print(avg_left_hor_gaze, avg_right_hor_gaze, avg_top_ver_gaze, avg_bottom_ver_gaze)
            flag = 1

        if gaze.is_blinking():
            text = "Blinking"

        if gaze.is_top_right(avg_right_hor_gaze, avg_top_ver_gaze):
            new_frame[:] = (0, 200, 227)
            text = "Looking top right"
            section = "A"
        elif gaze.is_top_left(avg_left_hor_gaze, avg_top_ver_gaze):
            new_frame[:] = (0, 0, 255)
            text = "Looking top left"
            section = "B"
        elif gaze.is_bottom_right(avg_right_hor_gaze, avg_top_ver_gaze):
            new_frame[:] = (255, 0, 170)
            text = "Looking bottom right"
            section = "C"
        elif gaze.is_bottom_left(avg_left_hor_gaze, avg_top_ver_gaze):
            new_frame[:] = (0, 255, 0)
            text = "Looking bottom left"
            section = "D"
        elif gaze.is_top_center(avg_top_ver_gaze, avg_right_hor_gaze, avg_left_hor_gaze):
            new_frame[:] = (0, 104, 250)
            text = "Looking top center"
            section = "E"
        elif gaze.is_bottom_center(avg_top_ver_gaze, avg_right_hor_gaze, avg_left_hor_gaze):
            new_frame[:] = (255, 0, 0)
            text = "Looking bottom center"
            section = "F"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("New Frame", new_frame)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break

total_gaze = R_top + L_top + C_top + R_bottom + L_bottom + C_bottom

print("Total Ratio: A:", sectionA, " B:", sectionB, "C:", sectionC, "D:", sectionD, "E:", sectionE, "F:", sectionF)
cv2.destroyAllWindows()
