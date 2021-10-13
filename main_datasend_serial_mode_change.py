#import MXP_EasyClass
import xpc
import threading
import time
import sys
from socket import *
import struct
import signal
import serial


sys.setrecursionlimit(3600000)  # Program can run in an hour
#MXP = MXP_EasyClass.MXPEasyClass()
host = "192.168.21.115"
port = 9999
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
    '''수정필요'''
    mode = 0x01
    throttle = 0
    ailrn = 0
    elev = 0
    ruddr = 0
    rotary_throttle1 = 0
    rotary_throttle2 = 0
    rotary_throttle3 = 0
    rotary_throttle4 = 0


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

        ser.port = 'COM3'
        ser.baudrate = 115200
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
        print(readed)

        if readed == b'\xf4':
            readed2 = self.read(ser)
            if readed2 == b'\xd4':
                serial_data_packet = self.read(ser, 40)
                #print(serial_data_packet)
                data = serial_data_packet[2:37]
                checksum = serial_data_packet[37]
                self.mode = data[2]
                self.throttle = struct.unpack('f', data[3:7])
                self.ailrn = struct.unpack('f', data[7:11])
                self.elev = struct.unpack('f', data[11:15])
                self.ruddr = struct.unpack('f', data[15:19])
                self.rotary_throttle1 = struct.unpack('f', data[19:23])
                self.rotary_throttle2 = struct.unpack('f', data[23:27])
                self.rotary_throttle3 = struct.unpack('f', data[27:31])
                self.rotary_throttle4 = struct.unpack('f', data[31:35])
                print("mode: {}".format(self.mode))
                '''

                if (sum(data.hex()) % 256) == checksum:
                    self.mode = data[2]
                    self.throttle = struct.unpack('f', data[3:6])
                    self.ailrn = struct.unpack('f', data[7:10])
                    self.elev = struct.unpack('f', data[11:14])
                    self.ruddr = struct.unpack('f', data[15:18])
                '''
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


                    #threading.Thread(target=self.send, args=(clientsocket,)).start()
                    #threading.Thread(target=self.recv, args=(clientsocket,)).start()
                    #threading.Timer(0.01, self.Xplane()).start()
                    threading.Thread(self.serial()).start()
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

                    controldata1 = [[8, elevater, aileron, rudder, 0, 0, 0, 0, 0]]
                    controldata2 = [[25, throttle, 0, 0, 0, 0, 0, 0, 0]]
                    controldata3 = [[25, rotary_throt1, rotary_throt2, rotary_throt3, rotary_throt4, 0, 0, 0, 0]]   # it can be index no.35

                    if self.mode == 1:
                        client.sendDATA(controldata1)
                        client.sendDATA(controldata2)
                    elif self.mode == 2:
                        client.sendDATA(controldata3)
                    #ctrldata1 = [[8, (self.elev[0] - 1500)/500, (self.ailrn[0] - 1500)/500, (self.ruddr[0] - 1500)/500, -998, -998, -998, -998, -998]]
                    #ctrldata2 = [[25, (self.throttle[0] - 1000)/1000, 0, 0, 0, 0, 0, 0, 0]]
                    #client.sendDATA(ctrldata1)
                    #client.sendDATA(ctrldata2)
                    #client.sendDATA([8, self.ailrn[0]/1500, self.elev[0]/1500, self.ruddr[0]/1500])
                    #client.sendDATA(daaaa)
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

        #self.Xplane()

    def Motor_Run(self, Posi, Vel, Acc, Dec):
        nAxisNo = [0, 1, 2]  # 0: Roll, 1: Pitch, 2: Yaw
        fPosition = Posi  # Position(Roll) * 235.6194
        fVel = Vel  # Velocity
        fAcc = Acc  # Acceleration
        fDec = Dec  # Deceleration
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

    #threading.Thread(simulation.serial()).start()
    #simulation.Motor_Start()
    threading.Thread(simulation.Xplane()).start()
    #threading.Thread(target=simulation.send, args=(clientsocket, simulation.values)).start()
    #threading.Thread(target=simulation.recv, args=(clientsocket,)).start()
    #simulation.Xplane().start()






if __name__ == "__main__":
    main()
