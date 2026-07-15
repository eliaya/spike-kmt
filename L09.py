import motor
import motor_pair
import runloop
from hub import motion_sensor, port

# Set motor pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

# Set values
forward_degrees = 1000
turn_speed = 200


async def go_forward():
    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1, forward_degrees, 0, stop=motor.BRAKE
    )


async def turn_left_90():
    # Reset
    motion_sensor.reset_yaw(0)

    # Wait motion_sensor
    while not motion_sensor.stable():
        await runloop.sleep_ms(10)

    # Turn left
    motor_pair.move_tank(motor_pair.PAIR_1, -turn_speed, turn_speed)

    # Stop at 90 degrees
    while abs(motion_sensor.tilt_angles()[0]) < 900:
        await runloop.sleep_ms(10)

    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


async def main():
    await go_forward()
    await turn_left_90()

    await go_forward()
    await turn_left_90()

    await go_forward()
    await turn_left_90()

    await go_forward()
    await turn_left_90()


runloop.run(main())
