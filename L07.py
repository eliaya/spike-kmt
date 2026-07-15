import color
import color_sensor
import distance_sensor
import force_sensor
import motor_pair
import runloop
from hub import port


async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

    state = 0
    was_pressed = False

    while True:
        is_pressed = force_sensor.pressed(port.A)
        dist = distance_sensor.distance(port.D)
        r, g, b, i = color_sensor.rgbi(port.C)

        if state == 0:
            if is_pressed and not was_pressed:
                motor_pair.move(motor_pair.PAIR_1, 0, velocity=280, acceleration=100)
                state = 1

        elif state == 1:
            if r > g and r > b and r > 20:
                print("赤っぽい")
                motor_pair.stop(motor_pair.PAIR_1)
                state = 0

        was_pressed = is_pressed
        await runloop.sleep_ms(10)


runloop.run(main())
