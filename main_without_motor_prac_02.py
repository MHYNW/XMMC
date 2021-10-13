import MXP_EasyClass
import xpc
import threading
import time
import sys
from socket import *
import struct
import serial
import keyboard
from multiprocessing import Process, Queue

sys.setrecursionlimit(3600000)  # Program can run in an hour
MXP = MXP_EasyClass.MXPEasyClass()
'''수정해야할 부분'''
# host = "192.168.22.6"
host = "192.168.8.9"
port = 9999
''''''
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((host, port))
print("Connected")


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
    drefs_send = []

    values = [None] * 15
    Flag = True
    '''TBD'''
    mode = 1
    throttle = [1000]
    ailrn = [1500]
    elev = [1500]
    ruddr = [1500]
    rotary_throttle1 = [1000]
    rotary_throttle2 = [1000]
    rotary_throttle3 = [1000]
    rotary_throttle4 = [1000]


    def __init__(self):
        pass

    def send(self, socket):
        buffer = bytes()
        for i in range(0, 15):
            buffer += struct.pack('f', self.values[i][0])
        print("senddata {}".format(buffer))
        # clientsocket.send(sendData.encode("utf-8"))
        clientsocket.send(buffer)

        ## 재성
        '''
        buffer = bytes()

        # for i in range(0,15):
        #     buffer += struct.pack('d', self.values[i][0])
        # buffer = bytearray(struct.pack("f", datalist))
        # print(buffer)

        for i in range(0, 15):
            buffer += struct.pack("f", self.values[i][0])

        clientsocket.send(buffer)
        '''


    def recv(self, socket):
        data = clientsocket.recv(1024)
        # pickle.loads(recvd_data)
        print("Data Received: ", data.decode("utf-8"))

    def openSerial(self):
        ser = serial.Serial()
        '''수정해야할 부분'''
        ser.port = 'COM5'
        ser.baudrate = 115200
        ''''''
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = None
        ser.xonxoff = False
        ser.rtscts = False
        ser.dsrdtr = False

        ser.open()
        return ser

    def writePort(self, ser, data):
        ser.write(data)

    def read(self, ser, size=1, timeout=None):
        ser.timeout = timeout
        readed = ser.read(size)
        return readed

    def readEOF(self, ser):
        readed = ser.readline()
        return readed[:-1]

    def readUntilExitCode(self, ser, exitcode=b'\x03'):
        readed = b''
        while True:
            data = ser.read()
            print(data)
            readed += data
            if exitcode in data:
                return readed[:1]

    def serial(self):
        ser = self.openSerial()
        '''
        string = 'hello world\r\n'
        self.writePort(ser, string)
        self.writePort(ser, string.encode())
        self.writePort(ser, string.encode())

        string = b'Hello World\r\n'
        self.writePort(ser, string)

        string = '한글 전송 테스트\r\n'
        self.writePort(ser. string.encode())
        '''
        readed = self.read(ser)
        #print(readed)

        if readed == b'\xf4':
            readed2 = self.read(ser)
            if readed2 == b'\xd4':
                serial_data_packet = self.read(ser, 40)
                #print(serial_data_packet)
                data = serial_data_packet[2:37]
                checksum = serial_data_packet[37]
                '''
                self.mode = data[2]
                self.throttle = struct.unpack('f', data[3:7])
                self.ailrn = struct.unpack('f', data[7:11])
                self.elev = struct.unpack('f', data[11:15])
                self.ruddr = struct.unpack('f', data[15:19])
                self.rotary_throttle1 = struct.unpack('f', data[19:23])
                self.rotary_throttle2 = struct.unpack('f', data[23:27])
                self.rotary_throttle3 = struct.unpack('f', data[27:31])
                self.rotary_throttle4 = struct.unpack('f', data[31:35])
                '''
                if (sum(data) % 256) == checksum:
                    self.mode = data[2]
                    self.throttle = struct.unpack('f', data[3:7])
                    self.ailrn = struct.unpack('f', data[7:11])
                    self.elev = struct.unpack('f', data[11:15])
                    self.ruddr = struct.unpack('f', data[15:19])
                    self.rotary_throttle1 = struct.unpack('f', data[19:23])
                    self.rotary_throttle2 = struct.unpack('f', data[23:27])
                    self.rotary_throttle3 = struct.unpack('f', data[27:31])
                    self.rotary_throttle4 = struct.unpack('f', data[31:35])

        else:
            pass



        #print(self.read(ser, 42))
        #print(self.read(ser, size=42, timeout=5))
        #print(self.readEOF(ser))
        #print(self.readUntilExitCode(ser))
        '''
        readed = self.read(ser)
        print(readed)
        print(self.read(ser, 10))
        print(self.read(ser, size=3, timeout=5))
        print(self.readEOF(ser))
        print(self.readUntilExitCode(ser))
        '''


    def Xplane(self):
        with xpc.XPlaneConnect() as client:
            while True:
                try:
                    start = time.time()
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
                             "sim/flightmodel/position/l-=ocal_vz"]  # velocity of Z axis in m/s
                    '''

                    self.values = client.getDREFs(self.drefs)


                    print("Roll: {}, Pitch: {}, Yaw: {}, P: {}, Q: {}, R: {}".format(self.values[3], self.values[4],
                                                                                     self.values[5],
                                                                                     self.values[6], self.values[7],
                                                                                     self.values[8]))
                    '''
                    if self.Flag == True:
                        threading.Thread(
                            self.Motor_Run(self.values[3][0], self.values[6][0], self.values[9][0], self.values[9][0])).start()
                    self.Flag = not self.Flag
                    '''
                    '''version 1(no thread)'''
                    #self.Motor_Run(self.values[3][0], self.values[4][0], self.values[5][0])

                    ##########################################################################################
                    '''version 2(using tread)'''
                    '''
                    threading.Thread(
                        self.Motor_Run(self.values[3][0], self.values[4][0], self.values[5][0])).start()
                    '''
                    ##########################################################################################
                    '''
                    if keyboard.is_pressed('esc'):
                        self.Motor_Stop()
                        break
                    '''

                    threading.Thread(target=self.send, args=(clientsocket,)).start()
                    threading.Thread(target=self.recv, args=(clientsocket,)).start()
                    #threading.Timer(0.01, self.Xplane()).start()
                    Process(self.serial()).start()

                    '''write to xplane'''
                    print("mode: {}, throttle: {}, ailrn: {}, elev: {}, ruddr: {}".format(self.mode, self.throttle, self.ailrn, self.elev, self.ruddr))

                    elevater = (self.elev[0] - 1500)/500
                    aileron = (self.ailrn[0] - 1500)/500
                    rudder = (self.ruddr[0] - 1500)/500
                    throttle = (self.throttle[0] - 1000)/1000
                    rotary_throt1 = (self.rotary_throttle1[0] - 1000)/1000
                    rotary_throt2 = (self.rotary_throttle2[0] - 1000)/1000
                    rotary_throt3 = (self.rotary_throttle3[0] - 1000)/1000
                    rotary_throt4 = (self.rotary_throttle4[0] - 1000)/1000
                    print("mode2 throttle: {}, {}, {}, {}".format(rotary_throt1, rotary_throt2, rotary_throt3, rotary_throt4))

                    controldata1 = [[8, elevater, aileron, rudder, 0, 0, 0, 0, 0]]
                    controldata2 = [[25, throttle, 0, 0, 0, 0, 0, 0, 0]]
                    controldata3 = [[25, rotary_throt1, rotary_throt2, rotary_throt3, rotary_throt4, 0, 0, 0, 0]]  # it can be index no.35

                    if self.mode == 1:
                        print("mode1 flying")
                        client.sendDATA(controldata1)
                        client.sendDATA(controldata2)
                    elif self.mode == 2:
                        print("mode2 flying")
                        client.sendDATA(controldata3)


                    end = time.time()
                    print("FPS: {}".format(1 / (end - start)))
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
        nAxisNo = [0, 1, 2]  # Roll: 0, Pith: 1, Yaw: 2
        stAxisState = MXP_EasyClass.MXP_AxisStateBit()
        nResult1 = MXP.AX_ReadStatus(nAxisNo[0], stAxisState)
        nResult2 = MXP.AX_ReadStatus(nAxisNo[1], stAxisState)
        nResult3 = MXP.AX_ReadStatus(nAxisNo[2], stAxisState)
        print("-Axis state- Roll: {}, Pitch: {}, Yaw: {}".format(nResult1, nResult2, nResult3))
        time.sleep(1)
        '''EtherCAT Slave State(Clear)'''
        nSlaveState = [0]
        nSlaveNo = [0, 1, 2]    # Roll: 0, Pitch: 1, Yaw: 2
        nResult1 = MXP.ECAT_GetSlaveCurrentState(nSlaveNo[0], nSlaveState)
        nResult2 = MXP.ECAT_GetSlaveCurrentState(nSlaveNo[1], nSlaveState)
        nResult3 = MXP.ECAT_GetSlaveCurrentState(nSlaveNo[2], nSlaveState)
        print("-EtherCAT Slave State- Roll: {}, Pitch: {}, Yaw: {}".format(nResult1, nResult2, nResult3))
        time.sleep(1)
        '''Servo On(Clear)'''
        if MXP.AX_Power(nAxisNo[0], True) == 0:
            print("Servo Roll On")
        if MXP.AX_Power(nAxisNo[1], True) == 0:
            print("Servo Pitch On")
        if MXP.AX_Power(nAxisNo[2], True) == 0:
            print("Servo Yaw On")

        time.sleep(1)
        '''Automatically 0.5seconds delay'''
        '''Axis Homing'''

        fSetPosition = 0
        nResult1 = MXP.AX_SetPosition(nAxisNo[0], fSetPosition)
        nResult3 = MXP.AX_SetPosition(nAxisNo[2], fSetPosition)
        if nResult3 == 0:
            print("Yaw Set Position Complete")

        #MXP.AX_Home(nAxisNo)
        #time.sleep(1)
        print("Axis Homing complete")
        time.sleep(1)
        '''Axis Ready Check'''
        bReadyCheck = [False]
        if MXP.AX_ReadyCheck(nAxisNo, bReadyCheck) == 0:
            print("Axis Ready Checked")

        #self.Xplane()

    def Motor_Run(self, roll, pitch, yaw):
        nAxisNo = [0, 1, 2]  # 0: Roll, 1: Pitch, 2: Yaw
        fPosition = [roll, pitch, yaw]  # Position(Roll) * 235.6194
        fVel = 50  # Velocity
        fAcc = 30  # Acceleration
        fDec = 30  # Deceleration
        fJerk = 100  # Jerk
        Roll = -roll    # Reverse Direction
        Pitch = pitch
        Yaw = -yaw


        if Roll > 25:
            Roll = 25
        if Roll < -25:
            Roll = -25
        if Pitch > 30:
            Pitch = 30
        if Pitch < -30:
            Pitch = -30
        '''
        if yaw >= 90 and yaw < 180:
            yaw = yaw - 90
        if yaw >= 180 and yaw < 270:
            yaw = yaw - 360
        if yaw >= 270 and yaw <= 360:
            yaw = yaw - 360
        '''
        '''
        nResult1 = MXP.AX_MoveDirectPosition(nAxisNo[0], Roll)
        '''

        nResult1 = MXP.AX_MoveAbsolute(nAxisNo[0], Roll, fVel, fAcc, fDec, fJerk,
                                       MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_NONE_DIRECTION,
                                       MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)

        nResult2 = MXP.AX_MoveAbsolute(nAxisNo[1], Pitch, fVel, fAcc, fDec, fJerk,
                                       MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_NONE_DIRECTION,
                                       MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
        nResult3 = MXP.AX_MoveAbsolute(nAxisNo[2], Yaw, fVel, fAcc, fDec, fJerk,
                                       MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_SHORTEST_WAY,
                                       MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)

        # nResult = MXP.AX_MoveAbsolute(nAxisNo[0], fPosition, fVel, fAcc, fDec, fJerk,
        #                              MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_POSITIVE_DIRECTION,
        #                              MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
        print("Motor_Run Function Called")
        if nResult1 and nResult2 and nResult3 == 0:
            print("Motor Drived Successfully")

    def Motor_Stop(self):
        fDec = 40
        fJerk = 100
        print("##########################################################################################")
        '''
        MXP.AX_Stop(0, True, fDec, fJerk)
        MXP.AX_Stop(1, True, fDec, fJerk)
        MXP.AX_Stop(2, True, fDec, fJerk)
        MXP.SYS_Stop()
        MXP.SYS_Destroy()
        '''
        print("#####################################  PROGRAM QUIT  #####################################")
        print("##########################################################################################")


def main():
    print("START")
    simulation = Simulation()
    #threading.Thread(simulation.serial()).start()
    #simulation.Motor_Start()
    threading.Thread(simulation.Xplane()).start()
    #threading.Thread(simulation.serial()).start()
    #threading.Thread(target=simulation.send, args=(clientsocket, simulation.values)).start()
    #threading.Thread(target=simulation.recv, args=(clientsocket,)).start()
    #simulation.Xplane().start()






if __name__ == "__main__":
    main()
