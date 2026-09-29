from machine import Pin
from utime import sleep
from utime import sleep_ms, sleep_us


def number(num):
    delay = 27500
    if num <= 5:
        for i in range(0,num):
            second_pin.off()
            # sleep_ms(27)
            sleep_us(delay)
            fisrt_pin.off()
            second_pin.on()
            sleep_us(delay)
            fisrt_pin.on()
            second_pin.on()
            sleep_us(delay)
            # print(i)
    else:
        for i in range(0,10-num):
            fisrt_pin.off()
            # sleep_ms(27)
            sleep_us(delay)
            second_pin.off()
            fisrt_pin.on()
            sleep_us(delay)
            fisrt_pin.on()
            second_pin.on()
            sleep_us(delay)
            # print(i)

    btn.off()
    sleep_us(delay)
    btn.on()
    sleep_us(delay*50)

    






btn = Pin(1, Pin.OUT)
fisrt_pin = Pin(2, Pin.OUT)
second_pin = Pin(3, Pin.OUT)

btn.on()
fisrt_pin.on()
second_pin.on()
sleep(1)


for a in range(0,10):
    for b in range(0,10):
        for c in range(0,10):
            for d in range(0,10):
                    number(a)
                    number(b)
                    number(c)
                    number(d)
                    print(f"{a}{b}{c}{d}")
                    sleep(3)


# fisrt_pin.off()
# # sleep_ms(27)
# sleep_us(delay)
# second_pin.off()
# # fisrt_pin.on()
# sleep_us(delay)
# fisrt_pin.on()
# second_pin.on()
# sleep_us(delay)

# for _ in range(1,11):
#     btn.off()
#     sleep(0.0325)
#     btn.on()
#     sleep(1)
# sleep(0.05)
# btn.off()
# sleep(0.05)
# btn.on()

print("Finished.")
