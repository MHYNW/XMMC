import socket

import MXP_EasyClass
import xpc
import threading
import time
import sys
import keyboard
from socket import *
import pickle


sys.setrecursionlimit(3600000)  # Program can run in an hour
MXP = MXP_EasyClass.MXPEasyClass()
host = "192.168.10.18"
port = 9999
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((host, port))
print("Connected")


'''
sys.setrecursionlimit(360000)       # Program can run in an hour
MXP = MXP_EasyClass.MXPEasyClass()
host = ""
port = 4444
datasocket = socket.socket(socket.AF_INET, socket.STREAM)
datasocket.bind((host, port))
datasocket.listen(1)
conn, addr = datasocket.accept()
print("Connected by ", addr)
'''

class Simulation:
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

    values = [None] * 15
    Flag = True

    def __init__(self):
        '''
        sys.setrecursionlimit(360000)  # Program can run in an hour
        MXP = MXP_EasyClass.MXPEasyClass()
        host = "127.0.0.1"
        port = 4444
        clientsocket = socket(AF_INET, SOCK_STREAM)
        clientsocket.connect((host, port))
        print("Connected")
        '''

    def send(self, sock):
        while True:
            sendData = pickle.dumps(self.values)
            # clientsocket.send(sendData.encode("utf-8"))
            clientsocket.send(sendData)

    def recv(self, sock):
        while True:
            data = clientsocket.recv(1024)
            # pickle.loads(recvd_data)
            print("Data Received: ", data.decode("utf-8"))


    def Xplane(self):
        with xpc.XPlaneConnect() as client:
            while True:
                try:
                    # start = time.time()
                    '''
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
                    '''

                    self.values = client.getDREFs(self.drefs)

                    print("Roll: {}, Pitch: {}, Yaw: {}, P: {}, Q: {}, R: {}".format(self.values[3], self.values[4],
                                                                                     self.values[5],
                                                                                     self.values[6], self.values[7],
                                                                                     self.values[8]))
                    if self.Flag == True:
                        threading.Thread(
                            self.Motor_Run(self.values[3][0], self.values[6][0], self.values[9][0], self.values[9][0])).start()
                    self.Flag = not self.Flag
                    threading.Thread(target=self.send, args=(clientsocket,)).start()
                    threading.Thread(target=self.recv, args=(clientsocket,)).start()
                    threading.Timer(0.01, self.Xplane()).start()
                    # end = time.time()
                    # print("FPS: {}".format(1 / (end - start)))
                except KeyboardInterrupt:
                    print("Program Exited")

    def Motor_Start(self):
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

        self.Xplane()

    def Motor_Run(self, Posi, Vel, Acc, Dec):
        nAxisNo = [0, 1, 2]  # 0: Roll, 1: Pitch, 2: Yaw
        fPosition = Posi  # Position(Roll) * 235.6194
        fVel = 10000*Vel  # Velocity
        fAcc = 10000*Acc  # Acceleration
        fDec = 10000*Dec  # Deceleration
        fJerk = 1000  # jerk
        nResult = MXP.AX_MoveDirectPosition(nAxisNo[0], fPosition)
        # nResult = MXP.AX_MoveAbsolute(nAxisNo[0], fPosition, fVel, fAcc, fDec, fJerk,
        #                              MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_POSITIVE_DIRECTION,
        #                              MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
        print("Motor_Run Function Called")
        if nResult == 0:
            print("Motor Drived Successfully")


def main():
    print("START")
    simulation = Simulation()
    simulation.Motor_Start()
    #simulation.Xplane()






if __name__ == "__main__":
    main()
