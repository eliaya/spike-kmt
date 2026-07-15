import force_sensor
import motor_pair
import runloop
from hub import port


async def main():
    # matching motor port E and port F
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

    # 起動時は何も起こらない
    is_moving = False

    while True:
        # check button status
        if force_sensor.pressed(port.A):
            # Logic change
            if not is_moving:
                motor_pair.move(motor_pair.PAIR_1, 0, velocity=280, acceleration=100)
                is_moving = True

            else:
                # Moving to stop
                motor_pair.stop(motor_pair.PAIR_1)
                is_moving = False

            # フォースセンサーを押すとSPIKEが前進する(モータが動く)
            while force_sensor.pressed(port.A):
                await runloop.sleep_ms(10)

        # Looping sleep
        await runloop.sleep_ms(10)


# Run App
runloop.run(main())
