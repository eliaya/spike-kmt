from hub import port
import runloop
import motor_pair


async def main():
   # 指定したポートのモーターをペアにします。
   motor_pair.pair(motor_pair.PAIR_1, port.E, port.F)


   # 指定したステアリングと速度と加速度で進みます。
   #motor_pair.move(motor_pair.PAIR_1, 380, velocity=450, acceleration=300)
   motor_pair.move(motor_pair.PAIR_1, 450)
   await runloop.sleep_ms(3200)
   motor_pair.stop(motor_pair.PAIR_1)


runloop.run(main())
