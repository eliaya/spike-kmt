import distance_sensor
import force_sensor
import motor_pair
import runloop
from hub import port


async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

    while True:
        dist = distance_sensor.distance(port.D)

        if dist != -1 and 0 <= dist <= 15:
            motor_pair.move(motor_pair.PAIR_1, 0, velocity=280, acceleration=100)
        else:
            motor_pair.stop(motor_pair.PAIR_1)

        await runloop.sleep_ms(10)


runloop.run(main())
