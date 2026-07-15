import distance_sensor
import force_sensor
import motor
import motor_pair
import runloop
from hub import port

# Global Settings
APPROACH_VELOCITY = 280
APPROACH_ACCELERATION = 100
DETECT_DISTANCE = 100
PUSH_DEGREES = 200
PUSH_VELOCITY = 500


async def run_once():
    # 1) Wait until the force sensor is pressed.
    while not force_sensor.pressed(port.A):
        await runloop.sleep_ms(10)

    # 2) Start moving forward.
    motor_pair.move(
        motor_pair.PAIR_1,
        0,
        velocity=APPROACH_VELOCITY,
        acceleration=APPROACH_ACCELERATION,
    )

    # 3) Wait until the button is released.
    while force_sensor.pressed(port.A):
        await runloop.sleep_ms(10)

    # 4) Keep moving until the bottle is detected close ahead.
    while True:
        dist = distance_sensor.distance(port.B)
        if dist != -1 and dist <= DETECT_DISTANCE:
            break
        await runloop.sleep_ms(10)

    # 5) Push a short extra distance at higher speed to knock the bottle over, then brake.
    await motor_pair.move_for_degrees(
        motor_pair.PAIR_1, PUSH_DEGREES, 0, velocity=PUSH_VELOCITY, stop=motor.BRAKE
    )

    # 6) Stop the robot.
    motor_pair.stop(motor_pair.PAIR_1, stop=motor.BRAKE)


async def main():
    # Pair motors
    motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)

    # Repeat the whole flow: after the bottle is knocked down and the robot
    # stops, pressing the force sensor again runs the same sequence once more.
    while True:
        await run_once()

        # Make sure the button from the previous run is fully released before
        # waiting for the next press, so one press triggers exactly one run.
        while force_sensor.pressed(port.A):
            await runloop.sleep_ms(10)


runloop.run(main())
