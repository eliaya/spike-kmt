import distance_sensor
import force_sensor
import motor
import motor_pair
import runloop
from hub import port

# Setting
REVERSE_VELOCITY = -280
REVERSE_ACCELERATION = 100
REVERSE_DISTANCE = 550


async def read_front_distance():
    # Waiting the DIstance
    while True:
        dist = distance_sensor.distance(port.B)
        if dist != -1:
            return dist
        await runloop.sleep_ms(10)


async def main():

    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

    while not force_sensor.pressed(port.A):
        await runloop.sleep_ms(10)

    start_dist = await read_front_distance()

    motor_pair.move(
        motor_pair.PAIR_1,
        0,
        velocity=REVERSE_VELOCITY,
        acceleration=REVERSE_ACCELERATION,
    )
    while force_sensor.pressed(port.A):
        await runloop.sleep_ms(10)

    while True:
        dist = distance_sensor.distance(port.B)
        if dist != -1 and (dist - start_dist) >= REVERSE_DISTANCE:
            break
        await runloop.sleep_ms(10)

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


runloop.run(main())
