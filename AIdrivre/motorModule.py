import RPi.GPIO as GPIO
from time import sleep


class motor():
    def __init__(self) -> None:
        # motor 1
        self.A1 = 24
        self.B1 = 23
        self.en1 = 25
        # motor 2
        self.A2 = 14
        self.B2 = 15
        self.en2 = 18

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.B1, GPIO.OUT)
        GPIO.setup(self.en1, GPIO.OUT)
        GPIO.output(self.A1, GPIO.LOW)
        GPIO.output(self.B1, GPIO.LOW)

        #GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A2, GPIO.OUT)
        GPIO.setup(self.B2, GPIO.OUT)
        GPIO.setup(self.en2, GPIO.OUT)
        GPIO.output(self.A2, GPIO.LOW)
        GPIO.output(self.B2, GPIO.LOW)

        self.m_1 = GPIO.PWM(self.en1, 50)
        self.m_2 = GPIO.PWM(self.en2, 50)

        self.m_1.start(10)
        self.m_2.start(10)

    def motor1(self, A_status, B_status):
        GPIO.output(self.A1, A_status)
        GPIO.output(self.B1, B_status)

    def motor2(self, A_status, B_status):
        GPIO.output(self.A2, A_status)
        GPIO.output(self.B2, B_status)

    def forward(self, wait=0):
        self.motor1(GPIO.LOW, GPIO.HIGH)
        self.motor2(GPIO.LOW, GPIO.HIGH)
        sleep(wait)

    def backward(self, wait=0):
        self.motor1(GPIO.HIGH, GPIO.LOW)
        self.motor2(GPIO.HIGH, GPIO.LOW)
        sleep(wait)

    def stop(self, wait=0):
        self.motor1(GPIO.LOW, GPIO.LOW)
        self.motor2(GPIO.LOW, GPIO.LOW)
        sleep(wait)

    def speed(self, speed):
        self.m_1.ChangeDutyCycle(speed)
        self.m_2.ChangeDutyCycle(speed)


    def left(self, wait=0):
        self.motor1(GPIO.HIGH, GPIO.LOW)
        self.motor2(GPIO.LOW, GPIO.HIGH)
        sleep(wait)

    def right(self, wait=0):
        self.motor1(GPIO.LOW, GPIO.HIGH)
        self.motor2(GPIO.HIGH, GPIO.LOW)
        sleep(wait)

    def exit(self):
        GPIO.cleanup()
        print("GPIO Clean up")

    def __del__(self):
    # Add a destructor to stop and close the PWM objects
        self.m_1.stop()
        self.m_2.stop()   

if __name__ == '__main__':
    
    car=motor()
    car.speed(20)
    car.backward(5)

    car.left(2)
    car.right(2)
    car.stop()
    car.exit()
