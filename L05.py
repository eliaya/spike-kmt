import distance_sensor
import force_sensor
import motor_pair
import runloop
from hub import port


async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

    while True:
        while not force_sensor.pressed(port.A):
            await runloop.sleep_ms(10)

        motor_pair.move(motor_pair.PAIR_1, 0, velocity=280, acceleration=100)

        while force_sensor.pressed(port.A):
            await runloop.sleep_ms(10)

        while True:
            dist = distance_sensor.distance(port.D)
            if dist != -1 and dist <= 100:
                break
            await runloop.sleep_ms(10)

        motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())
