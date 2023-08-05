import cv2

from robot_motor_fake.executor import FakeMotorExecutor

if __name__ == '__main__':
    c = FakeMotorExecutor()
    while True:
        frame = c.left()
        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Exit if ESC key is pressed
        if cv2.waitKey(20) & 0xFF == 27:
            break


