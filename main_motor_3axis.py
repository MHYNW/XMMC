# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import MXP_EasyClass
import xpc
import threading
import time

MXP = MXP_EasyClass.MXPEasyClass()

def Motor_Start():

    nResult = MXP_EasyClass.MXP_FUNCTION_STATUS
    nState = [0]
    bReadyState = [0]
    time.sleep(1)
    nResult = MXP.SYS_Init()
    print("INIT Status: {}".format(nResult))
    time.sleep(1)
    nResult = MXP.SYS_GetStatus(nState)
    print("GetStatus status: {}".format(nResult))
    time.sleep(1)

    nResult = MXP.SYS_Run()
    print("System Run Error: {}".format(nResult))
    time.sleep(5)

    ''' EtherCAT Check'''
    nResult = MXP.ECAT_ReadyCheck(bReadyState)
    print("EtherCAT Error state: {}".format(nResult))
    time.sleep(1)

    '''Return Axis State(Clear)'''
    nAxisNo = 0  # Roll: 0, Pith: 1, Yaw: 2
    stAxisState = MXP_EasyClass.MXP_AxisStateBit()
    nResult = MXP.AX_ReadStatus(nAxisNo, stAxisState)
    print("Axis state: {}".format(nResult))
    time.sleep(1)
    '''EtherCAT Slave State(Clear)'''
    nSlaveState = [0]
    nSlaveNo = 0
    nResult = MXP.ECAT_GetSlaveCurrentState(nSlaveNo, nSlaveState)
    print("EtherCAT Slave State: {}".format(nResult))
    time.sleep(1)
    '''Servo On(Clear)'''
    if MXP.AX_Power(nAxisNo, True) == 0:
        print("Servo On")
    time.sleep(1)
    '''Automatically 0.5seconds delay'''
    '''Axis Homing'''
    MXP.AX_Home(nAxisNo)
    time.sleep(1)
    print("Axis Homing complete")
    time.sleep(5)
    '''Axis Ready Check'''
    bReadyCheck = [False]
    if MXP.AX_ReadyCheck(nAxisNo, bReadyCheck) == 0:
        print("Axis Ready Checked")

    with xpc.XPlaneConnect() as client:
        while True:
            start = time.time()
            drefs = ["sim/flightmodel/position/latitude",  # Latitude in degrees
                     "sim/flightmodel/position/longitude",  # Longitude in degrees
                     "sim/flightmodel/position/elevation",  # Altitude in meter(Mean Sea Level)
                     "sim/flightmodel/position/phi",  # Roll in degrees
                     "sim/flightmodel/position/theta",  # Pitch in degrees
                     "sim/flightmodel/position/psi",  # Heading in degrees
                     "sim/flightmodel/position/P",  # Roll rates in deg/s
                     "sim/flightmodel/position/Q",  # Pitch rates in deg/s
                     "sim/flightmodel/position/R",  # Yaw rates in deg/s
                     "sim/flightmodel/position/P_dot",  # Roll acceleration in deg/s^2
                     "sim/flightmodel/position/Q_dot",  # Pitch acceleration in deg/s^2
                     "sim/flightmodel/position/R_dot",  # Yaw acceleration in deg/s^2
                     "sim/flightmodel/position/local_vx",  # Velocity of X axis in m/s
                     "sim/flightmodel/position/local_vy",  # Velocity of Y axis in m/s
                     "sim/flightmodel/position/local_vz"]  # velocity of Z axis in m/s

            values = client.getDREFs(drefs)

            print("Roll: {}, Pitch: {}, Yaw: {}, P: {}, Q: {}, R: {}".format(values[3][0], values[4][0], values[5][0],
                                                                             values[6][0], values[7][0], values[8][0]))

            '''Move Absolute'''
            #motor_run(nAxisNo, values[3][0], values[6][0], values[9][0], values[9][0])
            motor_run(values[3][0], values[4][0], values[5][0])
            '''
            fPosition = values[3][0]   # Position(Roll)
            fVel = values[6][0]    # Velocity
            fAcc = values[9][0]    # Acceleration
            fDec = values[9][0]    # Deceleration
            fJerk = 1000    # jerk
            nResult = MXP.AX_MoveAbsolute(nAxisNo, fPosition, fVel, fAcc, fDec, fJerk,
                                  MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_NONE_DIRECTION,
                                  MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
            time.sleep(1)
            if nResult == 0:
                print("Motor Drived Successfully")
            '''

            end = time.time()
            print("FPS: {}".format(1 / (end - start)))

'''
    if (MXP.SYS_Destroy() == 0):
        print("Destory Succed")

    nResult = MXP.SYS_GetStatus(nState)
    print(nResult)
'''
def motor_run(Roll, Pitch, Yaw):
    roll_axisno = 0     # 0: Roll, 1: Pitch, 2: Yaw
    pitch_axisno = 1
    yaw_axisno = 2
    roll_position = Roll    # Position(Roll)
    pitch_position = Pitch
    yaw_position = Yaw
    '''save lock'''
    if pitch_position > 30:
        pitch_position = 30
    if yaw_position > 45:
        yaw_position = 45
    ''''''
    nResult = MXP.AX_MoveDirectPosition(roll_axisno, roll_position)
    MXP.AX_MoveDirectPosition(yaw_axisno, pitch_position)
    MXP.AX_MoveDirectPosition(pitch_axisno, yaw_position)
    #nResult = MXP.AX_MoveAbsolute(nAxisNo, fPosition, fVel, fAcc, fDec, fJerk,
    #                              MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_POSITIVE_DIRECTION,
    #                              MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
    #time.sleep(1)
    if nResult == 0:
        print("Motor Drived Successfully")
'''
def motor_run(AxisNo, posi, vel, acc, dec):
    nAxisNo = AxisNo    # 0: Roll, 1: Pitch, 2: Yaw
    fPosition = posi    # Position(Roll)
    fVel = 10*vel          # Velocity
    fAcc = 10*acc          # Acceleration
    fDec = 10*dec          # Deceleration
    fJerk = 1000        # jerk
    nResult = MXP.AX_MoveDirectPosition(nAxisNo, fPosition)
    #nResult = MXP.AX_MoveAbsolute(nAxisNo, fPosition, fVel, fAcc, fDec, fJerk,
    #                              MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_POSITIVE_DIRECTION,
    #                              MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
    #time.sleep(1)
    if nResult == 0:
        print("Motor Drived Successfully")
'''

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Motor_Start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/