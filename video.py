import cv2
import numpy as np
import time


cap = cv2.VideoCapture(1)


def film():
    print('begin filming')
    ret, frame = cap.read()
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)

    result = cv2.VideoWriter('filename.avi',
                             cv2.VideoWriter_fourcc(*'XVID'),
                             30, size)
    start_time = time.time()
    while (int(time.time() - start_time) < 5):
        ret, frame = cap.read()
        result.write(frame)

    # Release everything if job is finished
    result.release()
    cv2.destroyAllWindows()

    print("The video was successfully saved")



def wait_and_detect():
    while True:
        if detect_motion(cap):
            film()


def detect_motion(cam):
    is_odd = False
    prev_frame = None
    while(True):
        is_odd = ~is_odd
        ret, frame = cam.read()
        img = np.array(frame)
        if is_odd:
            prepared_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)

            if prev_frame is None:
                prev_frame = prepared_frame
                continue

            diff_frame = cv2.absdiff(src1=prev_frame, src2=prepared_frame)
            prev_frame = prepared_frame

            kernel = np.ones((5, 5))
            diff_frame = cv2.dilate(diff_frame, kernel, 1)

            thresh_frame = cv2.threshold(src=diff_frame, thresh=30, maxval=255, type=cv2.THRESH_BINARY)[1]
            if np.any(thresh_frame):
                return 1


wait_and_detect()