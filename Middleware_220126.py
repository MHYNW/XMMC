import MXP_EasyClass
import xpc
import threading
import time
import sys
from socket import *
import struct
import serial
import keyboard
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox,
                             QRadioButton,
                             QCheckBox, QMenu, QGridLayout, QComboBox, QLabel, QLineEdit)
from PyQt5.QtGui import QIcon

__platform__ = sys.platform
sys.setrecursionlimit(3600000)  # Program can run in an hour
MXP = MXP_EasyClass.MXPEasyClass()
'''수정해야할 부분'''

# host = "192.168.22.6"
host = "192.168.8.9"
port = 9999
clientsocket = socket(AF_INET, SOCK_STREAM)

serial_port = 'COM5'
serial_baudrate = 115200

'''Event Flags'''
motor_stop_flag = False


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.threadrun = thread_app()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 2)
        grid.addWidget(self.PC_ConnectGroup(), 0, 0)
        grid.setSpacing(2)
        grid.addWidget(self.FCC_ConnectGroup(), 0, 1)
        #grid.addWidget(self.Motor_ConnectGroup(), 1, 0)
        grid.addWidget(self.Push_buttonGroup(), 1, 0)

        self.setLayout(grid)

        self.setWindowTitle("Middleware")
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(1000, 500)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def PC_ConnectGroup(self):
        groupbox = QGroupBox("PC Connect")
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        self.ip_textbox = QLineEdit()
        self.ip_textbox.setText('192.168.8.9')
        self.ipchange_button = QPushButton('Change')
        self.portnumber = QLineEdit()
        self.portnumber.setText('9999')
        self.portchange_button = QPushButton('Change')

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("IP"))
        vbox.addWidget(self.ip_textbox)
        vbox.addWidget(self.ipchange_button)
        vbox.addWidget(QLabel("Port"))
        vbox.addWidget(self.portnumber)
        vbox.addWidget(self.portchange_button)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        '''Click event'''
        self.ipchange_button.clicked.connect(self.ipchange)
        self.portchange_button.clicked.connect(self.portchange)

        return groupbox

    def FCC_ConnectGroup(self):
        groupbox = QGroupBox("FCC Connect")
        self.port = QComboBox()
        self.port.insertItems(0, self._get_available_port())
        self.baudrate = QComboBox()
        self.baudrate.addItem('110')
        self.baudrate.addItem('300')
        self.baudrate.addItem('600')
        self.baudrate.addItem('1200')
        self.baudrate.addItem('2400')
        self.baudrate.addItem('4800')
        self.baudrate.addItem('9600')
        self.baudrate.addItem('14400')
        self.baudrate.addItem('19200')
        self.baudrate.addItem('38400')
        self.baudrate.addItem('57600')
        self.baudrate.addItem('115200')
        self.baudrate.addItem('128000')
        self.baudrate.addItem('256000')
        self.baudrate.setCurrentText('115200')
        self.conncectbutton = QPushButton('Connect')

        '''                                                                                                                             
        baudrate.activated[str].connect(self.baudrate_change)     #baudrate event                                                       
        '''

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("COM Port"))
        vbox.addWidget(self.port)
        vbox.addWidget(QLabel("Baudrate"))
        vbox.addWidget(self.baudrate)
        vbox.addStretch(1)
        vbox.addWidget(self.conncectbutton)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        '''Click event'''
        self.conncectbutton.clicked.connect(self.fcc_connect)

        return groupbox

    def Motor_ConnectGroup(self):
        groupbox = QGroupBox("Motor")
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        initbutton = QPushButton("Servo INIT")
        resetbutton = QPushButton("Servo Reset")
        servo_off_button = QPushButton("Servo Off")

        vbox = QVBoxLayout()
        vbox.addWidget(resetbutton)
        vbox.addWidget(servo_off_button)
        vbox.addWidget(initbutton)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        '''Click event'''
        resetbutton.clicked.connect(self.motor_reset)
        servo_off_button.clicked.connect(self.motor_off)
        initbutton.clicked.connect(self.motor_init)

        return groupbox

    def Push_buttonGroup(self):
        groupbox = QGroupBox('Program Operations')

        startbutton = QPushButton("Program RUN")
        stopbutton = QPushButton("Program STOP(Keyboard 'ESC')")

        vbox = QVBoxLayout()
        vbox.addWidget(startbutton)
        vbox.addWidget(stopbutton)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        '''Click event'''
        startbutton.clicked.connect(self.startMW)
        stopbutton.clicked.connect(self.motor_stop)

        return groupbox

    def get_port_path(self):
        return {"linux": 'dev/ttyS', "win32": 'COM'}[__platform__]

    def _get_available_port(self):
        available_port = list()
        port_path = self.get_port_path()

        for number in range(256):
            port_name = port_path + str(number)
            '''                                                                                                                         
            if not self._open(port_name):                                                                                               
                continue                                                                                                                
            '''
            available_port.append(port_name)
        return available_port

    def port_change(self, text):
        port = text
        print(port)

    def baudrate_change(self, text):
        baudrate = text
        print(baudrate)

    def ipchange(self):
        ip = self.ip_textbox.text()
        global host
        print(ip)
        host = ip

    def portchange(self):
        portnum = self.portnumber.text()
        global port
        print(portnum)
        port = portnum

    def fcc_connect(self):
        global clientsocket
        global serial_port
        global serial_baudrate
        comport = self.port.currentText()
        print(comport)
        baudrate = self.baudrate.currentText()
        print(baudrate)
        serial_port = comport                   # Set FCC serial port
        serial_baudrate = int(baudrate)              # Set FCC serial baudrate
        clientsocket.connect((host, port))      # PC Connect

        print("Connected")

    def startMW(self):
        global motor_stop_flag
        '''
        threading.Thread(main()).start()
        print("main program start")
        '''
        motor_stop_flag = False
        self.threadrun.start()

    def motor_stop(self):
        global motor_stop_flag
        motor_stop_flag = True

    def motor_reset(self):
        MXP.AX_Reset(0)
        MXP.AX_Reset(1)
        MXP.AX_Reset(2)

    def motor_off(self):
        fDec = 40
        fJerk = 100
        print("##########################################################################################")
        MXP.AX_Stop(0, True, fDec, fJerk)
        MXP.AX_Stop(1, True, fDec, fJerk)
        MXP.AX_Stop(2, True, fDec, fJerk)
        MXP.SYS_Stop()
        MXP.SYS_Destroy()
        print("#####################################  PROGRAM QUIT  #####################################")
        print("##########################################################################################")

    def motor_init(self):
        MXP.SYS_Init()


class thread_app(QThread):
    def run(self):
        main()


currentTime = lambda: int(round(time.time()*1000))


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
    yaw_0 = 0
    ailrn_error_count = 0
    ailrn_error_pre_count = 0
    elev_error_count = 0
    elev_error_pre_count = 0
    ruddr_error_count = 0
    ruddr_error_pre_count = 0

    mode = 1
    throttle = [1000]
    ailrn = [1500]
    elev = [1500]
    ruddr = [1500]
    throttle_buffer = 0
    ailrn_buffer = 0
    elev_buffer = 0
    ruddr_buffer = 0
    rotary_throttle1 = [1000]
    rotary_throttle2 = [1000]
    rotary_throttle3 = [1000]
    rotary_throttle4 = [1000]


    def __init__(self):
        pass

    def key_read(self):
        pass

    def send(self, socket):
        buffer = bytes()
        sendtime = currentTime()
        for i in range(0, 15):
            buffer += struct.pack('f', self.values[i][0])
        buffer += struct.pack('q', sendtime)
        # print("senddata {}".format(buffer))
        clientsocket.send(buffer)


    def recv(self, socket):
        data = clientsocket.recv(1024)
        print("Data Received: ", data.decode("utf-8"))

    def openSerial(self):
        ser = serial.Serial()
        '''Variable'''
        ser.port = serial_port
        ser.baudrate = serial_baudrate
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

    def serial(self):
        ser = self.openSerial()
        readed = self.read(ser)
        if readed == b'\xf4':
            readed2 = self.read(ser)
            if readed2 == b'\xd4':
                serial_data_packet = self.read(ser, 40)
                data = serial_data_packet[2:37]
                checksum = serial_data_packet[37]
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

    def Xplane(self):
        with xpc.XPlaneConnect() as client:
            while True:
                start = time.time()
                self.values = client.getDREFs(self.drefs)           # Read from X Plane Data
                '''Key stop or Button stop'''
                if keyboard.is_pressed('esc') or motor_stop_flag == True:
                    self.Motor_Stop()
                    break

                '''Error count stop'''
                if self.elev_error_count > 20:
                    self.Motor_Stop()
                    break

                if self.ruddr_error_count > 20:
                    self.Motor_Stop()
                    break

                if self.ailrn_error_count > 20:
                    self.Motor_Stop()
                    break

                elevater = (self.elev[0] - 1500) / 500
                aileron = (self.ailrn[0] - 1500) / 500
                rudder = (self.ruddr[0] - 1500) / 500
                throttle = (self.throttle[0] - 1000) / 1000

                ''' Error Check'''
                if abs(self.ailrn_buffer - aileron) > 0.5:
                    aileron = self.ailrn_buffer
                    self.ailrn_error_count = self.ailrn_error_count + 1
                    print("############################################################")
                    print("#########################AIRLN##############################")
                    print("############################################################")
                else:
                    self.ailrn_buffer = aileron

                if abs(self.elev_buffer - elevater) > 0.5: #0.08
                    elevater = self.elev_buffer
                    self.elev_error_count = self.elev_error_count + 1
                    print("############################################################")
                    print("#####################ELEV###################################")
                    print("############################################################")
                else:
                    self.elev_buffer = elevater

                if abs(self.ruddr_buffer - rudder) > 0.5: #0.08
                    rudder = self.ruddr_buffer
                    self.ruddr_error_count = self.ruddr_error_count + 1
                    print("############################################################")
                    print("#########################RUDDR##############################")
                    print("############################################################")
                else:
                    self.ruddr_buffer = rudder

                ''' Error Count Reset'''
                if self.ailrn_error_count == self.ailrn_error_pre_count:
                    self.ailrn_error_count = 0
                    self.ailrn_error_pre_count = 0
                else:
                    self.ailrn_error_pre_count = self.ailrn_error_count

                if self.elev_error_count == self.elev_error_pre_count:
                    self.elev_error_count = 0
                    self.elev_error_pre_count = 0
                else:
                    self.elev_error_pre_count = self.elev_error_count

                if self.ruddr_error_count == self.ruddr_error_pre_count:
                    self.ruddr_error_count = 0
                    self.ruddr_error_pre_count = 0
                else:
                    self.ruddr_error_pre_count = self.ruddr_error_count
                controldata1 = [[8, elevater, aileron, rudder, 0, 0, 0, 0, 0]]             # X Plane data structure1
                controldata2 = [[25, throttle, 0, 0, 0, 0, 0, 0, 0]]                       # X Plane data structure2


                '''Motor Data'''
                '''
                print("Roll: {}, Pitch: {}, Yaw: {}, P: {}, Q: {}, R: {}".format(self.values[3], self.values[4],
                                                                                 self.values[5],
                                                                                 self.values[6], self.values[7],
                                                                                 self.values[8]))
                '''
                '''X Plane Data'''
                '''
                print("mode: {}, throttle: {}, ailrn: {}, elev: {}, ruddr: {}".format(self.mode, self.throttle,
                                                                                      self.ailrn, self.elev,
                                                                                      self.ruddr))
                '''
                self.Motor_Run(self.values[3][0], self.values[4][0], self.values[5][0])     # Motor Run
                threading.Thread(target=self.send, args=(clientsocket,)).start()            # PC Write
                threading.Thread(target=self.recv, args=(clientsocket,)).start()            # PC Read
                threading.Thread(self.serial()).start()                                     # FCC Serial
                client.sendDATA(controldata1)                                               # X Plane Write1
                client.sendDATA(controldata2)                                               # X Plane Write2
                '''
                if self.mode == 1:
                    print("mode1 flying")
                    client.sendDATA(controldata1)
                    client.sendDATA(controldata2)
                elif self.mode == 2:
                    print("mode2 flying")
                    client.sendDATA(controldata3)
                '''

                end = time.time()
                #print("FPS: {}".format(1 / (end - start)))
                print("Running...")

    def Motor_Start(self):

        nResult = MXP_EasyClass.MXP_FUNCTION_STATUS
        bReadyState = [0]
        time.sleep(1)
        #nResult = MXP.SYS_Init()
        '''Motor Init'''
        if MXP.SYS_Init() == 0:
            print("Motor Initialized")
        time.sleep(1)
        #nResult = MXP.SYS_GetStatus(nState)
        '''Motor Get Status'''
        if MXP.SYS_GetStatus([0]) == 0:
            print("Roll ..... Clear")
        if MXP.SYS_GetStatus([0]) == 0:
            print("Pitch ..... Clear")
        if MXP.SYS_GetStatus([0]) == 0:
            print("Yaw ..... Clear")
        time.sleep(1)

        '''System Run'''
        if MXP.SYS_Run() == 0:
            print("System Run Complete")
        #nResult = MXP.SYS_Run()
        #print("System Run Error: {}".format(nResult))
        time.sleep(5)

        ''' EtherCAT Check'''
        if MXP.ECAT_ReadyCheck([0]) == 0 and MXP.ECAT_ReadyCheck([1]) == 0 and MXP.ECAT_ReadyCheck([2]) == 0:
            print("EtherCat ..... Online")
        #nResult = MXP.ECAT_ReadyCheck(bReadyState)
        #print("EtherCAT Error state: {}".format(nResult))
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
        nResult2 = MXP.AX_SetPosition(nAxisNo[1], fSetPosition)
        nResult3 = MXP.AX_SetPosition(nAxisNo[2], fSetPosition)
        if nResult1 == 0 and nResult2 == 0 and nResult3 == 0:
            print("Set All Position Completely")
        #MXP.AX_Home(nAxisNo)
        #time.sleep(1)
        print("Axis Homing complete")
        time.sleep(1)

        '''Axis Ready Check'''
        bReadyCheck = [False]
        if MXP.AX_ReadyCheck(0, bReadyCheck) == 0 and MXP.AX_ReadyCheck(1, bReadyCheck) == 0 and MXP.AX_ReadyCheck(2, bReadyCheck) == 0:
            print("Axis Ready Checked")


    def Motor_Run(self, roll, pitch, yaw):
        global motor_stop_flag
        nAxisNo = [0, 1, 2]  # 0: Roll, 1: Pitch, 2: Yaw
        fPosition = [roll, pitch, yaw]  # Position(Roll) * 235.6194
        if roll > 25:
            roll = 25
            self.Motor_Stop()
        if roll < -25:
            roll = -25
            self.Motor_Stop()
        if pitch > 30:
            pitch = 30
            self.Motor_Stop()
        if pitch < -30:
            pitch = -30
            self.Motor_Stop()
        if yaw - self.yaw_0 > 180:
            if self.yaw_0 < -270:
                if yaw - self.yaw_0 > 540:
                    self.yaw_0 = yaw - 720
                    if self.yaw_0 <= -710:
                        self.yaw_0 = -710       # Negative restraint
                        print("#### negative direction limit ####")
                        motor_stop_flag = True  # Quit the program
                        #self.Motor_Stop()       # Quit the program
                else:
                    self.yaw_0 = yaw - 360
            else:
                self.yaw_0 = yaw - 360
        else:
            if self.yaw_0 > 270:
                if self.yaw_0 - yaw < 180:
                    self.yaw_0 = yaw
                else:
                    self.yaw_0 = yaw + 360
                    if self.yaw_0 >= 710:
                        self.yaw_0 = 710        # Positive restraint
                        print("#### positive direction limit ####")
                        motor_stop_flag = True  # Quit the program
                        #self.Motor_Stop()      # Quit the program
            else:
                self.yaw_0 = yaw



        fAcc = 80  # Acceleration
        fVel = 100  # Velocity
        fDec = 80  # Deceleration
        fJerk = 200  # Jerk
        Roll = -roll    # Reverse Direction
        Pitch = pitch
        Yaw = self.yaw_0

        nResult1 = MXP.AX_MoveAbsolute(nAxisNo[0], Roll, fVel, fAcc, fDec, fJerk,
                                       MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_NONE_DIRECTION,
                                       MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)

        nResult2 = MXP.AX_MoveAbsolute(nAxisNo[1], Pitch, fVel, fAcc, fDec, fJerk,
                                       MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_NONE_DIRECTION,
                                       MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
        nResult3 = MXP.AX_MoveAbsolute(nAxisNo[2], Yaw, fVel, fAcc, fDec, fJerk,
                                       MXP_EasyClass.MXP_DIRECTION_ENUM.MXP_SHORTEST_WAY,
                                       MXP_EasyClass.MXP_BUFFERMODE_ENUM.MXP_ABORTING)
        '''
        if nResult1 and nResult2 and nResult3 == 0:
            print("Motor Drived Successfully")
        '''

    def Motor_Stop(self):
        fDec = 40
        fJerk = 100
        print("##########################################################################################")
        MXP.AX_Stop(0, True, fDec, fJerk)
        MXP.AX_Stop(1, True, fDec, fJerk)
        MXP.AX_Stop(2, True, fDec, fJerk)
        MXP.SYS_Stop()
        MXP.SYS_Destroy()
        print("#####################################  PROGRAM QUIT  #####################################")
        print("##########################################################################################")




def main():
    print("START")
    #clientsocket = socket(AF_INET, SOCK_STREAM)
    #clientsocket.connect((host, port))
    #print("Connected")
    #currentTime = lambda: int(round(time.time() * 1000))
    simulation = Simulation()
    #threading.Thread(simulation.serial()).start()
    simulation.Motor_Start()
    threading.Thread(simulation.Xplane()).start()
    #threading.Thread(simulation.serial()).start()
    #simulation.Xplane().start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    #main()
