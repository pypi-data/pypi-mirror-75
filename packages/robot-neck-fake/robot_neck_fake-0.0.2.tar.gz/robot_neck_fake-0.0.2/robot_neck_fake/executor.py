import cv2
from robot_core.executor.executor import Executor


class FakeNeckExecutor(Executor):
    # Start Capture
    cap = cv2.VideoCapture(1)

    # Get frame dimensions
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def execute(self, **kwargs):
        if kwargs["command"] == "up":
            return self.up()
        elif kwargs["command"] == "down":
            return self.down()

        if kwargs["src"] is not None:
            cap = cv2.VideoCapture(kwargs["src"])

    def up(self):
        img = cv2.imread('up.png')
        img_height, img_width, _ = img.shape
        ret, frame = self.cap.read()
        frame_height, frame_width, _ = frame.shape
        x = (frame_width / 2) - (img_width / 2)
        y = 50
        frame[y:y + img_height, x:x + img_width] = img
        return frame

    def down(self):
        img = cv2.imread('down.png')
        img_height, img_width, _ = img.shape
        ret, frame = self.cap.read()
        frame_height, frame_width, _ = frame.shape
        x = (frame_width / 2) - (img_width / 2)
        y = frame_height - img_height - 10
        frame[y:y + img_height, x:x + img_width] = img
        return frame

