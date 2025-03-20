import cv2, traceback, threading, queue, subprocess
import numpy as np
from utils.coco_utils import COCO_test_helper
from utils.rknn_executor import RKNN_model_container
from utils.process import *

VIDEO_SIZE = (1080, 720) #(640, 512)
ffmpeg_command = [
    'ffmpeg',
    '-y',  # Overwrite output files without asking
    '-f', 'rawvideo',  # Input format: raw video
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24',  # Pixel format (OpenCV uses BGR)
    '-s', f'{VIDEO_SIZE[0]}x{VIDEO_SIZE[1]}',  # Video resolution
    '-r', "30",  # Frame rate
    '-i', '-',  # Input from stdin
    '-c:v', 'libx264',  # Video codec #h264_rkmpp #libx264
    '-tune', 'zerolatency',
    '-b:v', '5M',
    '-preset', 'ultrafast',  # Encoding speed
    '-pix_fmt', 'yuv420p',  # Output pixel format
    '-f', 'rtsp',  # Output format: RTSP
    "rtsp://localhost:8554/stream"  # RTSP server URL
]

TARGET = "rk3588"
RKNN_MODEL = "./model/yolov5.rknn"
LABEL = './model/yolov5.txt'

def main():
    model = RKNN_model_container(RKNN_MODEL, TARGET, None)
    co_helper = COCO_test_helper(enable_letter_box=True)

    with open(LABEL, 'r') as f:
        values = [float(_v) for _v in f.readlines()]
        anchors = np.array(values).reshape(3,-1,2).tolist()

    process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    cap = cv2.VideoCapture("/dev/video12")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = co_helper.letter_box(im= frame.copy(), new_shape=(IMG_SIZE[1], IMG_SIZE[0]), pad_color=(0,0,0))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        outputs = model.run([img])
        boxes, classes, scores = post_process(outputs, anchors)
        img_p = frame.copy()
        if boxes is not None:
            draw(img_p, co_helper.get_real_box(boxes), scores, classes)
            # cv2.imwrite("result.jpg", img_p)
        
        if img_p.shape[1] != VIDEO_SIZE[0] or img_p.shape[0] != VIDEO_SIZE[1]:
            img_p = cv2.resize(img_p, VIDEO_SIZE)
        process.stdin.write(img_p.tobytes())

        # cv2.imshow("image", img_p)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()