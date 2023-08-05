import cv2

from robot_neck_fake.executor import FakeNeckExecutor

if __name__ == '__main__':
    c = FakeNeckExecutor()
    while True:
        frame = c.down()
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Exit if ESC key is pressed
        if cv2.waitKey(20) & 0xFF == 27:
            break


