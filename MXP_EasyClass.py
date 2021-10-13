import sys
import time
import threading

import MXP_SoftMotion
import ctypes
from ctypes import *
from enum import IntEnum
import struct

#region SequenceMove

class MXP_SequenceBufferState(IntEnum):
    e_Null = 0
    e_Runing = 1
    e_Complete = 2
    e_Fail = 3
class ESequenceCmdType(IntEnum):
    e_AbsMove = 0
    e_RelativeMove = 1
    e_Dwell = 2
    e_IO = 3


class StSequenceMove():
    def __init__(self):
        self.nCmdType = 0
        self.fPos = 0
        self.fVel = 0
        self.fAcc = 0
        self.fDec = 0
        self.fJerk = 0
        self.fDwellTime = 0
        self.nIOSlaveNo = 0
        self.nIOBitNo = 0
        self.bIOBitSet = 0
        self.nDirection = 0
        self.nBufferMode = 0
        self.strStepName = ""

class EAxisSequenceData(IntEnum):
    e_MoveType = 0
    e_AxisGroupNo = 1
    e_nCmdType = 2
    e_fPos = 3
    e_fVel = 4
    e_fAcc = 5
    e_fDec = 6
    e_fJerk = 7
    e_fDwellTime = 8
    e_nIOSlaveNo = 9
    e_nIOBitNo =10
    e_bIOBitSet =11
    e_nDirection =12
    e_nBufferMode =13
    e_StepName =14
    e_End = 15


class StGroupSequenceMove():
    def __init__(self):
        self.nCmdType = 0
        self.fXPos = 0
        self.fYPos = 0
        self.fZPos = 0
        self.fUPos = 0
        self.fVPos = 0
        self.fWPos = 0
        self.fAPos = 0
        self.fBPos = 0
        self.fCPos = 0
        self.fVel = 0
        self.fAcc = 0
        self.fDec = 0
        self.fJerk = 0
        self.fDwellTime = 0
        self.nIOSlaveNo = 0
        self.nIOBitNo = 0
        self.bIOBitSet = 0
        self.nBufferMode = 0
        self.strStepName = ""
class EGroupSequenceData(IntEnum):
    e_MoveType = 0
    e_AxisGroupNo = 1
    e_nCmdType = 2
    e_fPos = 3
    e_fVel = 4
    e_fAcc = 5
    e_fDec = 6
    e_fJerk = 7
    e_fDwellTime = 8
    e_nIOSlaveNo = 9
    e_nIOBitNo =10
    e_bIOBitSet =11
    e_nBufferMode =12
    e_StepName =13
    e_End = 14

class AxisSequenceData():
    def __init__(self):
        self.bRunFlag = False
        self.nData = []

        self.nSaveNum = 0
        self.nReadNum = 0
        self.nCurBlock = 0
        self.nSendCount = 0
        self.nStartStep = 0
        self.nState = SEQUENCEMOVEPROCESS_CHECK()

    def DataClear(self):
        self.nData.clear()

    def DataAdd(self, nSequenceData):
        try:
            self.nData.append(nSequenceData)

        except Exception as ex:
            print('DataAdd Exception', str(ex))

class GroupSequenceData():
    def __init__(self):
        self.bRunFlag = False
        self.nData = []
        self.nSaveNum = 0
        self.nReadNum = 0
        self.nCurBlock = 0
        self.nSendCount = 0
        self.nStartStep = 0
        self.nState = SEQUENCEMOVEPROCESS_CHECK()

    def DataClear(self):
        self.nData.clear()
    def DataAdd(self,nGroupSequenceData):
        try:
            self.nData.append(nGroupSequenceData)

        except Exception as ex:
            print('DataAdd Exception', str(ex) )


class DataVaildCheck():
    def FCheckDataVaild(self, stReadData:StSequenceMove , arrCheckData ):

        if arrCheckData[EAxisSequenceData.e_AxisGroupNo] == 0:
            return False
        if arrCheckData[EAxisSequenceData.e_MoveType] == 0:
            return False
        if arrCheckData[EAxisSequenceData.e_nCmdType] == 0:
            return False
        if stReadData.nCmdType == ESequenceCmdType.e_AbsMove or stReadData.nCmdType == ESequenceCmdType.e_RelativeMove:
            if arrCheckData[EAxisSequenceData.e_fJerk] == 0 or stReadData.fJerk == 0:
                return False
            if arrCheckData[EAxisSequenceData.e_fAcc] == 0 or stReadData.fAcc == 0:
                return False
            if arrCheckData[EAxisSequenceData.e_fDec] == 0 or stReadData.fDec == 0:
                return False
            if arrCheckData[EAxisSequenceData.e_fPos] == 0 :
                return False
            if arrCheckData[EAxisSequenceData.e_fVel] == 0 or stReadData.fVel == 0:
                return False
            if arrCheckData[EAxisSequenceData.e_nBufferMode] == 0 or stReadData.nBufferMode == 0:
                return False

        elif stReadData.nCmdType == ESequenceCmdType.e_Dwell:
            if arrCheckData[EAxisSequenceData.e_fDwellTime] == 0 or stReadData.fDwellTime == 0:
                return False

        elif stReadData.nCmdType == ESequenceCmdType.e_IO:
            if arrCheckData[EAxisSequenceData.e_nIOBitNo] == 0:
                return False
            if arrCheckData[EAxisSequenceData.e_nIOSlaveNo] == 0:
                return False
            if arrCheckData[EAxisSequenceData.e_bIOBitSet] == 0:
                return False
        else:
            return False

        return True


    def FCheckGroupDataVaild(self, stReadData:StGroupSequenceMove , arrCheckData ):
        try:
            if arrCheckData[EGroupSequenceData.e_AxisGroupNo] == 0:
                return False
            if arrCheckData[EGroupSequenceData.e_MoveType] == 0:
                return False
            if arrCheckData[EGroupSequenceData.e_nCmdType] == 0:
                return False
            if stReadData.nCmdType == ESequenceCmdType.e_AbsMove or stReadData.nCmdType == ESequenceCmdType.e_RelativeMove:
                if arrCheckData[EGroupSequenceData.e_fJerk] == 0 or stReadData.fJerk == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_fAcc] == 0 or stReadData.fAcc == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_fDec] == 0 or stReadData.fDec == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_fPos] == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_fVel] == 0 or stReadData.fVel == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_nBufferMode] == 0 or stReadData.nBufferMode == 0:
                    return False

            elif stReadData.nCmdType == ESequenceCmdType.e_Dwell:
                if arrCheckData[EGroupSequenceData.e_fDwellTime] == 0 or stReadData.fDwellTime == 0:
                    return False

            elif stReadData.nCmdType == ESequenceCmdType.e_IO:
                if arrCheckData[EGroupSequenceData.e_nIOBitNo] == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_nIOSlaveNo] == 0:
                    return False
                if arrCheckData[EGroupSequenceData.e_bIOBitSet] == 0:
                    return False
            else:
                return False
            return True
        except Exception as ex:
            return False


class TXTLoader():
    DataCheck = DataVaildCheck()

    def AxisSequenceFileLoad(self,strFilePath,nAxisNo:c_uint32, arrData, strError):
        try:
            f = open(strFilePath, 'r')
            self.nLineCount = 0
            self.i = 0
            arrData.clear()
            self.nDataCheck =[]
            strError.append('')
            for nDataCount in range(EAxisSequenceData.e_End):
                self.nDataCheck.append(0)
            while True:
                self.nLineCount = self.nLineCount + 1
                self.nReadStr = f.readline()
                if not self.nReadStr:break
                self.nReadStr = self.nReadStr.replace('"' ,'')
                if self.nReadStr[0] !='#':
                    self.strSplit = self.nReadStr.split('\t')
                    if len(self.strSplit)  < 2:
                        strError[0] ='Line' + str(self.nLineCount) + ' data is invaild'
                        break

                    if self.strSplit[0] == 'MoveType':
                        if int(self.strSplit[1]) !=0:
                            strError[0] = 'MoveType data is invaild'
                            break
                        self.nDataCheck[EAxisSequenceData.e_MoveType] = True

                    elif self.strSplit[0] == 'Axis_GroupNo':
                        self.nReadAxisNo = int(self.strSplit[1])
                        if self.nReadAxisNo <0 or self.nReadAxisNo >127:
                            strError[0] = 'Axis_GroupNo data is invaild'
                            break
                        nAxisNo[0] = self.nReadAxisNo
                        self.nDataCheck[EAxisSequenceData.e_AxisGroupNo] = True
                    else:
                        self.AddData = StSequenceMove()
                        arrData.append(self.AddData)
                        self.strParam = self.strSplit[1].split(',')
                        if len(self.strParam) <2:
                            strError[0] = "Line " + str(self.nLineCount)+ ' data is invaild'
                            break
                        arrData[self.i].strStepName = self.strSplit[0]

                        for self.nDataCheckCount in range(EAxisSequenceData.e_End ):
                            if self.nDataCheckCount > EAxisSequenceData.e_AxisGroupNo:
                                self.nDataCheck[self.nDataCheckCount]  = False

                        for self.nParamCount  in range(len(self.strParam)):

                            self.strSplitParam = self.strParam[self.nParamCount].split(':')
                            if len(self.strSplitParam) < 2:
                                strError[0] = "Line " + str(self.nLineCount) + ' data is invaild'
                                break
                            if self.strSplitParam[0] == 'nCmdType':
                                arrData[self.i].nCmdType =  int(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_nCmdType] = True
                            if self.strSplitParam[0] == 'nDirection':
                                arrData[self.i].nDirection = int(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_nDirection] = True
                            if self.strSplitParam[0] == 'fPos':
                                arrData[self.i].fPos = float(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fVel':
                                arrData[self.i].fVel = float(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_fVel] = True
                            if self.strSplitParam[0] == 'fAcc':
                                arrData[self.i].fAcc = float(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_fAcc] = True
                            if self.strSplitParam[0] == 'fDec':
                                arrData[self.i].fDec = float(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_fDec] = True
                            if self.strSplitParam[0] == 'fJerk':
                                arrData[self.i].fJerk = float(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_fJerk] = True
                            if self.strSplitParam[0] == 'fDwellTime':
                                arrData[self.i].fDwellTime = float(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_fDwellTime] = True
                            if self.strSplitParam[0] == 'nIOSlaveNo':
                                arrData[self.i].nIOSlaveNo = int(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_nIOSlaveNo] = True
                            if self.strSplitParam[0] == 'nIOBitNo':
                                arrData[self.i].nIOBitNo = int(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_nIOBitNo] = True

                            if self.strSplitParam[0] == 'bIOBitSet':
                                arrData[self.i].bIOBitSet = int(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_bIOBitSet] = True

                            if self.strSplitParam[0] == 'nBufferMode':
                                arrData[self.i].nBufferMode = int(self.strSplitParam[1])
                                self.nDataCheck[EAxisSequenceData.e_nBufferMode] = True

                        if self.DataCheck.FCheckDataVaild(arrData[self.i] , self.nDataCheck ) == False:
                            strError[0] = "Step " + str(self.i + 1) + ' data is invaild'
                            break
                        self.i =self.i +1

            f.close()

            if strError[0] == '':
                return True
            else:
                return False
        except Exception as ex:
            f.close()
            strError[0] = str(ex) + '\t' + str(self.nLineCount)
            return False

    def GroupSequenceFileLoad(self,strFilePath,nAxesGroup:c_uint32, arrData, strError):
        try:
            f = open(strFilePath, 'r')
            self.nLineCount = 0
            self.i = 0
            arrData.clear()
            self.nDataCheck =[]
            strError.append('')

            for nDataCount in range(EGroupSequenceData.e_End):
                self.nDataCheck.append(0)
            while True:
                self.nLineCount = self.nLineCount + 1
                self.nReadStr = f.readline()
                if not self.nReadStr:break
                self.nReadStr = self.nReadStr.replace('"' ,'')
                if self.nReadStr[0] !='#':
                    self.strSplit = self.nReadStr.split('\t')
                    if len(self.strSplit)  < 2:
                        strError[0] ='Line' + str(self.nLineCount) + ' data is invaild'
                        break

                    if self.strSplit[0] == 'MoveType':
                        if int(self.strSplit[1]) !=1:
                            strError[0] = 'MoveType data is invaild'
                            break
                        self.nDataCheck[EGroupSequenceData.e_MoveType] = True

                    elif self.strSplit[0] == 'Axis_GroupNo':
                        self.nReadGroupNo = int(self.strSplit[1])
                        print('self.nReadGroupNo',self.nReadGroupNo)
                        if self.nReadGroupNo <0 or self.nReadGroupNo >31:
                            strError[0] = 'Axis_GroupNo data is invaild'
                            break
                        nAxesGroup[0] = self.nReadGroupNo
                        self.nDataCheck[EGroupSequenceData.e_AxisGroupNo] = True
                    else:
                        self.AddData = StGroupSequenceMove()
                        arrData.append(self.AddData)
                        self.strParam = self.strSplit[1].split(',')
                        if len(self.strParam) <2:
                            strError[0] = "Line " + str(self.nLineCount)+ ' data is invaild'
                            break
                        arrData[self.i].strStepName = self.strSplit[0]

                        for self.nDataCheckCount in range(EGroupSequenceData.e_End ):
                            if self.nDataCheckCount > EGroupSequenceData.e_AxisGroupNo:
                                self.nDataCheck[self.nDataCheckCount]  = False

                        for self.nParamCount  in range(len(self.strParam)):

                            self.strSplitParam = self.strParam[self.nParamCount].split(':')
                            if len(self.strSplitParam) < 2:
                                strError[0] = "Line " + str(self.nLineCount) + ' data is invaild'
                                break

                            if self.strSplitParam[0] == 'nCmdType':
                                arrData[self.i].nCmdType =  int(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_nCmdType] = True
                            if self.strSplitParam[0] == 'fXPos':
                                arrData[self.i].fXPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True

                            if self.strSplitParam[0] == 'fYPos':
                                arrData[self.i].fTPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fZPos':
                                arrData[self.i].fZPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fUPos':
                                arrData[self.i].fUPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fVPos':
                                arrData[self.i].fVPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fWPos':
                                arrData[self.i].fWPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fAPos':
                                arrData[self.i].fAPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fBPos':
                                arrData[self.i].fBPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True
                            if self.strSplitParam[0] == 'fCPos':
                                arrData[self.i].fCPos = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fPos] = True


                            if self.strSplitParam[0] == 'fVel':
                                arrData[self.i].fVel = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fVel] = True
                            if self.strSplitParam[0] == 'fAcc':
                                arrData[self.i].fAcc = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fAcc] = True
                            if self.strSplitParam[0] == 'fDec':
                                arrData[self.i].fDec = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fDec] = True
                            if self.strSplitParam[0] == 'fJerk':
                                arrData[self.i].fJerk = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fJerk] = True
                            if self.strSplitParam[0] == 'fDwellTime':
                                arrData[self.i].fDwellTime = float(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_fDwellTime] = True
                            if self.strSplitParam[0] == 'nIOSlaveNo':
                                arrData[self.i].nIOSlaveNo = int(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_nIOSlaveNo] = True
                            if self.strSplitParam[0] == 'nIOBitNo':
                                arrData[self.i].nIOBitNo = int(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_nIOBitNo] = True

                            if self.strSplitParam[0] == 'bIOBitSet':
                                arrData[self.i].bIOBitSet = int(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_bIOBitSet] = True

                            if self.strSplitParam[0] == 'nBufferMode':
                                arrData[self.i].nBufferMode = int(self.strSplitParam[1])
                                self.nDataCheck[EGroupSequenceData.e_nBufferMode] = True

                        if self.DataCheck.FCheckGroupDataVaild(arrData[self.i] , self.nDataCheck ) == False:
                            strError[0] = "Step " + str(self.i + 1) + ' data is invaild'
                            break
                        self.i =self.i +1

            f.close()

            if strError[0] == '':
                return True
            else:
                return False
        except Exception as ex:
            f.close()
            strError[0] = str(ex) + '\t' + str(self.nLineCount)
            return False
#endregion




#region define_Test
class MXP_CAMTABLE_REF(Structure):
    _fields_ = [
        ("MasterPos", c_float),
        ("SlavePos", c_float ),
        ("SlaveVel", c_float),
        ("SlaveAcc", c_float),
        ("SlaveJerk", c_float),
        ("PointType", c_uint32),
        ("InterpolationType", c_int32)]

class MXP_PROFILE_TABLE_IN(Structure):
    _fields_ = [
        ("TableindexNo", c_byte),
        ("nMotionMode", c_byte),
        ("Position", c_float),
        ("Velocity", c_float),
        ("Acc", c_float),
        ("Dec", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("Buffermode", c_int32)]

class MXP_File_TABLE_IN(Structure):
    _fields_ = [
        ("TableindexNo", c_byte),
        ("Position", c_float),
        ("Velocity", c_float),
        ("nTime", c_float),
        ("nDiffPosition", c_float),
        ("nDiffVelocity", c_float),
        ("nAcc", c_float)]

class MXP_IO_TABLE_IN(Structure):
    _fields_ = [
        ("TableindexNo", c_byte),
        ("SlaveNo", c_uint16),
        ("BitPos", c_uint16),
        ("BitValue", c_byte)]

class MXP_FILE_TABLE_ARRAY_IN(Structure):
    _fields_ = [
        ("DataSize", c_uint32),
        ("FileTable", MXP_File_TABLE_IN * 50)]


class MXP_PROFILE_TABLE_ARRAY_IN(Structure):
    _fields_ = [
        ("DataSize", c_uint32),
        ("ProfileTable", MXP_PROFILE_TABLE_IN * 50)]


class MXP_IO_TABLE_ARRAY_IN(Structure):
    _fields_ = [
        ("DataSize", c_uint32),
        ("IOTable", MXP_IO_TABLE_IN * 50)]

class MXP_MULTIAXISCOUPLE_SINGLEAXISGAIN(Structure):
    _fields_ = [
        ("FeedForward_V_Gain", c_uint16),
        ("FeedForward_A_Gain", c_uint16),
        ("P_Gain", c_uint16),
        ("I_Gain", c_uint16),
        ("D_Gain", c_uint16)]

class MXP_MULTIAXISCOUPLE_SINGLEAXISGAIN_ARRAY_IN(Structure):
    _fields_ = [
         ("SingleGain", MXP_MULTIAXISCOUPLE_SINGLEAXISGAIN * 10)]

class MXP_MULTIAXISCOUPLE_CCCGAIN(Structure):
    _fields_ = [
        ("CCC_Wp", c_uint16),
        ("CCC_Wi", c_uint16)]

class MXP_MULTIAXISCOUPLE_CCCGAIN_ARRAY_IN(Structure):
    _fields_ = [
         ("CCCGain", MXP_MULTIAXISCOUPLE_CCCGAIN * 10)]

...
#endregion
#region Enum Define


#region define_structure
class READ_CAMTABLE_REPLY():

    CamDataArray = []

    def __init__(self,nCount):
        self.Busy = 0
        self.Done = 0
        self.ErrorOn = 0
        self.ErrorID = 0
        self.TableRowCount = 0
        self.CamDataArray.clear
        Adddata = MXP_SoftMotion.MXP_CAMTABLE_REF()
        for i in range(nCount):
            self.CamDataArray.append(Adddata)

class READ_CAMSLAVEPOSITION_REPLY():
    def __init__(self):
        self.Busy = 0
        self.Done = 0
        self.ErrorOn = 0
        self.ErrorID = 0
        self.SlavePos = 0

class SEQUENCEMOVEPROCESS_CHECK():
    def __init__(self):
        self.Busy = 0
        self.Done = 0
        self.ErrorOn = 0
        self.ErrorID = 0

class PROCESS_CHECK():
    def __init__(self):
        self.Busy = 0
        self.Done = 0
        self.ErrorOn = 0
        self.ErrorID = 0

class READ_ETParameterReply():
    ReadData =[]
    def __init__(self,nCount):
        self.Busy = 0
        self.Done = 0
        self.ErrorOn = 0
        self.ErrorID = 0
        self.ReadData.clear()
        for i in range(nCount):
            self.ReadData.append(0)

class TouchProbeReadPos_Reply():
    def __init__(self):
        self.EdgePositivePosition = 0
        self.EdgeNegativePosition = 0

class AccDecToAccTime_Reply():
    def __init__(self):
        self.AccDecBuildUp = 0
        self.LimitAccDec = 0
        self.AccDecRampDown = 0

class AccTimeToAccDec_Reply():
    def __init__(self):
        self.Accdec = 0
        self.Jerk = 0

class PORT_STATE():
    def __init__(self):
        self.Port1State = 0
        self.Port2State = 0
        self.Port3State = 0
        self.Port4State = 0

class AXIS_ERROR():
    def __init__(self):
        self.MXPError = 0
        self.DriveError = 0

class GROUP_POS():
    def __init__(self):
        self.nX = 0
        self.nY = 0
        self.nZ = 0
        self.nU = 0
        self.nV = 0
        self.nY = 0
        self.nA = 0
        self.nB = 0
        self.nC = 0

class MXP_AxisStateBit():
    def __init__(self):
        self.ErrorStop = 0
        self.Disable = 0
        self.Stopping = 0
        self.Standstill = 0
        self.DiscreteMotion = 0
        self.ContinuousMotion = 0
        self.SynchronizedMotion = 0
        self.Homing = 0
        self.ConstantVelocity = 0
        self.Accelerating = 0
        self.Decelerating = 0
        self.DirectionPositive = 0
        self.DirectionNegative = 0
        self.HomeAbsSwitch = 0
        self.HWLimitSwitchPosEvent = 0
        self.HWLimitSwitchNegEvent = 0
        self.ReadyForPowerOn = 0
        self.PowerOn = 0
        self.IsHomed = 0
        self.AxisWarning = 0
class strTouchprobeState():
    def __init__(self):
        self.TouchprobeUsing = 0
        self.TouchprobeRisingEdgeSave = 0
        self.TouchprobeFallingEdgeSave = 0
        self.TouchprobeRisingPositionUpdate = 0
        self.TouchprobeFallingPositionUpdate = 0
...
#endregion
#region Enum Define
class MXP_CAM_MASTER_TYPE(IntEnum):
    MXP_CAM_MASTER_TYPE_MOTOR = 0
    MXP_CAM_MASTER_TYPE_EXTENAL_ENC = 1

class MXP_CAM_STATUS(IntEnum):
    RETCAM_NO_ERROR = 0
    RETCAM_ERROR_TABLEID =1
    RETCAM_ERROR_INPUTPARAM =2
    RETCAM_ERROR_DATASIZE =3
    RETCAM_ERROR_INTERPOLATION =4
    RETCAM_ERROR_MASTERPOS =5
    RETCAM_ERROR_EXECUTIONMODE =6

class MXP_DATA_TYPE(IntEnum):
    DATA_TYPE_Bit = 0x10
    DATA_TYPE_Word = 0x20
    DATA_TYPE_L = 0x30
    DATA_TYPE_F = 0x40
    DATA_TYPE_A = 0x50
    DATA_TYPE_Byte = 0x60
    DATA_TYPE_D = 0x70

class MXP_FUNCTION_STATUS(IntEnum):
    RET_NO_ERROR = 0 ,
    RET_ERROR_FUNCTION = -1    # Error (Functional buffer over flow)
    RET_ERROR_FULL = -2    # Buffer for command is full.
    RET_ERROR_WRONG_INDEX = -3     # Commanded Motion block index number is out of range.
    RET_ERROR_WRONG_AXISNO = -4    # Axis number does not exist.
    RET_ERROR_MOTIONBUSY = -5    # Commanded Motion block is already working.
    RET_ERROR_WRONG_SLAVENO = -6    # Slave number does not exist.
    RET_ERROR_WRONG_CAMTABLENO = -7    # CamTable number is out of range.
    RET_ERROR_WRONG_ECMASTERNO = -8    # ECamMaster number does not exist.
    RET_ERROR_WRONG_ECSLAVENO = -9    # ECamSlaver number does not exist.
    RET_ERROR_NOT_OPMODE = -10    # Slave is not op-mode.
    RET_ERROR_NOTRUNNING = -11    # Motion kernel is not running
    RET_ERROR_WRONG_PARAMETER_NO = -12     # Parameter number does not exist.
    RET_ERROR_WRONG_MXP_TYPE = -13    # License is not MXP-A type.
    RET_ERROR_ALREADYOPEN = -14    # Anaother API Opne to DLL
    RET_ERROR_NOT_SCANMODE = -15    # Anaother API Opne to DLL
    RET_ERROR_WRONG_ONLINESTATE = -16    # Anaother API Opne to DLL
    RET_ERROR_NOT_SIMULATIONMODE = -17  # Anaother API Opne to DLL
    RET_ERROR_NOT_FOEMODE = -18    # Anaother API Opne to DLL
    RET_ERROR_NOT_INVALID_LIC_FEATURE = -19     # Anaother API Opne to DLL

    RET_ERROR_INVAILD_LASTSTEPVEL = -20
    RET_ERROR_INVAILD_LASTTEPPOS = -21
    RET_ERROR_INVAILD_FIRSTSTEPVEL = -22

    # API Wrapping Class Define  = -200
    RET_ERROR_INVAILD_IOSize = -200
    RET_ERROR_FAIL_INDEX_CHECK = -201
    RET_ERROR_EXCEPTIONERROR = -202
    RET_ERROR_STATECHECK_FAIL = - 203
    RET_INVAILD_PLCADDRESS = -204
    RET_SEQUENCEMOVE_READ_FAIL = -205
    RET_SEQUENCEMOVE_INVAILDSTATE = -206
    RET_SEQUENCEMOVE_PROCESS_FAIL = -207




class KERNEL_STATUS(IntEnum):
    SYSTEM_UNLICENSED = -2   #System is NOT licensed.
    SYSTEM_IDLE = 1    #System is no working.
    SYSTEM_KILLING = 2    #System is killing.
    SYSTEM_KILLED = 3    #System is killed.
    SYSTEM_CREATING = 4    #System is creating.
    SYSTEM_CREATED = 5    #System is created.
    SYSTEM_INITING = 6    #System is initializing.
    SYSTEM_INITED = 7    #System is initialized.
    SYSTEM_READY = 8    #System is Initialized. System is ready to run.
    SYSTEM_RUN = 9    #System is running.
class MXP_ONLINE_STATE(IntEnum):
    ONLINE_STATE_NONE = 0x00
    ONLINE_STATE_INIT = 0x01
    ONLINE_STATE_PREOP = 0x02
    ONLINE_STATE_BOOT = 0x03
    ONLINE_STATE_SAFEOP = 0x04
    ONLINE_STATE_OP = 0x08
    ONLINE_STATE_ERROR_NONE = 0x10
    ONLINE_STATE_ERROR_INIT = 0x11
    ONLINE_STATE_ERROR_PREOP = 0x12
    ONLINE_STATE_ERROR_BOOT = 0x13
    ONLINE_STATE_ERROR_SAFEOP = 0x14
    ONLINE_STATE_ERROR_OP = 0x18
class MXP_NODE_TYPE(IntEnum):
    TYPE_NUll = 0
    TYPE_DRIVE =1
    TYPE_IO  =2
class MXP_PORT_STATE(IntEnum):
    DL_STATUS_LOOP_OPEN_NO_LINK = 0
    DL_STATUS_LOOP_CLOSE_NO_LINK = 1
    DL_STATUS_LOOP_OPEN_WITH_LINK = 2
    DL_STATUS_LOOP_CLOSE_WITH_LINK = 3
class MXP_IO_Type(IntEnum):
    IO_Out = 0
    IO_IN = 1

class MXP_ACTIVATIONMODE(IntEnum):
    IMMEDIATELY = 0
    ACTIVATIONPOSITION =1
    NEXTPERIOD = 2

class MXP_TRIGGER_MODE(IntEnum):
    e_Single = 0
    e_Continuous = 1
class MXP_TRIGGER_TYPE(IntEnum):
    e_Touchprobe = 0
    e_Index = 1
class MXP_TRIGGER_EDGE(IntEnum):
    e_Rising = 0
    e_Falling = 1
    e_Both = 2
class MXP_PDO_DIRECTION(IntEnum):
    e_ServoWrite = 0
    e_MXPWrite = 1
class MXP_MOVESTATE(IntEnum):
    MOVESTATE_Null = 0
    MOVESTATE_Moving =1
    MOVESTATE_Complete =2
    MOVESTATE_Fail =3
class MXP_BUFFERMODE_ENUM(IntEnum):
    MXP_ABORTING = 0
    MXP_BUFFERED = 1
    MXP_BLENDING_LOW = 2
    MXP_BLENDING_PREVIOUS = 3
    MXP_BLENDING_NEXT = 4
    MXP_BLENDING_HIGH = 5
    MXP_SINGLE_BLOCK = 6

class MXP_DIRECTION_ENUM(IntEnum):
    MXP_NONE_DIRECTION = 0
    MXP_POSITIVE_DIRECTION = 1
    MXP_SHORTEST_WAY = 2
    MXP_NEGATIVE_DIRECTION = 3
    MXP_CURRENT_DIRECTION = 4

class MXP_SOURCE_ENUM(IntEnum):
    MXP_COMMANDEDVALUE = 1
    MXP_SETVALUE = 2
    MXP_ACTUALVALUE = 3
class MXP_TOUCHPROBE_EDGE_ENUM(IntEnum):
    MXP_EDGE_POSITIVE = 0
    MXP_EDGE_NEGATIVE = 1
class MXP_PATHCHOICE_ENUM(IntEnum):
    MXP_CLOCKWISE = 0
    MXP_COUNTERCLOCKWISE = 1
class MXP_PLANE(IntEnum):
    XPLANE = 0
    YPLANE = 1
    ZPLANE = 2
    UPLANE =3
class MXP_STARTMODE_ENUM(IntEnum):
    MXP_ABSOLUTE = 0
    MXP_RELATIVE = 1
    MXP_RAMPIN = 2

class MXP_USERLib(IntEnum):
    MXP_R2R = 0
    MXP_Robotics = 1
    MXP_EDG = 2

...
#endregion
DefualtIOSize = 10
nProfileIn = MXP_SoftMotion.MXP_PROFILE_MOVE_IN()

mTouchprobeFunc=[]
for i in range(127):
    mTouchprobeFunc.append(0)


#region MotionIndexCal
class ECmdType(IntEnum):
    e_Null = 0
    e_GearIn = 1
    e_GearInPos = 2
    e_CAMIn = 3
    e_CAMTableOption = 4
    e_CAMTableEdit = 5
    e_CAMTable = 6
    e_ReadCAMSlavePos = 7

    e_ETParameterReadReq = 8
    e_ETParameterWriteReq =9

    e_ProfileMove = 10
    e_TouchprobeSet =11
    e_Direct_torque =12
    e_Direct_Velocity =13
    e_Direct_Position =14
    e_CCCSet =15
    e_CCCReset =16
    e_CCCGainSet =17


MC_SINGLEAXIS_INDEX = 0
MC_POWER_INDEX = 128
MC_RESETHOME_INDEX = 256
MC_GROUPAXIS_INDEX = 384
MC_IO_INDEX_START = 416
MC_IO_INDEX_END = 447
MC_PLCINTERFACE_INDEX = 448
MC_PDOWRITE = 450
MC_USERSTART_INDEX = 500
MC_USEREND_INDEX = 799
MC_PROFILEMOVE_INDEX = 800




class strIndexInfo():
    def __init__(self, bUsing:c_bool, nSlaveNo:c_uint32,nCmdType:ECmdType,nSubInfo:c_int32):
        self.bUsing = bUsing
        self.nSlaveNo = nSlaveNo
        self.nCmdType = nCmdType
        self.nSubInfo = nSubInfo



mMotionIndexInfo = []
for i in range(MC_USERSTART_INDEX  , MC_USEREND_INDEX ):
    mMotionIndexInfo.append(strIndexInfo( False , 0, 0, 0))

mIOIndexInfo = []
for i in range(MC_IO_INDEX_START  , MC_IO_INDEX_END ):
    mIOIndexInfo.append(strIndexInfo(False, 0, 0, 0))


def ClearAllIndex():
    for i in range(0, len(mMotionIndexInfo)-1):
        mMotionIndexInfo[i].bUsing = False
        mMotionIndexInfo[i].nSlaveNo = 0
        mMotionIndexInfo[i].nCmdType =ECmdType.e_Null
        mMotionIndexInfo[i].nSubInfo = 0

    for i in range(0, len(mIOIndexInfo)-1):
        mIOIndexInfo[i].bUsing = False
        mIOIndexInfo[i].nSlaveNo = 0
        mIOIndexInfo[i].nCmdType =ECmdType.e_Null
        mIOIndexInfo[i].nSubInfo = 0



    return 0
def ClearIndex(nIndexCount):
    nClearCount = nIndexCount - MC_USERSTART_INDEX
    mMotionIndexInfo[nClearCount].bUsing = False
    mMotionIndexInfo[nClearCount].nSlaveNo = 0
    mMotionIndexInfo[nClearCount].nCmdType = ECmdType.e_Null
    mMotionIndexInfo[nClearCount].nSubInfo = 0
    return True
def GetMotionIndex(nAxisNo:c_uint32, nCmdType:ECmdType ,nSubInfo:c_int =-999 ):
    nIndexCount =0
    if nSubInfo != -999:
        for nIndexCount in range(len(mMotionIndexInfo)-1):
            if mMotionIndexInfo[nIndexCount].nSlaveNo == nAxisNo and mMotionIndexInfo[nIndexCount].nCmdType == nCmdType and \
                    mMotionIndexInfo[nIndexCount].nSubInfo == nSubInfo and mMotionIndexInfo[nIndexCount].bUsing == True:
                return  nIndexCount + MC_USERSTART_INDEX

        for nIndexCount in range(len(mMotionIndexInfo)-1):
            if mMotionIndexInfo[nIndexCount].bUsing == False:
                mMotionIndexInfo[nIndexCount].bUsing = True
                mMotionIndexInfo[nIndexCount].nSlaveNo = nAxisNo
                mMotionIndexInfo[nIndexCount].nCmdType = nCmdType
                mMotionIndexInfo[nIndexCount].nSubInfo = nSubInfo
                return  nIndexCount + MC_USERSTART_INDEX
        return  0
    else:
        for nIndexCount in range(len(mMotionIndexInfo) - 1):
            if mMotionIndexInfo[nIndexCount].nSlaveNo == nAxisNo and mMotionIndexInfo[
                nIndexCount].nCmdType == nCmdType and mMotionIndexInfo[nIndexCount].bUsing == True:
                return nIndexCount + MC_USERSTART_INDEX

        for nIndexCount in range(len(mMotionIndexInfo) - 1):
            if mMotionIndexInfo[nIndexCount].bUsing == False:
                mMotionIndexInfo[nIndexCount].bUsing = True
                mMotionIndexInfo[nIndexCount].nSlaveNo = nAxisNo
                mMotionIndexInfo[nIndexCount].nCmdType = nCmdType
                mMotionIndexInfo[nIndexCount].nSubInof = 0
                return nIndexCount + MC_USERSTART_INDEX
        return 0



def GetMotionIndexCheck(nAxisNo:c_uint32, nCmdType:ECmdType ,nSubInfo:c_int = -999):
    nIndexCount = 0
    if nSubInfo != -999:
        for nIndexCount in range(len(mMotionIndexInfo)-1):
            if mMotionIndexInfo[nIndexCount].nSlaveNo == nAxisNo and mMotionIndexInfo[nIndexCount].nCmdType == nCmdType and \
                mMotionIndexInfo[nIndexCount].nSubInfo == nSubInfo and mMotionIndexInfo[nIndexCount].bUsing == True:
                return  nIndexCount + MC_USERSTART_INDEX
    else:
        for nIndexCount in range(len(mMotionIndexInfo)-1):
            if mMotionIndexInfo[nIndexCount].nSlaveNo == nAxisNo and mMotionIndexInfo[nIndexCount].nCmdType == nCmdType and \
                mMotionIndexInfo[nIndexCount].bUsing == True:
                return  nIndexCount + MC_USERSTART_INDEX
    return 0

def GetIoIndex(nSlave:c_uint32):
    nIndexCount =0
    for nIndexCount in range(len(mIOIndexInfo)-1):
        if mIOIndexInfo[nIndexCount].nSlaveNo == nSlave and mIOIndexInfo[nIndexCount].bUsing == True:
            return  nIndexCount + MC_IO_INDEX_START

    for nIndexCount in range(len(mIOIndexInfo)-1):
        if mIOIndexInfo[nIndexCount].bUsing == False:
            mIOIndexInfo[nIndexCount].bUsing = True
            mIOIndexInfo[nIndexCount].nSlaveNo = nSlave
            return  nIndexCount + MC_IO_INDEX_START
    return  0

...
#endregion

#region Data format

def to_float(long_):
    buf = struct.pack('>L', long_)
    return struct.unpack('>f',buf)[0]

def to_uint32(float_):
    buf = struct.pack('>f', float_)
    return struct.unpack('>L',buf)[0]


def uint32_to_float(long_):
    buf = struct.pack('>L', long_)
    return struct.unpack('>f',buf)[0]


def uint32_to_int32(uint32_):
    try:
        buf = struct.pack('>L', uint32_)
        return struct.unpack('>l',buf)[0]
    except Exception as ex:
        print('uint32_to_int32', ex)


def uint32_to_int16(uint32_):
    try:
        return uint32_.value
      #  buf = struct.pack('>L', uint32_)
      #  return struct.unpack('>h',buf)[0]

    except Exception as ex:
        print('uint32_to_int16', ex)



def int32_to_uint32(int32_):
    buf = struct.pack('>i', int32_)
    return struct.unpack('>I',buf)[0]

def int16_to_uint32(int16_):
    buf = struct.pack('>i', int16_)
    return struct.unpack('>I',buf)[0]



def uint64_to_int64(uint64_):
    try:
        buf = struct.pack('>Q', uint64_)
        return struct.unpack('>q',buf)[0]
    except Exception as ex:
        print('uint64_to_int64', ex)

def uint64_to_double(uint64_):
    buf = struct.pack('>Q', uint64_)
    return struct.unpack('>d',buf)[0]

def int64_to_uint64(int64_):
    buf = struct.pack('>q', int64_)
    return struct.unpack('>Q',buf)[0]

def double_to_uint64(double_):
    try:
        print('double_to_uint64' , double_)
        buf = struct.pack('>d', double_)
        print('double_to_uint64 out', struct.unpack('>Q',buf)[0])
        return struct.unpack('>Q',buf)[0]
    except Exception as ex:
        print('double_to_uint64', ex)



def int2bytes(n):
    result = bytearray()
    while (n):
        result.append(n & 0xff)
        n = n >> 8
    return list(result[::1])

def int2Bites(n):
    b = format(n, 'b')
    bitarray = list(b)
    bitarray = [int(i) for i in bitarray]
    bitarray.reverse()

    nSizeArray =[]
    for i in range (32):
        nSizeArray.append(0)
    nSizeArray[0:len(bitarray) - 1] = bitarray

    return  nSizeArray

...
#endregion



mGroupSequenceData = []
for GroupID in range(32):
    AddData = GroupSequenceData()
    mGroupSequenceData.append(AddData)


mAxisSequenceData = []
for AxisID in range(128):
    AddData = AxisSequenceData()
    mAxisSequenceData.append(AddData)

nTaskPos = []
nResult = []

nGroupTaskPos = []
nGroupResult = []

for i in range(128):
    nTaskPos.append(0)
    nResult.append(0)

for i in range(32):
    nGroupTaskPos.append(0)
    nGroupResult.append(0)

class MXPEasyClass(object):
    TxtReader = TXTLoader()
    def __init__(self):
        print('MXP start')



    # region System

    def SYS_Init(self):
        ''' Internal initialization to use the MXP

        :return: The result of Calling the function is returned
        '''
        try:
            nStatus = c_uint32()
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_InitKernel(pointer(nStatus))
            return nResult

        except Exception as ex:
            print('SYS_Init', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_Init_Developer(self):
        ''' Internal initialization to use the MXP

        :return: The result of Calling the function is returned
        '''
        try:
            nStatus = c_uint32()
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_InitKernel_Developer(pointer(nStatus))
            return nResult
        except Exception as ex:
            print('SYS_Init_Developer', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_Run(self):
        ''' This function runs the MXP.

        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_SystemRun()
            return nResult
        except Exception as ex:
            print('SYS_Run', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_Stop(self):
        ''' This function stops the MXP

        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_SystemStop()
            return nResult
        except Exception as ex:
            print('SYS_Stop', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_Destroy(self):
        ''' This function is called to terminate the connection with the MXP

        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_Destroy()
            return nResult
        except Exception as ex:
            print('SYS_Destroy', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_Destroy_Developer(self):
        ''' This function is called to terminate the connection with the MXP

        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_Destroy_Developer()
            return nResult
        except Exception as ex:
            print('SYS_Destroy_Developer', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def SYS_GetStatus(self, nStatus:KERNEL_STATUS):
        ''' This function returns the current status of the MXP State.
        Before Calling this function. initialize the MXP by calling SYS_Init.

        :param nStatus: Return the current status of the MXP
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_GetKernelStatus(byref(nReadData))
            nStatus[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('SYS_GetStatus', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_CheckLicense(self, nFunction:MXP_USERLib ,bStatus :c_bool):
        ''' This function check the MXP license

        :param nFunction: Set MXP_USERLib value
        :param bStatus: Return the licence Status(valid : TRUE, invalid : FALSE)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_byte()
            nResult = MXP_SoftMotion.MXP_CheckFeature(nFunction, byref(nReadData))
            bStatus[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('SYS_CheckLicense', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_GetMasterOnlineMode(self, nStatus:MXP_ONLINE_STATE ):
        ''' This function returns the network state of the current EtherCAT

        :param nStatus: Return the current EtherCAT master
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_GetOnlineMode(byref(nReadData))
            nStatus[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetMasterOnlineMode', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_GetMasterSimulationMode(self, bSimulation:c_bool):
        ''' This function returnes the MXP Run Mode

        :param bSimulation: Return MXP simulation Mode
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_SM_IsSimulationMode(byref(nReadData))
            bSimulation[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('SYS_GetMasterSimulationMode', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_GetSlaveNoFromNodeId(self, nNodeID:c_uint32, nSlaveNo:c_uint32):
        ''' This function obtains slave number using the NodeID

        :param nNodeID: NodeID of the EtherCAT module(0~255)
        :param nSlaveNo: Return slave number of the EtherCAT module(0~127)
        :return: The result of Calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint16()
            nResult = MXP_SoftMotion.MXP_GetSlaveNoFromNodeId(nNodeID, byref(nReadData))
            nSlaveNo[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveNoFromNodeId', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_GetAxisNoFromNodeId(self, nNodeID:c_uint32, nAxisNo:c_uint32):
        ''' This function obtains axis number using the NodeID

        :param nNodeID: NodeID of the EtherCAT module(0~255)
        :param nAxisNo: Return axis number of the EtherCAT module(0~127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_GetAxisNoFromNodeId(nNodeID, byref(nReadData))
            nAxisNo[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetAxisNoFromNodeId', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_GetSlaveCurrentState(self, nSlaveNo:c_uint32, nStatus:MXP_ONLINE_STATE):
        ''' Return the network state of an individual slave

        :param nSlaveNo: Slave number of the EtherCAT module(0~127)
        :param nStatus: Return the EtherCAT network state(0~0x18). refer MXP_ONLINE_STATE
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_IsSlaveOnline(nSlaveNo, byref(nReadData))
            nStatus[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveCurrentState', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_GetSlaveCount(self, nSlaveCount:c_uint32):
        ''' Return the number of slave devices currently connected

        :param nSlaveCount: Return the number of slave devices currently connected
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint16()
            nResult = MXP_SoftMotion.MXP_GetSlaveCount(0, byref(nReadData))
            nSlaveCount[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveCount', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_GetAxisCount(self, nAxisCount:c_uint32):
        ''' Return the number of Axis devices currently connected

        :param nAxisCount: Return the number of axes currently connected
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint16()
            nResult = MXP_SoftMotion.MXP_GetSlaveCount(1, byref(nReadData))
            nAxisCount[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveCount', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_GetSlaveType(self,nSlaveNo:c_uint32, nType:MXP_NODE_TYPE):
        ''' Return the type of a slave node

        :param nSlaveNo: Number of the slave module
        :param nType: Return the node type(1 : Servo Drive, 2 :IO)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_QueryNodeType(nSlaveNo, byref(nReadData))
            nType[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveType', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_GetMasterEtherCATLineStatus(self,bConnectState:c_bool):
        ''' This function returns the hardware network connect state of the EtherCAT master

        :param bConnectState: Return the PortState(True:Connect)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_SYSINFO_OUT()

            nResult = MXP_SoftMotion.MXP_GetSystemInformation(ctypes.byref(nIn))
            if nIn.EthercatLinkState.Master ==1:
                bConnectState[0] = True
            else:
                bConnectState[0] = False

            return nResult
        except Exception as ex:
            print('ECAT_GetMasterEtherCATLineStatus', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_GetSlaveEtherCATLineStatus(self,nSlaveNo:c_uint32, stPortState:PORT_STATE):
        ''' This function returns the hardware network connect state of the EtherCAT slave

        :param nSlaveNo: Set the slave number
        :param stPortState: Return the PortState(port1 ~ port4)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_SYSINFO_OUT()

            nResult = MXP_SoftMotion.MXP_GetSystemInformation(ctypes.byref(nIn))
            nbitArray = int2Bites(nIn.EthercatLinkState.Slaves[nSlaveNo])
            stPortState.Port1State = nbitArray[0] + nbitArray[1] *2
            stPortState.Port2State = nbitArray[2] + nbitArray[3] *2
            stPortState.Port3State = nbitArray[4] + nbitArray[5] *2
            stPortState.Port4State = nbitArray[6] + nbitArray[7] *2

            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveEtherCATLineStatus', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_GetEtherCATHistoryAlarm(self,arrAlarmArray):
        ''' This function returns the EtherCAT network alarm history

        :param arrAlarmArray: Return alarm history
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_SYSINFO_OUT()
            nResult = MXP_SoftMotion.MXP_GetSystemInformation(ctypes.byref(nIn))
            arrAlarmArray[:] = nIn.Alarm.History
            return nResult
        except Exception as ex:
            print('SYS_GetEtherCATHistoryAlarm', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_GetSlaveName(self, nSlaveNo:c_uint32,strName):
        ''' Return the slave name of entered slave number

        :param nSlaveNo: Set the Slave number
        :param strName: Return the slave name
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            path_buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            nResult = MXP_SoftMotion.MXP_GetSlaveName(nSlaveNo,path_buf)
            strName[0] = path_buf.value
            return nResult
        except Exception as ex:
            print('ECAT_GetSlaveName', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_SetMasterOnlineMode(self,nMode:MXP_SoftMotion.EC_NETWORK_CMD):
        ''' When MXP state is running, Set the mode of master

        :param nMode:Set the mode(0:Init, 1:ProOP, 2:Boot, 4:SafeOP, 8:OP)
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_ET_SetMasterOnlineMode(nMode)
            return nResult
        except Exception as ex:
            print('ECAT_SetMasterOnlineMode', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_SetSlaveOnlineMode(self,nSlaveNo:c_uint32, nMode:MXP_SoftMotion.EC_NETWORK_CMD):
        '''When MXP state is running, Set the mode of slave

        :param nSlaveNo:Set the slave number
        :param nMode:>Set the mode(0:Init, 1:ProOP, 2:Boot, 4:SafeOP, 8:OP)
        :return:The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_ET_SetSlaveOnlineMode(nSlaveNo,nMode)
            return nResult
        except Exception as ex:
            print('ECAT_SetSlaveOnlineMode', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_Reset(self):
        ''' This function Restart the MXP

        :return:The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_SystemReset()
            return nResult
        except Exception as ex:
            print('SYS_Reset', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_SlaveReadyCheck(self,nSlaveNo:c_uint32, bReady:c_bool):
        '''Check the slave communication ready status

        :param nSlaveNo:Set the Slave number
        :param bReady:Return the value which check the slave communication status
        :return:The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nStatus = [0]
            nOnlineState = [0]
            bReady[0] = 0
            nResult = self.SYS_GetStatus(nStatus)
            if nStatus[0] >= KERNEL_STATUS.SYSTEM_RUN:
                nResult = self.ECAT_GetMasterOnlineMode(nOnlineState)
                if nOnlineState[0] == MXP_ONLINE_STATE.ONLINE_STATE_OP:
                    nResult = self.ECAT_GetSlaveCurrentState(nSlaveNo,nOnlineState)
                    if nOnlineState[0] == MXP_ONLINE_STATE.ONLINE_STATE_OP:
                        bReady[0] = 1

            return nResult
        except Exception as ex:
            print('ECAT_SetSlaveOnlineMode', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_ReadyCheck(self, bReady:c_bool):
        '''Check the slave communication ready status

        :param bReady:Return the value which check the slave communication status
        :return:The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nStatus = [0]
            nOnlineState = [0]
            bReady[0] = 0
            nSlaveCount = [0]
            bReady[0] = 0
            nResult = self.SYS_GetStatus(nStatus)
            if nStatus[0] >= KERNEL_STATUS.SYSTEM_RUN:
                nResult = self.ECAT_GetMasterOnlineMode(nOnlineState)
                if nOnlineState[0] == MXP_ONLINE_STATE.ONLINE_STATE_OP:
                    nResult = self.ECAT_GetSlaveCount(nSlaveCount)
                    for i in range(nSlaveCount[0]):
                        nResult = self.ECAT_GetSlaveCurrentState(i,nOnlineState)
                        if nOnlineState[0] != MXP_ONLINE_STATE.ONLINE_STATE_OP:
                            bReady[0] = 0
                            return nResult
                    bReady[0] = 1
            return nResult
        except Exception as ex:
            print('ECAT_SetSlaveOnlineMode', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...

    # endregion

    # region SingleAxis
    def AX_Power(self, nAxisNo: c_uint32, bEnable: c_bool):
        ''' Control the servo on/off state of the specified axis

        :param nAxisNo: Axis number(0 ~ 127)
        :param bEnable: TRUE : Servo On, FALSE : Servo Off
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_POWER_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_POWER_IN(nAxisNo, bEnable, 0, 0)
            nResult = MXP_SoftMotion.MXP_PowerCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('MC_Power Exception', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_Reset(self, nAxisNo: c_uint32):
        ''' Reset all axis-related errors and Change the state of the axis from ErrorStop to Standstill

        :param nAxisNo: Axis number(0 ~ 127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_RESETHOME_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_RESET_IN()
            nIn.Axis = nAxisNo
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_ResetCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_ResetCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('AX_Reset Exception', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_Home(self, nAxisNo:c_uint32):
        ''' Command the servo axis to perform the homing motion

        :param nAxisNo: Axis number(0 ~ 127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_RESETHOME_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_HOME_IN()
            nIn.Axis = nAxisNo
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_HomeCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_HomeCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_Home', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_SetPosition(self, nAxisNo:c_uint32 , fPosition:c_float):
        ''' When selected axis is in the Standstill state, Reset the actual position to set Position

        :param nAxisNo: Axis number(0 ~ 127)
        :param fPosition: Set position value
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_SETPOSITION_IN()
            nIn.Axis = nAxisNo
            nIn.Position = fPosition
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_SetPositionCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_SetPositionCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_SetPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_Halt(self, nAxisNo:c_uint32 , fDec:c_float, fJerk:c_float):
        ''' Stop the ongoing motion and Transfer the axis to the Standstill state

        :param nAxisNo: Axis number(0 ~ 127)
        :param fDec: Set decelation value
        :param fJerk: Set Jerk value
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_HALT_IN(nAxisNo, False ,fDec, fJerk , MXP_BUFFERMODE_ENUM.MXP_ABORTING)
            nResult= MXP_SoftMotion.MXP_HaltCmd(nMotionIndex, byref(nIn))
            nIn = MXP_SoftMotion.MXP_HALT_IN(nAxisNo, True ,fDec, fJerk , MXP_BUFFERMODE_ENUM.MXP_ABORTING)
            nResult= MXP_SoftMotion.MXP_HaltCmd(nMotionIndex, byref(nIn))

            mAxisSequenceData[nAxisNo].bRunFlag = False

            return  nResult
        except Exception as ex:
            print('MC_Halt Exception', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_Stop(self, nAxisNo:c_uint32 , bExecute:c_bool,fDec:c_float,fJerk:c_float):
        ''' Stop the ongoing motion and Transfer the axis to the Stopping state
         To perform another motion command, the execute parameter must be changed from true to false
        :param nAxisNo: Axis number(0 ~ 127)
        :param bExecute: Execute the command with rising edge
        :param fDec: Set Decelation value
        :param fJerk:S et Jerk value
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_STOP_IN()
            nIn.Axis = nAxisNo
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.Execute = bExecute
            nResult = MXP_SoftMotion.MXP_StopCmd(nMotionIndex, ctypes.byref(nIn))
            if nIn.Execute == True:
                mAxisSequenceData[nAxisNo].bRunFlag = False
            return nResult

        except Exception as ex:
            print('AX_SetPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_MoveAbsolute(self, nAxisNo:c_uint32 , fPosition:c_float, fVel:c_float, fAcc:c_float \
                        , fDec:c_float, fJerk:c_float ,nDirection:MXP_DIRECTION_ENUM , nBufferMode:MXP_BUFFERMODE_ENUM ):
        ''' Move the axis from the actual position to a specified absolute position


        :param nAxisNo: Axis number(0 ~ 127)
        :param fPosition: Set Position value
        :param fVel: Set Velocity value
        :param fAcc: Set Acceleration value
        :param fDec: Set Deceleration value
        :param fJerk: Set Jerk value
        :param nDirection: Set Direction of movement
        :param nBufferMode: Set Buffer mode
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVEABSOLUTE_IN(nAxisNo, False, 0, fPosition, fVel, fAcc, fDec,
                                                                                      fJerk, nDirection, nBufferMode)
            nResult= MXP_SoftMotion.MXP_MoveAbsoluteCmd(nMotionIndex, byref(nIn))
            nIn = MXP_SoftMotion.MXP_MOVEABSOLUTE_IN(nAxisNo, True, 0, fPosition, fVel,fAcc, fDec,
                                                                                      fJerk, nDirection, nBufferMode)
            nResult= MXP_SoftMotion.MXP_MoveAbsoluteCmd(nMotionIndex, byref(nIn))

            return  nResult
        except Exception as ex:
            print('MC_MoveAbsolute Exception', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MoveRelative(self, nAxisNo:c_uint32 , fDistance:c_float, fVel:c_float, fAcc:c_float \
                        , fDec:c_float, fJerk:c_float , nBufferMode:MXP_BUFFERMODE_ENUM ):
        ''' Move the axis from the actual position by the distance set in the distance input

        :param nAxisNo: Axis number(0 ~ 127)
        :param fDistance: Set Distance
        :param fVel: Set Velocity value
        :param fAcc: Set Acceleration value
        :param fDec: Set Deceleration value
        :param fJerk: Set Jerk value
        :param nBufferMode: Set Buffer mode
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVERELATIVE_IN()
            nIn.Axis = nAxisNo
            nIn.Distance = fDistance
            nIn.Velocity = fVel
            nIn.Acceleration = fAcc
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveRelativeCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveRelativeCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('AX_MoveRelative', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR






    def AX_MoveAbsolute_Ex(self, nAxisNo:c_uint32 ,nCommandBlockNo:c_uint16, fPosition:c_float, fVel:c_float, fAcc:c_float \
                        , fDec:c_float, fJerk:c_float ,nDirection:MXP_DIRECTION_ENUM , nBufferMode:MXP_BUFFERMODE_ENUM ):
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVEABSOLUTE_EX_IN(nAxisNo,nCommandBlockNo, False, 0, fPosition, fVel, fAcc, fDec,
                                                                                      fJerk, nDirection, nBufferMode)
            nResult= MXP_SoftMotion.MXP_MoveAbsoluteCmd_Ex(nMotionIndex, byref(nIn))
            nIn = MXP_SoftMotion.MXP_MOVEABSOLUTE_EX_IN(nAxisNo,nCommandBlockNo, True, 0, fPosition, fVel,fAcc, fDec,
                                                                                      fJerk, nDirection, nBufferMode)
            nResult= MXP_SoftMotion.MXP_MoveAbsoluteCmd_Ex(nMotionIndex, byref(nIn))

            return  nResult
        except Exception as ex:
            print('AX_MoveAbsolute_Ex Exception', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MoveRelative_Ex(self, nAxisNo:c_uint32 ,nCommandBlockNo:c_uint16 , fDistance:c_float, fVel:c_float, fAcc:c_float \
                        , fDec:c_float, fJerk:c_float , nBufferMode:MXP_BUFFERMODE_ENUM ):

        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVERELATIVE_EX_IN()
            nIn.Axis = nAxisNo
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.Distance = fDistance
            nIn.Velocity = fVel
            nIn.Acceleration = fAcc
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveRelativeCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveRelativeCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('AX_MoveRelative_Ex', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_Dwell_Ex(self, nAxisNo:c_uint32 ,nCommandBlockNo:c_uint16 , fTime:c_float ):

        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_DWELL_EX_IN()
            nIn.Axis = nAxisNo
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.TimeValue = fTime
            nIn.BufferMode = MXP_BUFFERMODE_ENUM.MXP_BUFFERED
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_DwellCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_DwellCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('AX_Dwell_Ex', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_BufferedIO_Ex(self, nAxisNo:c_uint32 ,nCommandBlockNo:c_uint16 , nSlaveNo:c_uint16, nBitPos:c_uint16, bBitValue:c_bool ):

        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_BUFFEREDDIGITALIO_EX_IN()
            nIn.Axis = nAxisNo
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.SlaveNo = nSlaveNo
            nIn.BitPosition = nBitPos
            nIn.BitValue = bBitValue
            nIn.BufferMode = MXP_BUFFERMODE_ENUM.MXP_BUFFERED
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_BufferedDigitalioCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_BufferedDigitalioCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('AX_BufferedIO_Ex', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_MoveVelocity(self, nAxisNo:c_uint32 , fVel:c_float, fAcc:c_float \
                        , fDec:c_float, fJerk:c_float ,nDirection:MXP_DIRECTION_ENUM, nBufferMode:MXP_BUFFERMODE_ENUM):
        ''' Move the axis at the velocity specified in the velocity parameter

        :param nAxisNo: Axis number(0 ~ 127)
        :param fVel: Set Velocity value
        :param fAcc: Set Acceleration value
        :param fDec: Set Deceleration value
        :param fJerk: Set Jerk value
        :param nDirection: Set Direction of movement
        :param nBufferMode: Set Buffer mode
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVEVELOCITY_IN()
            nIn.Axis = nAxisNo
            nIn.Velocity = fVel
            nIn.Acceleration = fAcc
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.Direction = nDirection
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveVelocityCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveVelocityCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('AX_MoveVelocity', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_SetOverride(self, nAxisNo:c_uint32 , fVelFactor:c_float):
        ''' Set the velocity rate for all function
         The factor can be set as a real number from 0 to 1(0 ~ 100%)

        :param nAxisNo: Axis number(0 ~ 127)
        :param fVelFactor: Set the velocity scale factor as a multiplier of a real number
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_SETOVERRIDE_IN()
            nIn.Axis = nAxisNo
            nIn.VelFactor = fVelFactor
            nIn.Enable = 0
            nResult = MXP_SoftMotion.MXP_SetOverrideCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_SetOverrideCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('AX_SetOverride', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_ReadyCheck(self, nAxisNo:c_uint32 , bReady:c_bool):
        ''' Check the Axis ready status

        :param nAxisNo: Set the number of the axis(0~127)
        :param bReady: Return the value which check the axis status
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nState = MXP_AxisStateBit()
            nResult = self.AX_ReadStatus(nAxisNo, nState)
            if nState.PowerOn == 1 and nState.Standstill == 1:
                bReady[0] = True
            else:
                bReady[0] = False
            return nResult

        except Exception as ex:
            print('AX_ReadyCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MoveStateCheck(self, nAxisNo:c_uint32 , fTargetPos:c_float, fInPositionCheckRange:c_float,
                          nMoveState:MXP_MOVESTATE):
        ''' Check the Axis move status

        :param nAxisNo: Set the number of the axis(0~127)
        :param fTargetPos: Set the target position which wrote when you call the Axis move motion function
        :param fInPositionCheckRange: Set the inposition range
        :param nMoveState: Return the move status
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nCurPos = [0]
            nState = MXP_AxisStateBit()
            bInpos = [False]
            nResult = self.AX_ReadActualPosition(nAxisNo, nCurPos)
            nResult = self.AX_ReadStatus(nAxisNo, nState)

            if abs(fTargetPos - nCurPos[0]) < fInPositionCheckRange:
                bInpos[0] = True
            if nState.Standstill ==1 and bInpos[0] == True:
                nMoveState[0] = MXP_MOVESTATE.MOVESTATE_Complete
            elif nState.ErrorStop == 1:
                nMoveState[0] = MXP_MOVESTATE.MOVESTATE_Fail
            elif nState.ConstantVelocity == 1 or nState.Accelerating == 1 or nState.Decelerating == 1:
                nMoveState[0] = MXP_MOVESTATE.MOVESTATE_Moving
            else:
                nMoveState[0] = MXP_MOVESTATE.MOVESTATE_Null
            return nResult

        except Exception as ex:
            print('AX_MoveStateCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...

    # endregion

    # region Monitoring

    def AX_ReadStatus(self, nAxisNo:c_uint32 , stAxisStatus:MXP_AxisStateBit):
        ''' Return the selected axis status.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127).
        :param stAxisStatus: Return the Axis State value(Type:MXP_AxisStateBit).
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READSTATUS_IN(nAxisNo,True)
            nOut = MXP_SoftMotion.MXP_READSTATUS_OUT()

            nResult = MXP_SoftMotion.MXP_ReadStatus(ctypes.byref(nIn), ctypes.byref(nOut))
            stAxisStatus.ErrorStop = nOut.ErrorStop
            stAxisStatus.Disable = nOut.Disabled
            stAxisStatus.Stopping = nOut.Stopping
            stAxisStatus.Standstill = nOut.Standstill
            stAxisStatus.DiscreteMotion = nOut.DiscreteMotion
            stAxisStatus.ContinuousMotion = nOut.ContinuousMotion
            stAxisStatus.SynchronizedMotion = nOut.SynchronizedMotion
            stAxisStatus.Homing = nOut.Homing

            nIn2 = MXP_SoftMotion.MXP_READMOTIONSTATE_IN(nAxisNo,True ,0)
            nOut2 = MXP_SoftMotion.MXP_READMOTIONSTATE_OUT()
            nResult = MXP_SoftMotion.MXP_ReadMotionState(ctypes.byref(nIn2), ctypes.byref(nOut2))
            stAxisStatus.ConstantVelocity = nOut2.ConstantVelocity
            stAxisStatus.Accelerating = nOut2.Accelerating
            stAxisStatus.Decelerating = nOut2.Decelerating
            stAxisStatus.DirectionPositive = nOut2.DirectionPositive
            stAxisStatus.DirectionNegative = nOut2.DirectionNegative


            nIn3 = MXP_SoftMotion.MXP_READAXISINFO_IN(nAxisNo,True)
            nOut3 = MXP_SoftMotion.MXP_READAXISINFO_OUT()
            nResult = MXP_SoftMotion.MXP_ReadAxisInfo(ctypes.byref(nIn3), ctypes.byref(nOut3))
            stAxisStatus.HomeAbsSwitch = nOut3.HomeAbsSwitch
            stAxisStatus.HWLimitSwitchPosEvent = nOut3.LimitSwitchPos
            stAxisStatus.HWLimitSwitchNegEvent = nOut3.LimitSwitchNeg
            stAxisStatus.ReadyForPowerOn = nOut3.ReadyForPowerOn
            stAxisStatus.PowerOn = nOut3.PowerOn
            stAxisStatus.IsHomed = nOut3.IsHomed
            stAxisStatus.AxisWarning = nOut3.AxisWarning
            return  nResult
        except Exception as ex:
            print('MC_ReadAxisStatus' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadActualPosition(self, nAxisNo:c_uint32 , fPosition:c_float):
        ''' Return the actual position of the specified axis.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127).
        :param fPosition: Return the position value.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALPOSITION_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALPOSITION_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadActualPosition(ctypes.byref(nIn), ctypes.byref(nOut))
            fPosition[0] = nOut.Position
            return  nResult
        except Exception as ex:
            print('AX_ReadActualPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadActualVelocity(self, nAxisNo:c_uint32 , fVelocity:c_float):
        ''' Return the actual position of the specified axis.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127)
        :param fVelocity: Returns the velocity (position/time) value.
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALVELOCITY_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALVELOCITY_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1

            nResult = MXP_SoftMotion.MXP_ReadActualVelocity(ctypes.byref(nIn), ctypes.byref(nOut))
            fVelocity[0] = nOut.Velocity
            return  nResult
        except Exception as ex:
            print('AX_ReadActualVelocity', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadFollowingError(self, nAxisNo:c_uint32 , fFollowingErrorValue:c_float):
        ''' Returns the Following Error values of the axes commanded.

        :param nAxisNo: Set the number of the axis to read the Following Error value(0~127).
        :param fFollowingErrorValue: Return the Following Error value.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READFOLLOWINGERRORVALUE_IN()
            nOut = MXP_SoftMotion.MXP_READFOLLOWINGERRORVALUE_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadFollowingErrorValue(ctypes.byref(nIn), ctypes.byref(nOut))
            fFollowingErrorValue[0] = nOut.FollowingErrorValue
            return  nResult
        except Exception as ex:
            print('AX_ReadFollowingError', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadActualTorque(self, nAxisNo:c_uint32 , fTorque:c_float):
        ''' Return the actual torque of the specified axis.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127).
        :param fTorque: Return the rated torque value of the specified axis as a percentage (%).
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALTORQUE_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALTORQUE_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadActualTorque(ctypes.byref(nIn), ctypes.byref(nOut))
            fTorque[0] = nOut.Torque
            return nResult
        except Exception as ex:
            print('AX_ReadActualTorque', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadCommandPosition(self, nAxisNo:c_uint32 , fPosition:c_float):
        ''' This function block returns the position commanded to the servo drive in real time.

        :param nAxisNo: Set the number of the axis to which the motion command is instructed(0~127).
        :param fPosition: Return the command position.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READCOMMANDPOSITION_IN()
            nOut = MXP_SoftMotion.MXP_READCOMMANDPOSITION_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1

            nResult = MXP_SoftMotion.MXP_ReadCommandPosition(ctypes.byref(nIn), ctypes.byref(nOut))
            fPosition[0] = nOut.CommandPosition
            return  nResult
        except Exception as ex:
            print('AX_ReadCommandPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadCommandVelocity(self, nAxisNo:c_uint32 , fVelocity:c_float):
        ''' This function block returns the velocity commanded to the servo drive in real time.

        :param nAxisNo: Set the number of the axis to which the motion command is instructed(0~127).
        :param fVelocity: Return the command velocity.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READCOMMANDVELOCITY_IN()
            nOut = MXP_SoftMotion.MXP_READCOMMANDVELOCITY_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1

            nResult = MXP_SoftMotion.MXP_ReadCommandVelocity(ctypes.byref(nIn), ctypes.byref(nOut))
            fVelocity[0] = nOut.CommandVelocity
            return  nResult
        except Exception as ex:
            print('AX_ReadCommandVelocity', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ReadError(self, nAxisNo:c_uint32 , stAxisError:AXIS_ERROR):
        ''' Return an error code when the axis is in the ErrorStop state.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127).
        :param stAxisError: Return the error state(Type:AXIS_ERROR).
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READAXISERROR_IN()
            nOut = MXP_SoftMotion.MXP_READAXISERROR_OUT()
            nIn.Axis = nAxisNo
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadAxisError(ctypes.byref(nIn), ctypes.byref(nOut))
            stAxisError.MXPError = nOut.AxisErrorID
            stAxisError.DriveError = nOut.AuxErrorID
            return  nResult
        except Exception as ex:
            print('AX_ReadError', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...

    # endregion

    #region Group

    def GRP_ReadStatus(self, nAxesGroup:c_uint32 , stAxisStatus:MXP_AxisStateBit):

        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READSTATUS_IN()
            nOut = MXP_SoftMotion.MXP_READSTATUS_OUT()


            nGroupAxisInfo = []
            for i in range(9):
                nGroupAxisInfo.append(-1)
            nResult = self.GRP_GetGroupAxis(nAxesGroup , nGroupAxisInfo)
            if nResult != 0:
                return nResult
            for i in range(len(nGroupAxisInfo)):
                if nGroupAxisInfo[i] != -1:
                    nIn = MXP_SoftMotion.MXP_READSTATUS_IN(nGroupAxisInfo[i],True)
                    nResult = MXP_SoftMotion.MXP_ReadStatus(ctypes.byref(nIn), ctypes.byref(nOut))
                    if nResult != 0:
                        return nResult
                    if nOut.Disabled:
                        stAxisStatus.Disable = True
                    if nOut.ErrorStop:
                        stAxisStatus.ErrorStop = True
                    if nOut.Stopping:
                        stAxisStatus.Stopping = True
                    if nOut.DiscreteMotion:
                        stAxisStatus.DiscreteMotion = True
                    if nOut.ContinuousMotion:
                        stAxisStatus.ContinuousMotion = True
                    if nOut.SynchronizedMotion:
                        stAxisStatus.SynchronizedMotion = True
                    if nOut.Homing:
                        stAxisStatus.Homing = True

            if stAxisStatus.Disable == False and stAxisStatus.ErrorStop == False  and stAxisStatus.Stopping == False and stAxisStatus.DiscreteMotion == False and \
                    stAxisStatus.ContinuousMotion == False and stAxisStatus.SynchronizedMotion == False and stAxisStatus.Homing == False:
                stAxisStatus.Standstill = True

            return  nResult
        except Exception as ex:
            print('GRP_ReadStatus' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_GetGroupAxis(self, nAxesGroup:c_uint32 , arrAxisNo):
        ''' Return the axis number from the entered group number.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param arrAxisNo: Return the axis numbers in group.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisCount = [0]
            nResult  = self.ECAT_GetAxisCount(nAxisCount)
            if nResult != 0: return  nResult
            nCount = 0
            for i in range(nAxisCount[0]):
                nGroupUsing = [0]
                nGroupNo = [0]
                nAxis = [0]
                nResult = self.AX_ReadParameter(i,400,nGroupUsing)
                nResult = self.AX_ReadParameter(i,401,nGroupNo)
                nResult = self.AX_ReadParameter(i,402,nAxis)
                if nGroupUsing[0] == 1 and nGroupNo[0] == nAxesGroup:
                    arrAxisNo[nCount] = i
                    nCount = nCount + 1
            return  nResult
        except Exception as ex:
            print('GRP_GetGroupAxis', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def GRP_ReadyCheck(self, nAxesGroup:c_uint32 , bReady:c_bool):
        ''' Check the Axis ready status

        :param nAxesGroup: Set the number of the group(0~31)
        :param bReady: Return the value which check the axis status
        :return: The result of calling the function is returned
        '''
        try:
            arrGroupAxisInfo = []
            nResult = MXP_FUNCTION_STATUS
            for i in range(9):
                arrGroupAxisInfo.append(-1)
            nResult = self.GRP_GetGroupAxis(nAxesGroup, arrGroupAxisInfo)

            for ncount  in range(len(arrGroupAxisInfo)):
                if arrGroupAxisInfo[ncount] >-1:
                    nState = MXP_AxisStateBit()
                    nResult = self.AX_ReadStatus(arrGroupAxisInfo[ncount], nState)
                    if nState.PowerOn == 1 and nState.Standstill == 1:
                        bReady[0] = True
                    else:
                        bReady[0] = False
                    if bReady[0] == False:
                        return nResult
            return  nResult

        except Exception as ex:
            print('AX_ReadyCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_Stop(self, nAxesGroup:c_uint32 , bExecute:c_bool, fDec:c_float, fJerk:c_float):
        ''' Command a controlled motion stop on the motor axes of the specified axis group.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param bExecute: Execute the command with rising edge.
        :param fDec: Set the deceleration.
        :param fJerk: Set the jerk value.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVECIRCULARABSOLUTE_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.Execute = bExecute

            nResult = MXP_SoftMotion.MXP_GroupStopCmd(nMotionIndex, ctypes.byref(nIn))
            if nIn.Execute:
                mGroupSequenceData[nAxesGroup].bRunFlag = False

            return nResult

        except Exception as ex:
            print('GRP_Stop Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_MoveLinearAbsolute(self, nAxesGroup:c_uint32 , stPosition:GROUP_POS,fVelocity:c_float,
                               fAcceleration:c_float,fDeceleration:c_float,fJerk:c_float,
                               nBufferMode:MXP_BUFFERMODE_ENUM):
        ''' Command a linear interpolation motion from the actual position to a specified absolute position.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param stPosition: Set the position value of the path.
        :param fVelocity: Set the velocity of the path.
        :param fAcceleration: Set the acceleration of the path.
        :param fDeceleration: Set the deceleration of the path.
        :param fJerk: Set the jerk of the path.
        :param nBufferMode: Set the buffer mode.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVELINEARABSOLUTE_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.PositionX = stPosition.nX
            nIn.PositionY = stPosition.nY
            nIn.PositionZ = stPosition.nZ
            nIn.PositionU = stPosition.nU
            nIn.PositionV = stPosition.nV
            nIn.PositionW = stPosition.nW
            nIn.PositionA = stPosition.nA
            nIn.PositionB = stPosition.nB
            nIn.PositionC = stPosition.nC
            nIn.Velocity = fVelocity
            nIn.Acceleration = fAcceleration
            nIn.Deceleration = fDeceleration
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveLinearAbsoluteCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveLinearAbsoluteCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('GRP_MoveLinearAbsolute Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR
    def GRP_MoveLinearRelative(self, nAxesGroup:c_uint32 , stDistance:GROUP_POS,fVelocity:c_float,
                               fAcceleration:c_float,fDeceleration:c_float,fJerk:c_float,
                               nBufferMode:MXP_BUFFERMODE_ENUM):
        ''' Command a linear interpolation from the actual position by the specified distance.

        :param nAxesGroup: Set the number of the target group(0~31)
        :param stDistance: Set the distance value of the path
        :param fVelocity: Set the velocity of the path
        :param fAcceleration: Set the acceleration of the path
        :param fDeceleration: Set the deceleration of the path
        :param fJerk: Set the jerk of the path
        :param nBufferMode: Set the buffer mode
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVELINEARRELATIVE_IN()
            nIn.AxesGroup = nAxesGroup

            nIn.DistanceX = stDistance.nX
            nIn.DistanceY = stDistance.nY
            nIn.DistanceZ = stDistance.nZ
            nIn.DistanceU = stDistance.nU
            nIn.DistanceV = stDistance.nV
            nIn.DistanceW = stDistance.nW
            nIn.DistanceA = stDistance.nA
            nIn.DistanceB = stDistance.nB
            nIn.DistanceC = stDistance.nC

            nIn.Velocity = fVelocity
            nIn.Acceleration = fAcceleration
            nIn.Deceleration = fDeceleration
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveLinearRelativeCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveLinearRelativeCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult

        except Exception as ex:
            print('GRP_MoveLinearRelative Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def GRP_MoveLinearAbsolute_Ex(self, nAxesGroup:c_uint32, nCommandBlockNo:c_uint16 , stPosition:GROUP_POS,fVelocity:c_float,
                               fAcceleration:c_float,fDeceleration:c_float,fJerk:c_float,
                               nBufferMode:MXP_BUFFERMODE_ENUM):
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVELINEARABSOLUTE_EX_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.PositionX = stPosition.nX
            nIn.PositionY = stPosition.nY
            nIn.PositionZ = stPosition.nZ
            nIn.PositionU = stPosition.nU
            nIn.PositionV = stPosition.nV
            nIn.PositionW = stPosition.nW
            nIn.PositionA = stPosition.nA
            nIn.PositionB = stPosition.nB
            nIn.PositionC = stPosition.nC
            nIn.Velocity = fVelocity
            nIn.Acceleration = fAcceleration
            nIn.Deceleration = fDeceleration
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveLinearAbsoluteCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveLinearAbsoluteCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('GRP_MoveLinearAbsolute_Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def GRP_MoveLinearRelative_Ex(self, nAxesGroup:c_uint32 , nCommandBlockNo:c_uint16, stDistance:GROUP_POS,fVelocity:c_float,
                               fAcceleration:c_float,fDeceleration:c_float,fJerk:c_float,
                               nBufferMode:MXP_BUFFERMODE_ENUM):
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVELINEARRELATIVE_EX_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.DistanceX = stDistance.nX
            nIn.DistanceY = stDistance.nY
            nIn.DistanceZ = stDistance.nZ
            nIn.DistanceU = stDistance.nU
            nIn.DistanceV = stDistance.nV
            nIn.DistanceW = stDistance.nW
            nIn.DistanceA = stDistance.nA
            nIn.DistanceB = stDistance.nB
            nIn.DistanceC = stDistance.nC

            nIn.Velocity = fVelocity
            nIn.Acceleration = fAcceleration
            nIn.Deceleration = fDeceleration
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveLinearRelativeCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveLinearRelativeCmd_Ex(nMotionIndex, ctypes.byref(nIn))

            return nResult

        except Exception as ex:
            print('GRP_MoveLinearRelative Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_Dwell_Ex(self, nAxesGroup:c_uint32 , nCommandBlockNo:c_uint16, fTime:c_float):
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_GROUPDWELL_EX_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.TimeValue = fTime
            nIn.BufferMode = MXP_BUFFERMODE_ENUM.MXP_BUFFERED
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_GroupDwellCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_GroupDwellCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('GRP_Dwell_Ex Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def GRP_BufferedIO_Ex(self, nAxesGroup:c_uint32 , nCommandBlockNo:c_uint16, nSlaveNo:c_uint16, nBitPos:c_uint16, bBitValue:c_bool):
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_GROUPBUFFEREDDIGITALIO_EX_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.CommandBlockNo = nCommandBlockNo
            nIn.SlaveNo = nSlaveNo
            nIn.BitPosition = nBitPos
            nIn.BitValue = bBitValue
            nIn.BufferMode = MXP_BUFFERMODE_ENUM.MXP_BUFFERED
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_GroupBufferedDigitalioCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_GroupBufferedDigitalioCmd_Ex(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('GRP_BufferedIO_Ex Ex =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR









    def GRP_MoveCircularAbsolute(self, nAxesGroup:c_uint32 , nPathChoice:MXP_PATHCHOICE_ENUM
                                ,fAuxPoint1:c_float , fAuxPoint2:c_float, fEndPoint1:c_float ,fEndPoint2:c_float
                                , nPlane1: MXP_PLANE,nPlane2:MXP_PLANE,fVelocity:c_float,fAcceleration:c_float,
                                 fDeceleration:c_float,fJerk:c_float,nBufferMode:MXP_BUFFERMODE_ENUM):
        ''' Command a circular interpolation based on the actual position and the absolute coordinate system.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param nPathChoice: Set the direction of the circular path (0: clockwise, 1: counterclockwise).
        :param fAuxPoint1: Set the center point of the circle on Plane1.
        :param fAuxPoint2: Set the center point of the circle on Plane2.
        :param fEndPoint1: Set the end point of the circle on Plane1.
        :param fEndPoint2: Set the end point of the circle on Plane2.
        :param nPlane1: Specify a plane to be Plane1 (X-C: 0~8)
        :param nPlane2: Specify a plane to be Plane2 (X-C: 0~8)
        :param fVelocity: Set the velocity of the path.
        :param fAcceleration: Set the acceleration of the path.
        :param fDeceleration: Set the deceleration of the path.
        :param fJerk: Set the jerk of the path.
        :param nBufferMode: Set the buffer mode.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVECIRCULARABSOLUTE_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.CircMode = 0
            nIn.AuxPoint1 = fAuxPoint1
            nIn.AuxPoint2 = fAuxPoint2
            nIn.EndPoint1 = fEndPoint1
            nIn.EndPoint2 = fEndPoint2
            nIn.PathChoice = nPathChoice
            nIn.Plane1 = nPlane1
            nIn.Plane2 = nPlane2
            nIn.Velocity = fVelocity
            nIn.Acceleration = fAcceleration
            nIn.Deceleration = fDeceleration
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveCircularAbsoluteCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveCircularAbsoluteCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('GRP_MoveCircularAbsolute  =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_MoveCircularRelative(self, nAxesGroup:c_uint32,nPathChoice:MXP_PATHCHOICE_ENUM
                                ,fAuxPoint1:c_float,fAuxPoint2:c_float, fEndPoint1:c_float
                                 ,fEndPoint2:c_float,nPlane1: MXP_PLANE,nPlane2:MXP_PLANE,fVelocity:c_float
                                 ,fAcceleration:c_float,fDeceleration:c_float,fJerk:c_float,
                                 nBufferMode:MXP_BUFFERMODE_ENUM):
        ''' Command a circular interpolation based on the actual position and the relative coordinate system.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param nPathChoice: Set the direction of the circular path (0: clockwise, 1: counterclockwise).
        :param fAuxPoint1: Set the center point of the circle on Plane1 relative to the starting point.
        :param fAuxPoint2: Set the center point of the circle on Plane2 relative to the starting point.
        :param fEndPoint1: Set the end point of the circle on Plane1 relative to the starting point.
        :param fEndPoint2: Set the end point of the circle on Plane2 relative to the starting point.
        :param nPlane1: Specify a plane to be Plane1 (X-C: 0~8).
        :param nPlane2: Specify a plane to be Plane2 (X-C: 0~8).
        :param fVelocity: Set the velocity of the path.
        :param fAcceleration: Set the acceleration of the path.
        :param fDeceleration: Set the deceleration of the path.
        :param fJerk: Set the jerk of the path.
        :param nBufferMode: Set the buffer mode.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_MOVECIRCULARRELATIVE_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.CircMode = 0
            nIn.AuxPoint1 = fAuxPoint1
            nIn.AuxPoint2 = fAuxPoint2
            nIn.EndPoint1 = fEndPoint1
            nIn.EndPoint2 = fEndPoint2
            nIn.PathChoice = nPathChoice
            nIn.Plane1 = nPlane1
            nIn.Plane2 = nPlane2
            nIn.Velocity = fVelocity
            nIn.Acceleration = fAcceleration
            nIn.Deceleration = fDeceleration
            nIn.Jerk = fJerk
            nIn.BufferMode = nBufferMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MoveCircularRelativeCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MoveCircularRelativeCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult

        except Exception as ex:
            print('GRP_MoveCircularRelative  =' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_SetOverride(self, nAxesGroup:c_uint32,fVelFactor:c_float):
        ''' Set the velocity rate for all function in group axis.
         The factor can be set as a real number from 0 to 1(0 ~ 100%).

        :param nAxesGroup: Set the number of the target group(0~31).
        :param fVelFactor: Set the velocity scale factor as a multiplier of a real number.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_GROUPAXIS_INDEX + nAxesGroup
            nIn = MXP_SoftMotion.MXP_GROUPSETOVERRIDE_IN()
            nIn.AxesGroup = nAxesGroup
            nIn.VelFactor = fVelFactor
            nIn.Enable = 0
            nResult = MXP_SoftMotion.MXP_GroupSetOverrideCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_GroupSetOverrideCmd(nMotionIndex, ctypes.byref(nIn))
            print(nIn.AxesGroup , nIn.VelFactor)
            return nResult
        except Exception as ex:
            print('GRP_SetOverride' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def GRP_ReadActualVelocity(self,nAxesGroup:c_uint32,fPathVelocity:c_float):
        ''' Return the actual velocity of the path in real time.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param fPathVelocity: Return the actual velocity of the path.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_GROUPREADACTUALVELOCITY_IN()
            nOut = MXP_SoftMotion.MXP_GROUPREADACTUALVELOCITY_OUT()
            nIn.AxesGroup = nAxesGroup
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_GroupReadActualVelocity(ctypes.byref(nIn), ctypes.byref(nOut))
            fPathVelocity[0] = nOut.PathVelocity
            return  nResult
        except Exception as ex:
            print('GRP_ReadActualVelocity', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def GRP_ReadActualPosition(self, nAxesGroup:c_uint32,stPosition:GROUP_POS):
        '''Return the actual position of each coordinate in real time.

        :param nAxesGroup:Set the number of the target group(0~31).
        :param stPosition:Return the position.
        :return:The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_GROUPREADACTUALPOSITION_IN()
            nOut = MXP_SoftMotion.MXP_GROUPREADACTUALPOSITION_OUT()
            nIn.AxesGroup = nAxesGroup
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_GroupReadActualPosition(ctypes.byref(nIn), ctypes.byref(nOut))
            stPosition.nX = nOut.PositionX
            stPosition.nY = nOut.PositionY
            stPosition.nZ = nOut.PositionZ
            stPosition.nU = nOut.PositionU
            stPosition.nV = nOut.PositionV
            stPosition.nW = nOut.PositionV
            stPosition.nA = nOut.PositionA
            stPosition.nB = nOut.PositionB
            stPosition.nC = nOut.PositionC
            return nResult
        except Exception as ex:
            print('GRP_ReadActualPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_ReadCommandVelocity(self, nAxesGroup:c_uint32,fPathVelocity:c_float):
        ''' Return the command velocity of the path in real time.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param fPathVelocity: Return the command velocity of the path.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_GROUPREADCOMMANDVELOCITY_IN()
            nOut = MXP_SoftMotion.MXP_GROUPREADCOMMANDVELOCITY_OUT()
            nIn.AxesGroup = nAxesGroup
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_GroupReadCommandVelocity(ctypes.byref(nIn), ctypes.byref(nOut))
            fPathVelocity[0] = nOut.PathCommandVelocity
            return nResult
        except Exception as ex:
            print('GRP_ReadCommandVelocity', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_ReadCommandPosition(self, nAxesGroup:c_uint32,stPosition:GROUP_POS):
        ''' Return the actual position of each coordinate in real time.

        :param nAxesGroup: Set the number of the target group(0~31).
        :param stPosition: Return the position.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_GROUPREADCOMMANDPOSITION_IN()
            nOut = MXP_SoftMotion.MXP_GROUPREADCOMMANDPOSITION_OUT()
            nIn.AxesGroup = nAxesGroup
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_GroupReadCommandPosition(ctypes.byref(nIn), ctypes.byref(nOut))
            stPosition.nX = nOut.PositionX
            stPosition.nY = nOut.PositionY
            stPosition.nZ = nOut.PositionZ
            stPosition.nU = nOut.PositionU
            stPosition.nV = nOut.PositionV
            stPosition.nW = nOut.PositionV
            stPosition.nA = nOut.PositionA
            stPosition.nB = nOut.PositionB
            stPosition.nC = nOut.PositionC
            return nResult
        except Exception as ex:
            print('GRP_ReadCommandPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    ...
    #endregion

    # region Parameter

    def AX_ReadParameter(self, nAxisNo:c_uint32 , nParameterNum:c_uint16, fValue:c_float):
        ''' Return the setting value of an axis parameter.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127).
        :param nParameterNum: Set the number of the parameter.
        :param fValue: Return the value of the specified parameter.
        :return: The result of calling the function is returned.
        '''

        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READPARAMETER_IN(nAxisNo,True,nParameterNum)
            nOut = MXP_SoftMotion.MXP_READPARAMETER_OUT()
            nIn.Axis = nAxisNo
            nIn.ParameterNumber = nParameterNum
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadParameter(byref(nIn), ctypes.byref(nOut))
            fValue[0] = nOut.Value
            return nResult
        except Exception as ex:
            print('MC_ReadParameter' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_WriteParameter(self, nAxisNo:c_uint32,nParameterNum:c_uint16,fValue:c_float ):
        ''' Set the value of the motion parameter for the specified axis.

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127).
        :param nParameterNum: Set the number of the parameter.
        :param fValue: Set the new value of the specified parameter.
        :return: The result of calling the function is returned.
        '''

        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_WRITEPARAMETER_IN()
            nIn.Axis = nAxisNo
            nIn.ParameterNumber = nParameterNum
            nIn.Value = fValue
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_WriteParameterCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_WriteParameterCmd(nMotionIndex, ctypes.byref(nIn))
            return  nResult
        except Exception as ex:
            print('AX_WriteParameter' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_StoreParameter(self):
        ''' Store current all parameters.
         If you want to use saved parameter, Use the Upload option in mxConfigurator.

        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_WRITEPARAMETEREX_IN()
            nIn.Execute = 1
            nIn.ExecutionMode = MXP_SoftMotion.MXP_EXECUTIONMODE_ENUM.MXP_IMMEDIATELY
            nResult = MXP_SoftMotion.MXP_WriteParameterExCmd(ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('AX_StoreParameter' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...

    # endregion

    # region PDO_ET

    def ECAT_ReadPdoData(self, nSlaveNo:c_uint32,nDirection:MXP_PDO_DIRECTION,nOffset:c_uint16,
                       nSize:c_uint16,arrValue:bytearray):
        ''' In real time, Return the PDO data currently mapped to the specified slave device.

        :param nSlaveNo: Set the number of the slave(0~127)
        :param nDirection: Set PDO direction(0 : Servo write, 1 : MXP write)
        :param nOffset: Set the offset for PDO mapping.
        :param nSize: Set the size of the PDO data.
        :param arrValue: Return the value.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READPDODATA_IN(nSlaveNo,True,nDirection,nOffset,nSize)
            nOut = MXP_SoftMotion.MXP_READPDODATA_OUT()
            N_array = (c_byte * nSize)()
            nResult = MXP_SoftMotion.MXP_ReadPDOData(ctypes.byref(nIn), ctypes.byref(nOut) ,  N_array )
            arrValue[:] = N_array
            return nResult
        except Exception as ex:
            print('MC_ReadPDOData', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_ReadAxisIO(self,nAxisNo:c_uint32,arrDataArray:bytearray ):
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READOUTPUTS_IN(nAxisNo,True)
            nOut = MXP_SoftMotion.MXP_READOUTPUTS_OUT()
            N_array = (c_uint8 * DefualtIOSize)()
            nResult = MXP_SoftMotion.MXP_ReadOutputs(ctypes.byref(nIn), ctypes.byref(nOut) ,  N_array )
            print(N_array[0] , N_array[1])
            for i in range(nOut.Size):
                arrDataArray[i] = N_array[i]
            return nResult
        except Exception as ex:
            print('MC_IO_Out_Read' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_WrtieAxisIO(self,nAxisNo:c_uint32,nData:bytearray):
        ''' This function writes byte value to the selected slave.

        :param nAxisNo: Number of the slave.
        :param nData: Byte value to write.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetIoIndex(nAxisNo)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN()
            N_array = (c_byte * 4)()
            print('size', len(nData))
            for i in range(len(nData)):
                N_array[i] = nData[i]

            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nAxisNo, False, 4)

            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex, ctypes.byref(nIn), N_array)
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nAxisNo, True, 4)
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex, ctypes.byref(nIn), N_array)
            return nResult
        except Exception as ex:
            print('ECAT_WrtieAxisIO',ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_WrtiePdoData(self,nSlaveNo:c_uint32,nOffset:c_uint16,
                       nSize:c_uint16,arrValue:bytearray):
        ''' Output the data to the PDO currently mapped to the specified slave device.

        :param nSlaveNo: Set the number of the slave(0~127).
        :param nOffset: Set the offset for PDO mapping.
        :param nSize: Set the size of the PDO data.
        :param arrValue: Set the PDO data value.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_PDOWRITE
            nIn = MXP_SoftMotion.MXP_WRITEPDODATA_IN()
            N_array = (c_byte * nSize)()
            for i in range(len(arrValue)):
                N_array[i] = arrValue[i]
            nIn.SourceNo = nSlaveNo
            nIn.Offset = nOffset
            nIn.Size = nSize
            nIn.Direction = MXP_PDO_DIRECTION.e_MXPWrite
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_WritePDODataCmd(nMotionIndex, ctypes.byref(nIn),  N_array)
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_WritePDODataCmd(nMotionIndex, ctypes.byref(nIn), N_array )
            return  nResult
        except Exception as ex:
            print('ECAT_WrtiePdoData Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def ECAT_CoeReadRequest(self, nSlaveNo:c_uint32 ,nIndex:c_uint16,
                       nSubIndex:c_uint16,nSize:c_uint16):
        ''' Read parameters from a slave device through EtherCAT communication.

        :param nSlaveNo: Set the number of the slave(0~127).
        :param nIndex: Set the index of the parameter.
        :param nSubIndex: Set the subIndex value.
        :param nSize: Set the buffer size.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveNo, ECmdType.e_ETParameterReadReq)
            nIn = MXP_SoftMotion.MXP_ET_READPARAMETER_IN()
            nIn.SlaveNo = nSlaveNo
            nIn.Index = nIndex
            nIn.SubIndex = nSubIndex
            nIn.BufLen = nSize
            nResult = MXP_SoftMotion.MXP_ET_ReadParameterCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('ECAT_CoEReadRequest Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_CoeReadReply(self,nSlaveNo:c_uint32,stStatus:READ_ETParameterReply):
        ''' Return the result about calling the ECAT_CoeReadRequest function.

        :param nSlaveNo: Set the number of the slave(0~127)
        :param stStatus: Output the data contained in the specified index of the parameter(Type:READ_ETParameterReply)
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveNo, ECmdType.e_ETParameterReadReq)
            nOut = MXP_SoftMotion.MXP_ET_READPARAMETER_OUT()
            if nMotionIndex ==0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR
            nResult = MXP_SoftMotion.MXP_ET_GetReadParameterOutParam(nMotionIndex, ctypes.byref(nOut))
            for i in range(len(stStatus.ReadData)):
                stStatus.ReadData[i] = nOut.Data[i]
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Valid
            stStatus.ErrorOn = nOut.Errored
            return nResult
        except Exception as ex:
            print('ECAT_CoeReadReply Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_CoeRead(self, nSlaveNo:c_uint32 ,nIndex:c_uint16,
                       nSubIndex:c_uint16,nSize:c_uint16,nWaitTime:c_int32,stStatus:PROCESS_CHECK):
        ''' Read parameters from a slave device through EtherCAT communication.

        :param nSlaveNo: Set the number of the slave(0~127).
        :param nIndex: Set the index of the parameter.
        :param nSubIndex: Set the subIndex value.
        :param nSize: Set the buffer size.
        :param stStatus: return CoeWrite result
        :param nWaitTime: return check wait time
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveNo, ECmdType.e_ETParameterReadReq)
            nIn = MXP_SoftMotion.MXP_ET_READPARAMETER_IN()
            nOut = MXP_SoftMotion.MXP_ET_READPARAMETER_OUT()
            nIn.SlaveNo = nSlaveNo
            nIn.Index = nIndex
            nIn.SubIndex = nSubIndex
            nIn.BufLen = nSize
            nResult = MXP_SoftMotion.MXP_ET_ReadParameterCmd(nMotionIndex, ctypes.byref(nIn))
            if nResult  != 0:
                ClearIndex(nMotionIndex)
                return nResult

            time.sleep(nWaitTime/1000)

            nResult = MXP_SoftMotion.MXP_ET_GetReadParameterOutParam(nMotionIndex, ctypes.byref(nOut))
            if nResult  != 0:
                ClearIndex(nMotionIndex)
                return nResult
            for i in range(len(stStatus.ReadData)):
                stStatus.ReadData[i] = nOut.Data[i]
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Valid
            stStatus.ErrorOn = nOut.Errored

            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('ECAT_CoeRead Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def ECAT_CoeWriteRequest(self,nSlaveNo:c_uint32,nIndex:c_uint16,
                       nSubIndex:c_uint16,nsize:c_uint16,nWrtieData:c_uint32):
        ''' Return the result about calling the ECAT_CoeWriteRequest function.

        :param nSlaveNo: The result of calling the function is returned.
        :param nIndex: Set the index of the parameter.
        :param nSubIndex: Set the subIndex value.
        :param nsize: Set the buffer size.
        :param nWrtieData: Set the data in the parameter.
        :return:
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveNo, ECmdType.e_ETParameterWriteReq)
            nIn = MXP_SoftMotion.MXP_ET_WRITEPARAMETER_IN()
            nIn.SlaveNo = nSlaveNo
            nIn.Index = nIndex
            nIn.SubIndex = nSubIndex
            nIn.BufLen = nsize
            nIn.Data = nWrtieData
            nResult = MXP_SoftMotion.MXP_ET_WriteParameterCmd(nMotionIndex, ctypes.byref(nIn))
            return nResult
        except Exception as ex:
            print('ECAT_CoeWriteRequest Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def ECAT_CoeWriteReply(self,nSlaveNo:c_uint32,stStatus:PROCESS_CHECK):
        ''' Return the result about calling the ECAT_CoeWriteRequest function.

        :param nSlaveNo: Set the number of the slave(0~127).
        :param stStatus: Return the status value(Type:PROCESS_CHECK).
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex =  GetMotionIndexCheck(nSlaveNo, ECmdType.e_ETParameterWriteReq)
            nOut = MXP_SoftMotion.MXP_ET_WRITEPARAMETER_OUT()
            if nMotionIndex ==0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR
            nResult = MXP_SoftMotion.MXP_ET_GetWriteParameterOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored
            return nResult
        except Exception as ex:
            print('ECAT_CoeWriteReply Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def ECAT_CoeWrite(self,nSlaveNo:c_uint32,nIndex:c_uint16,
                       nSubIndex:c_uint16,nsize:c_uint16,nWrtieData:c_uint32,
                      nWaitTime:c_int32, stStatus:PROCESS_CHECK  ):
        ''' Return the result about calling the ECAT_CoeWriteRequest function.

        :param nSlaveNo: The result of calling the function is returned.
        :param nIndex: Set the index of the parameter.
        :param nSubIndex: Set the subIndex value.
        :param nsize: Set the buffer size.
        :param nWrtieData: Set the data in the parameter.
        :param stStatus: return CoeWrite result
        :param nWaitTime: return check wait time
        :return:
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveNo, ECmdType.e_ETParameterWriteReq)
            nIn = MXP_SoftMotion.MXP_ET_WRITEPARAMETER_IN()
            nOut = MXP_SoftMotion.MXP_ET_WRITEPARAMETER_OUT()
            nIn.SlaveNo = nSlaveNo
            nIn.Index = nIndex
            nIn.SubIndex = nSubIndex
            nIn.BufLen = nsize
            nIn.Data = nWrtieData
            nResult = MXP_SoftMotion.MXP_ET_WriteParameterCmd(nMotionIndex, ctypes.byref(nIn))
            if nResult  != 0:
                ClearIndex(nMotionIndex)
                return nResult

            time.sleep(nWaitTime/1000)
            nResult = MXP_SoftMotion.MXP_ET_GetWriteParameterOutParam(nMotionIndex, ctypes.byref(nOut))
            if nResult  != 0:
                ClearIndex(nMotionIndex)
                return nResult

            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored

            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('ECAT_CoeWrite Exception' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    # endregion


    #region PLCInterface

    def PLC_ReadBit(self,nAddress:c_uint32,nBitNo:c_byte,bData:c_bool):
        ''' Read Bit data of PLC from entered address and bit number.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nBitNo: Set the bit number.
        :param bData: Return the bit data of bool format.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS

            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, nBitNo,MXP_DATA_TYPE.DATA_TYPE_Bit,
                                                                byref(nReadData))

            bData[0] = nReadData.value
            return  nResult
        except Exception as ex:
            print('PLC_ReadBit' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadByte(self, nAddress:c_uint32, nData:c_uint8):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the Byte data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Byte,
                                                                byref(nReadData))
            nData[0] = nReadData.value
            return  nResult
        except Exception as ex:
            print('PLC_ReadByte' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def PLC_ReadSByte(self, nAddress:c_uint32, nData:c_int8):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the Byte data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Byte,
                                                                byref(nReadData))
            if nReadData.value <128:
                nData[0] = nReadData.value
            else:
                nData[0] = nReadData.value - 256
            return  nResult
        except Exception as ex:
            print('PLC_ReadByte' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadUInt16(self,nAddress:c_uint32,nData:c_uint16):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the UInt16 data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Word, byref(nReadData))
            nData[0] = nReadData.value
            return  nResult
        except Exception as ex:
            print('PLC_ReadUInt16' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadInt16(self,nAddress:c_uint32,nData:c_int16):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the Int16 data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Word, byref(nReadData))

            nData[0] = uint32_to_int16(nReadData)
            print(nData[0],uint32_to_int16(nReadData))

            return nResult
        except Exception as ex:
            print('PLC_ReadInt16' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def PLC_ReadUInt32(self,nAddress:c_uint32,nData:c_uint32):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the UInt32 data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_L, byref(nReadData))
            nData[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('PLC_ReadUInt32' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadInt32(self, nAddress:c_uint32, nData:c_int32):
        '''Read Byte data of PLC from entered address.
        Address must be over 5000.

        :param nAddress:Set the address number(over 5000).
        :param nData:Return the Int32 data.
        :return:The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_L, byref(nReadData))
            nData[0] = uint32_to_int32(nReadData.value)
            return nResult
        except Exception as ex:
            print('PLC_ReadInt32' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadFloat(self,nAddress:c_uint32,fData:c_float):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param fData: Return the Float data.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint32()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_L, byref(nReadData))
            fData[0] = to_float(nReadData.value)
            return nResult
        except Exception as ex:
            print('PLC_ReadFloat' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def PLC_ReadUInt64(self,nAddress:c_uint32,nData:c_uint64):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the UInt64 data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint64()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegisterEx(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_D, byref(nReadData))
            nData[0] = nReadData.value
            return nResult
        except Exception as ex:
            print('PLC_ReadUInt64' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadInt64(self,nAddress:c_uint32,nData:c_int64):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Return the Int64 data.
        :return: The result of calling the function is returned.
        '''
        try:
            if nAddress <5000:
                return MXP_FUNCTION_STATUS.RET_INVALID_PLCADDRESS
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint64()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegisterEx(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_D, byref(nReadData))
            nData[0] = uint64_to_int64(nReadData)
            return nResult
        except Exception as ex:
            print('PLC_ReadInt64', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_ReadDouble(self, nAddress:c_uint32 , dData:c_double):
        ''' Read Byte data of PLC from entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param dData: Return the Double data.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = c_uint64()
            nResult = MXP_SoftMotion.MXP_PLC_ReadSystemRegisterEx(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_D, byref(nReadData))
            dData[0] = uint64_to_double(nReadData.value)
            return  nResult
        except Exception as ex:
            print('PLC_ReadDouble' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_WriteBit(self,nAddress:c_uint32,nBitNo:c_byte,bData:c_bool):
        ''' Write Bit data to entered address and bit number.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nBitNo: Set the bit number.
        :param bData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''

        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, nBitNo,MXP_DATA_TYPE.DATA_TYPE_Bit, c_uint32(bData))
            return nResult
        except Exception as ex:
            print('PLC_WriteBit' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_WriteByte(self,nAddress:c_uint32,nData:c_byte):
        ''' Write Byte data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Byte, c_uint32(nData))
            return nResult
        except Exception as ex:
            print('PLC_WriteByte' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def PLC_WriteSByte(self,nAddress:c_uint32,nData:c_int8 ):
        ''' Write Byte data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            if nData >0:
                nWriteData =  nData
            else:
                nWriteData = nData + 256
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Byte, c_uint32(nData))
            return nResult
        except Exception as ex:
            print('PLC_WriteSByte' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def PLC_WriteUInt16(self, nAddress:c_uint32 , nData:c_uint16):
        ''' Write UInt16 data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Word, c_uint32(nData))
            return nResult
        except Exception as ex:
            print('PLC_WriteUInt16' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_WriteInt16(self,nAddress:c_uint32,nData:c_int16):
        ''' Write Int16 data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nWriteData = int16_to_uint32(nData)
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_Word, c_uint32(nWriteData))
            return nResult
        except Exception as ex:
            print('PLC_WriteInt16' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def PLC_WriteUInt32(self, nAddress:c_uint32 , nData:c_uint32):
        ''' Write UInt32 data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_L, c_uint32(nData))
            return nResult
        except Exception as ex:
            print('PLC_WriteUInt32' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_WriteInt32(self,nAddress:c_uint32,nData:c_int32):
        ''' Write Int32 data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nWriteData = int32_to_uint32(nData)
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_L, c_uint32(nWriteData))
            return nResult
        except Exception as ex:
            print('PLC_WriteInt32', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def PLC_WriteFloat(self, nAddress:c_uint32 , fData:c_float):
        ''' Write Float data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param fData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nWriteData = to_uint32(fData)
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegister(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_L, c_uint32(nWriteData))
            return  nResult
        except Exception as ex:
            print('MC_PLCWriteFloatData' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR




    def PLC_WriteUInt64(self, nAddress:c_uint32 , nData:c_uint64):
        ''' Write UInt64 data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegisterEx(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_D, c_uint64(nData))
            return nResult
        except Exception as ex:
            print('PLC_WriteUInt64' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def PLC_WriteInt64(self,nAddress:c_uint32,nData:c_int64):
        ''' Write Int64 data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param nData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nWriteData = int64_to_uint64(nData)
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegisterEx(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_D, c_uint64(nWriteData))
            return nResult
        except Exception as ex:
            print('PLC_WriteInt64', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def PLC_WriteDouble(self,nAddress:c_uint32,dData:c_double):
        ''' Write Double data to entered address.
         Address must be over 5000.

        :param nAddress: Set the address number(over 5000).
        :param dData: Set the write data to PLC.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nWriteData = double_to_uint64(dData)
            nResult = MXP_SoftMotion.MXP_PLC_WriteSystemRegisterEx(nAddress, 0,MXP_DATA_TYPE.DATA_TYPE_D, c_uint64(nWriteData))
            return  nResult
        except Exception as ex:
            print('PLC_WriteDouble' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    #endregion

    # region IO


    def IO_ReadBit(self, nSlaveNo:c_uint32,IoType:MXP_IO_Type,nOffset:c_uint16,nBitOffset:c_byte,bData:c_bool):
        ''' This function reads bit value to selected slave.

        :param nSlaveNo: Number of slave.
        :param IoType: MXP_IO_Type(IO_IN or IO_OUT).
        :param nOffset: Start address of  bit to read.
        :param nBitOffset: Bit number of address to read.
        :param bData: Return bit value.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIOCount  = nOffset * 8 + nBitOffset
            if IoType == MXP_IO_Type.IO_IN:
                nResult = self.MC_IO_In_Read_BIT(nSlaveNo, nIOCount, bData)
            else:
                nResult = self.MC_IO_Out_Read_BIT(nSlaveNo, nIOCount, bData)
            return nResult
        except Exception as ex:
            print('IO_ReadBit' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def IO_ReadByte(self,nSlaveNo:c_uint32,IoType:MXP_IO_Type,nOffset:c_uint16,nData:c_byte):
        ''' This function read byte value to selected slave.

        :param nSlaveNo: Number of slave.
        :param IoType: MXP_IO_Type(IO_IN or IO_OUT)
        :param nOffset: Start address of byte to read
        :param nData: Return byte value
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIOSize = [0]
            nArray = bytearray(DefualtIOSize)
            if IoType == MXP_IO_Type.IO_IN:
                nResult = self.MC_IO_In_Read(nSlaveNo, nIOSize,   nArray)
                if nResult != 0:
                    return  nResult
                if nIOSize[0] < nOffset:
                    return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize
                nData[0] = nArray[nOffset]
            else:
                nResult = self.MC_IO_Out_Read(nSlaveNo, nIOSize, nArray)
                if nResult != 0:
                    return  nResult
                if nIOSize[0] < nOffset:
                    return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize
                nData[0] = nArray[nOffset]

            return nResult
        except Exception as ex:
            print('IO_ReadByte' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def IO_ReadWord(self,nSlaveNo:c_uint32,IoType:MXP_IO_Type,nOffset:c_uint16,nData:c_uint16):
        ''' This function read word value to selected slave.

        :param nSlaveNo: Number of slave.
        :param IoType: MXP_IO_Type(IO_IN or IO_OUT)
        :param nOffset: Start address of word to read
        :param nData: Return word value
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIOSize = [0]
            nArray = bytearray(DefualtIOSize)
            if IoType == MXP_IO_Type.IO_IN:
                nResult = self.MC_IO_In_Read(nSlaveNo, nIOSize,   nArray)
            else:
                nResult = self.MC_IO_Out_Read(nSlaveNo, nIOSize, nArray)
            if nResult != 0:
                return  nResult
            if nIOSize[0] < nOffset + 2:
                return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize
            nDataArray = bytearray(2)
            nDataArray[0] = nArray[nOffset]
            nDataArray[1] = nArray[nOffset+1]
            nData[0] = int.from_bytes(nDataArray, 'little', signed=False)
            return nResult
        except Exception as ex:
            print('IO_ReadWord' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR
    def IO_ReadDWord(self,nSlaveNo: c_uint32,IoType: MXP_IO_Type,nOffset:c_uint16,nData: c_uint32):
        ''' This function read Dword value to selected slave.

        :param nSlaveNo: Number of slave.
        :param IoType: MXP_IO_Type(IO_IN or IO_OUT)
        :param nOffset: Start address of Dword to read
        :param nData: Return Dword value
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIOSize = [0]
            nArray = bytearray(DefualtIOSize)
            if IoType == MXP_IO_Type.IO_IN:
                nResult = self.MC_IO_In_Read(nSlaveNo, nIOSize, nArray)
            else:
                nResult = self.MC_IO_Out_Read(nSlaveNo, nIOSize, nArray)
            if nResult != 0:
                return nResult
            if nIOSize[0] < nOffset + 4:
                return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize
            nDataArray = bytearray(4)
            nDataArray[0] = nArray[nOffset]
            nDataArray[1] = nArray[nOffset + 1]
            nDataArray[2] = nArray[nOffset + 2]
            nDataArray[3] = nArray[nOffset + 3]
            nData[0] = int.from_bytes(nDataArray, 'little', signed=False)
            return nResult
        except Exception as ex:
            print('IO_ReadDWord', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def IO_Read(self, nSlaveNo:c_uint32,IoType:MXP_IO_Type,nOffset:c_uint16,nSize:c_uint16,arrData:bytearray):
        ''' This function reads byte array value to selected slave .

        :param nSlaveNo: Number of slave.
        :param IoType: MXP_IO_Type(IO_IN or IO_OUT).
        :param nOffset: Start address of byte array to read.
        :param nSize: Size of the byte array to read.
        :param arrData: Byte array value to read.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIOSize = [0]
            nArray = bytearray(DefualtIOSize)
            if IoType == MXP_IO_Type.IO_IN:
                nResult = self.MC_IO_In_Read(nSlaveNo, nIOSize, nArray)
            else:
                nResult = self.MC_IO_Out_Read(nSlaveNo, nIOSize, nArray)
            if nResult != 0:
                return  nResult
            if nIOSize[0] < nOffset + nSize:
                return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize
            for i in range(nSize):
                arrData[i] = nArray[i+nOffset]
            return nResult
        except Exception as ex:
            print('IO_ReadDWord' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def MC_IO_Out_Read_BIT(self,nSlaveNo:c_uint32,nBitNo:c_byte, bData:c_bool):
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READDIGITALOUTPUT_IN (nSlaveNo,True,nBitNo)
            nOut = MXP_SoftMotion.MXP_READDIGITALOUTPUT_OUT()

            nResult = MXP_SoftMotion.MXP_ReadDigitalOutput(ctypes.byref(nIn), ctypes.byref(nOut))
            bData[0] = nOut.Value
            return nResult
        except Exception as ex:
            print('MC_IO_Out_Read_BIT' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def MC_IO_In_Read_BIT(self, nSlaveNo:c_uint32 , nBitNo:c_byte, bData:c_bool):
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READDIGITALINPUT_IN(nSlaveNo,True,nBitNo)
            nOut = MXP_SoftMotion.MXP_READDIGITALINPUT_OUT()

            nResult = MXP_SoftMotion.MXP_ReadDigitalInput(ctypes.byref(nIn), ctypes.byref(nOut))
            bData[0] = nOut.Value
            return nResult
        except Exception as ex:
            print('MC_IO_In_Read_BIT' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def MC_IO_Out_Read(self,nSlaveNo:c_uint32,nSize:c_uint16,arrDataArray:bytearray ):
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READOUTPUTS_IN(nSlaveNo,True)
            nOut = MXP_SoftMotion.MXP_READOUTPUTS_OUT()
            N_array = (c_uint8 * DefualtIOSize)()
            nResult = MXP_SoftMotion.MXP_ReadOutputs(ctypes.byref(nIn), ctypes.byref(nOut) ,  N_array )
            print(N_array[0] , N_array[1])
            nSize[0] = nOut.Size
            for i in range(nOut.Size):
                arrDataArray[i] = N_array[i]
            return nResult
        except Exception as ex:
            print('MC_IO_Out_Read' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def MC_IO_In_Read(self,nSlaveNo:c_uint32,nSize:c_uint16,arrDataArray:bytearray ):
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READINPUTS_IN(nSlaveNo,True)
            nOut = MXP_SoftMotion.MXP_READINPUTS_OUT()

            N_array = (c_uint8 * DefualtIOSize)()
            nResult = MXP_SoftMotion.MXP_ReadInputs(ctypes.byref(nIn), ctypes.byref(nOut) ,  N_array )
            nSize[0] = nOut.Size
            for i in range(nOut.Size):
                arrDataArray[i] = N_array[i]
            return nResult
        except Exception as ex:
            print('MC_IO_Out_Read' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def IO_WriteBit(self,nSlaveNo:c_uint32,nOffset:c_uint16,nBitOffset:c_byte, bData:c_bool):
        ''' This function writes bit value to the selected slave.

        :param nSlaveNo: Number of the slave.
        :param nOffset: Start address of bit to write.
        :param nBitOffset: Bit number to write(0 ~ 7).
        :param bData: Bit value to write.
        :return: The result of calling the function is returned.
        '''
        try:
            nMotionIndex  = GetIoIndex(nSlaveNo)
            nResult = MXP_FUNCTION_STATUS
            nIOCount = nOffset * 8 + nBitOffset
            nIn = MXP_SoftMotion.MXP_WRITEDIGITALOUTPUT_IN(nSlaveNo,False,nIOCount,bData,0)
            nResult = MXP_SoftMotion.MXP_WriteDigitalOutputCmd(nMotionIndex ,  ctypes.byref(nIn))
            nIn = MXP_SoftMotion.MXP_WRITEDIGITALOUTPUT_IN(nSlaveNo,True,nIOCount,bData,0)
            nResult = MXP_SoftMotion.MXP_WriteDigitalOutputCmd(nMotionIndex ,  ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('IO_WriteBit' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def IO_WriteByte(self,nSlaveNo:c_uint32,nOffset:c_uint16,nData:c_byte):
        ''' This function writes byte value to the selected slave.

        :param nSlaveNo: Number of the slave.
        :param nOffset: Start address of byte to write.
        :param nData: Byte value to write.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetIoIndex(nSlaveNo)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nArray = bytearray(DefualtIOSize)
            nIOSize = [0]
            nResult = self.MC_IO_Out_Read(nSlaveNo,nIOSize,nArray)
            if nResult != 0:
                return nResult
            nArray[nOffset] = nData
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,False,nIOSize[0])
            N_array = (c_uint8 * nIOSize[0])()
            for i in range(nIOSize[0]):
                N_array[i] = nArray[i]
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,True,nIOSize[0])
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            return nResult
        except Exception as ex:
            print('IO_WriteByte',ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def IO_WriteWord(self,nSlaveNo:c_uint32,nOffset:c_uint16,nData:c_uint16):
        ''' This function writes word value to the selected slave.

        :param nSlaveNo: Number of the slave.
        :param nOffset: Start address of byte to write.
        :param nData: word value to write.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetIoIndex(nSlaveNo)
            if nMotionIndex == 0:
                return  MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nArray = bytearray(DefualtIOSize)
            nIOSize = [0]
            nResult = self.MC_IO_Out_Read(nSlaveNo,nIOSize,nArray)
            if nResult != 0:
                return nResult
            if nIOSize[0] < nOffset +2:
                return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize

            nDataArray = bytearray(2)
            nChageData = int2bytes(nData)
            if len(nChageData) !=0:
                nDataArray[0:len(nChageData) -1] = nChageData
            for i in range(len(nDataArray)):
                nArray[nOffset+ i] = nDataArray[i]
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,False,nIOSize[0])
            N_array = (c_uint8 * nIOSize[0])()
            for i in range(nIOSize[0]):
                N_array[i] = nArray[i]
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,True,nIOSize[0])
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            return nResult
        except Exception as ex:
            print('IO_WriteWord', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def IO_WriteDword(self, nSlaveNo:c_uint32 , nOffset:c_uint16 , nData:c_uint32):
        ''' This function writes Dword value to the selected slave.

        :param nSlaveNo: Number of the slave.
        :param nOffset: Start address to write.
        :param nData: Dword value to write.
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetIoIndex(nSlaveNo)
            if nMotionIndex == 0:
                return  MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nArray  = bytearray(DefualtIOSize)
            nIOSize = [0]
            nResult = self.MC_IO_Out_Read(nSlaveNo,nIOSize,nArray)
            if nResult != 0:
                return  nResult
            if nIOSize[0] < nOffset + 4:
                return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize

            nDataArray = bytearray(4)
            nChageData = int2bytes(nData)
            if len(nChageData) !=0:
                nDataArray[0:len(nChageData) -1] = nChageData

            for i in range(len(nDataArray)):
                nArray[nOffset+ i] = nDataArray[i]


            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,False,nIOSize[0])

            N_array = (c_uint8 * nIOSize[0])()
            for i in range(nIOSize[0]):
                N_array[i] = nArray[i]

            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,True,nIOSize[0])
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            return nResult
        except Exception as ex:
            print('IO_WriteDword' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def IO_Write(self, nSlaveNo:c_uint32,nOffset:c_uint16,nSize:c_uint16,arrData:bytearray):
        ''' This function writes byte array value to the selected slave.

        :param nSlaveNo: Number of the slave
        :param nOffset: Start address of array to write
        :param nSize: Size of the write byte array
        :param arrData: Byte array value to write
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetIoIndex(nSlaveNo)
            if nMotionIndex == 0:
                return  MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nArray = bytearray(DefualtIOSize)
            nIOSize = [0]
            nResult = self.MC_IO_Out_Read(nSlaveNo,nIOSize,nArray)
            if nResult != 0:
                return nResult
            if nIOSize[0] < nOffset + nSize:
                return MXP_FUNCTION_STATUS.RET_ERROR_INVAILD_IOSize
            for i in range(nSize):
                nArray[nOffset+ i] = arrData[i]

            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,False,nIOSize[0])
            N_array = (c_uint8 * nIOSize[0])()
            for i in range(nIOSize[0]):
                N_array[i] = nArray[i]

            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            nIn = MXP_SoftMotion.MXP_WRITEOUTPUTS_IN(nSlaveNo,True,nIOSize[0])
            nResult = MXP_SoftMotion.MXP_WriteOutputsCmd(nMotionIndex,ctypes.byref(nIn) , N_array )
            return nResult
        except Exception as ex:
            print('IO_Write' , ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    # endregion


    #region Gear
    def AX_GearIn(self, nMasterAxis:c_uint32,nSlaveAxis:c_uint32,nRatioNumerator:c_int32,
                  nRatioDenominator:c_uint32,nMasterValueSource:MXP_SOURCE_ENUM,fAcc:c_float,
                  fDec: c_float,fJerk: c_float):
        ''' Command a controlled motion on an electronic gear

        :param nMasterAxis: Master Axis number(0 ~ 127)
        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param nRatioNumerator: Set Gear ratio of the slave axis
        :param nRatioDenominator: Set Gear ratio of the master axis
        :param nMasterValueSource: Select master data for synchronization
        :param fAcc: Set Acceleration value
        :param fDec: Set Deceleration value
        :param fJerk: Set Jerk value
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_GearIn)
            nIn = MXP_SoftMotion.MXP_GEARIN_IN()
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nIn.Master = nMasterAxis
            nIn.Slave = nSlaveAxis
            nIn.ContinuousUpdate = 0
            nIn.RatioNumerator = nRatioNumerator
            nIn.RatioDenominator = nRatioDenominator
            nIn.MasterValueSource = nMasterValueSource
            nIn.Acceleration = fAcc
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.BufferMode = MXP_BUFFERMODE_ENUM.MXP_ABORTING
            nIn.Execute = 0

            nResult = MXP_SoftMotion.MXP_GearInCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_GearInCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_GearIn', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_GearInMonitor(self, nSlaveAxis:c_uint32, stStatus:PROCESS_CHECK):
        ''' Return a Status and ErrorID of the slave which is executed GearIn command

        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param stStatus: Return the GearIn status.(type : MXPEasyClass.PROCESS_CHECK)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveAxis, ECmdType.e_GearIn)

            nOut = MXP_SoftMotion.MXP_GEARIN_OUT()
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nResult = MXP_SoftMotion.MXP_GetGearInOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Active
            stStatus.Done = nOut.InGear
            stStatus.ErrorOn = nOut.Errored

            return nResult
        except Exception as ex:
            print('AX_GearInMonitor', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_GearOut(self, nSlaveAxis: c_uint32):
        ''' Disengage a slave axis from the master axis

        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveAxis, ECmdType.e_GearIn)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nIn = MXP_SoftMotion.MXP_GEAROUT_IN(nSlaveAxis, False)
            nResult = MXP_SoftMotion.MXP_GearOutCmd(nMotionIndex,  ctypes.byref(nIn))
            nIn = MXP_SoftMotion.MXP_GEAROUT_IN(nSlaveAxis, True)
            nResult = MXP_SoftMotion.MXP_GearOutCmd(nMotionIndex,  ctypes.byref(nIn))

            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('AX_GearOut', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def AX_GearInPos(self, nMasterAxis: c_uint32, nSlaveAxis: c_uint32, nRatioNumerator: c_int32,
                  nRatioDenominator:c_uint32, nMasterValueSource: MXP_SOURCE_ENUM, fMasterSyncPos: c_float,
                  fSlaveSyncPos:c_float, fMasterStartDistance:c_float, fVel:c_float, fAcc: c_float, fDec: c_float,
                  fJerk: c_float):
        ''' Command a controlled motion on an electronic gear.
         Unlike AX_GearIn, Set the position in which the slave and master axes are synchronized.

        :param nMasterAxis: Master Axis number(0 ~ 127)
        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param nRatioNumerator: Set Gear ratio of the slave axis
        :param nRatioDenominator: Set Gear ratio of the master axis
        :param nMasterValueSource: Select master data for synchronizition
        :param fMasterSyncPos: Set the position where synchronization of the master axis is completed
        :param fSlaveSyncPos: Set the position where synchronization of the slave axis is completed
        :param fMasterStartDistance: Set the position of the master axis where the master axis starts synchronizing with the slave axis
        :param fVel: Set Maximum Velocity of the slave axis until the synchronization is complete
        :param fAcc: Set Maximum Acceleration of the slave axis until the synchronization is complete
        :param fDec: Set Maximum Deceleration of the slave axis until the synchronization is complete
        :param fJerk: Set Maximum Jerk of the slave axis until the synchronization is complete
        :return: The result of calling the function is returned.
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_GearInPos)

            nIn = MXP_SoftMotion.MXP_GEARINPOS_IN()

            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nIn.Master = nMasterAxis
            nIn.Slave = nSlaveAxis
            nIn.RatioNumerator = nRatioNumerator
            nIn.RatioDenominator = nRatioDenominator
            nIn.MasterValueSource = nMasterValueSource
            nIn.MasterSyncPosition = fMasterSyncPos
            nIn.SlaveSyncPosition = fSlaveSyncPos
            nIn.MasterStartDistance = fMasterStartDistance
            nIn.Velocity = fVel
            nIn.Acceleration = fAcc
            nIn.Deceleration = fDec
            nIn.Jerk = fJerk
            nIn.BufferMode = MXP_BUFFERMODE_ENUM.MXP_ABORTING
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_GearInPosCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_GearInPosCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_GearInPos', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_GearInPosMonitor(self, nSlaveAxis:c_uint32, stStatus:PROCESS_CHECK):
        ''' Return a Status and ErrorID of the slave which is executed GearInPos command

        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param stStatus: Return the GearInPos status.(type : MXPEasyClass.PROCESS_CHECK)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveAxis, ECmdType.e_GearInPos)

            nOut = MXP_SoftMotion.MXP_GEARINPOS_OUT()
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nResult = MXP_SoftMotion.MXP_GetGearInPosOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Active
            stStatus.Done = nOut.InSync
            stStatus.ErrorOn = nOut.Errored

            return nResult
        except Exception as ex:
            print('AX_GearInPosMonitor', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_GearInPosOut(self,nSlaveAxis:c_uint32):
        ''' Disengage a slave axis from the master axis

        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveAxis, ECmdType.e_GearIn)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nIn = MXP_SoftMotion.MXP_GEAROUT_IN(nSlaveAxis, False)
            nResult = MXP_SoftMotion.MXP_GearOutCmd(nMotionIndex,  ctypes.byref(nIn))
            nIn = MXP_SoftMotion.MXP_GEAROUT_IN(nSlaveAxis, True)
            nResult = MXP_SoftMotion.MXP_GearOutCmd(nMotionIndex,  ctypes.byref(nIn))
            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('AX_GearInPosOut', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    #endregion

    #region CAM

    def AX_CamTableSelect(self, nMasterAxis:c_uint32, nSlaveAxis:c_uint32, nCamTableID:c_uint16, bPeriodic: c_bool):
        '''  Read the CAM table to use the electronic CAM function

        :param nMasterAxis: Master Axis number(0 ~ 127)
        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param nCamTableID: Set the number of the table to be read in
        :param bPeriodic: Specify whether to execute the table periodically. (0 : NonPeriodic, 1 : Periodic)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_CAMTableOption)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn = MXP_SoftMotion.MXP_CAMTABLESELECT_IN()

            nIn.Master = nMasterAxis
            nIn.Slave = nSlaveAxis
            nIn.CamTable = nCamTableID
            nIn.Periodic  = bPeriodic
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_CamTableSelectCmd(nMotionIndex, ctypes.byref(nIn))

            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_CamTableSelectCmd(nMotionIndex, ctypes.byref(nIn))

            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('AX_CamTableSelect', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamWriteTableRequest(self, nCamTableID: c_uint16, bExecute: c_bool, nTableRowCount: c_int16,
                                arrCamData):
        ''' Write the CAM table data

        :param nCamTableID: Set the table number to write
        :param bExecute: Execute the command with rising edge
        :param nTableRowCount: Set the number of table rows to write
        :param arrCamData: CAM table value to write
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nCamTableID, ECmdType.e_CAMTableEdit)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nIn = MXP_SoftMotion.MXP_WRITECAMTABLE_IN()
            nIn.CamTable = nCamTableID


            for i in range(nTableRowCount):
                nIn.CamDataArray[i].MasterPos = arrCamData[i].MasterPos
                nIn.CamDataArray[i].SlavePos = arrCamData[i].SlavePos
                nIn.CamDataArray[i].SlaveVel = arrCamData[i].SlaveVel
                nIn.CamDataArray[i].SlaveAcc = arrCamData[i].SlaveAcc
                nIn.CamDataArray[i].SlaveJerk = arrCamData[i].SlaveJerk
                nIn.CamDataArray[i].PointType = arrCamData[i].PointType
                nIn.CamDataArray[i].InterpolationType = arrCamData[i].InterpolationType

            if nTableRowCount <100:
                nIn.DataSize = 100
            elif nTableRowCount <200:
                nIn.DataSize = 200
            else:
                nIn.DataSize = 400
            nIn.ExecutionMode = 2
            nIn.Execute = False
            nResult = MXP_SoftMotion.MXP_WriteCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            if bExecute == True:
                nIn.Execute = True
                nResult = MXP_SoftMotion.MXP_WriteCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            else:
                ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('AX_CamWriteTableRequest', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_CamWriteTableReply(self, nCamTableID: c_uint16, stStatus: PROCESS_CHECK):
        ''' Return a Status and ErrorID of the CAM table which is executed AX_CamWriteTableRequest

        :param nCamTableID: CamTableID(0~63)
        :param stStatus: Return the CAMWriteTable status.(type : MXPEasyClass.PROCESS_CHECK)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nCamTableID, ECmdType.e_CAMTableEdit)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nOut = MXP_SoftMotion.MXP_WRITECAMTABLE_OUT()
            nResult = MXP_SoftMotion.MXP_GetWriteCamTableOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored

            return nResult
        except Exception as ex:
            print('AX_CamWriteTableReply', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamWriteTable(self, nCamTableID: c_uint16, nTableRowCount: c_int16,
                                nCamDataArray,nWaitTime:c_int32,stStatus:PROCESS_CHECK ):
        ''' Write the CAM table data

        :param nCamTableID: Set the table number to write
        :param bExecute: Execute the command with rising edge
        :param nTableRowCount: Set the number of table rows to write
        :param nCamDataArray: CAM table value to write
        :param nWaitTime: return check wait time
        :param stStatus: return AX_CamWriteTable result
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nCamTableID, ECmdType.e_CAMTableEdit)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nIn = MXP_SoftMotion.MXP_WRITECAMTABLE_IN()
            nIn.CamTable = nCamTableID
            for i in range(nTableRowCount):
                nIn.CamDataArray[i].MasterPos = nCamDataArray[i].MasterPos
                nIn.CamDataArray[i].SlavePos = nCamDataArray[i].SlavePos
                nIn.CamDataArray[i].SlaveVel = nCamDataArray[i].SlaveVel
                nIn.CamDataArray[i].SlaveAcc = nCamDataArray[i].SlaveAcc
                nIn.CamDataArray[i].SlaveJerk = nCamDataArray[i].SlaveJerk
                nIn.CamDataArray[i].PointType = nCamDataArray[i].PointType
                nIn.CamDataArray[i].InterpolationType = nCamDataArray[i].InterpolationType

            if nTableRowCount <100:
                nIn.DataSize = 100
            elif nTableRowCount <200:
                nIn.DataSize = 200
            else:
                nIn.DataSize = 400
            nIn.ExecutionMode = 2
            nIn.Execute = False
            nResult = MXP_SoftMotion.MXP_WriteCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = True
            nResult = MXP_SoftMotion.MXP_WriteCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            if nResult !=0:
                ClearIndex(nMotionIndex)
                return nResult
            time.sleep(nWaitTime/1000)

            nOut = MXP_SoftMotion.MXP_WRITECAMTABLE_OUT()
            nResult = MXP_SoftMotion.MXP_GetWriteCamTableOutParam(nMotionIndex, ctypes.byref(nOut))
            if nResult !=0:
                ClearIndex(nMotionIndex)
                return nResult
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored

            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('AX_CamWriteTable', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamReadTableRequest(self, nCamTableID:c_uint16, bExecute: c_bool):
        ''' Read the existing CAM table file

        :param nCamTableID: Set the table number to read
        :param bExecute: Execute the command with rising edge
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nCamTableID, ECmdType.e_CAMTableEdit)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nIn = MXP_SoftMotion.MXP_READCAMTABLE_IN()
            nIn.CamTable = nCamTableID
            nIn.Execute = False
            nResult = MXP_SoftMotion.MXP_ReadCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            if bExecute ==True:
                nIn.Execute = True
                nResult = MXP_SoftMotion.MXP_ReadCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            else:
                ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('AX_CamReadTableRequest', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_CamReadTableReply(self, nCamTableID: c_uint16, stStatus: READ_CAMTABLE_REPLY):
        ''' Return a Status and ErrorID of the CAM table which is executed AX_CamReadTableRequest command

        :param nCamTableID: Set the table number to read
        :param stStatus: Return the CAMReadTable status(Type:READ_CAMTABLE_REPLY)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nCamTableID, ECmdType.e_CAMTableEdit)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nOut = MXP_SoftMotion.MXP_READCAMTABLE_OUT()

            nResult = MXP_SoftMotion.MXP_GetReadCamTableOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.TableRowCount = nOut.DataSize
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored

            for i  in range(nOut.DataSize):
                stStatus.CamDataArray[i] = nOut.CamDataArray[i]
            return nResult

        except Exception as ex:
            print('AX_CamReadTableReply', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamReadTable(self, nCamTableID:c_uint16,nWaitTime:c_int32, stStatus:READ_CAMTABLE_REPLY):
        ''' Read the existing CAM table file

        :param nCamTableID: Set the table number to read
        :param nWaitTime: return check wait time
        :param stStatus: return CoeWrite result
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nCamTableID, ECmdType.e_CAMTableEdit)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK

            nIn = MXP_SoftMotion.MXP_READCAMTABLE_IN()
            nIn.CamTable = nCamTableID
            nIn.Execute = False
            nResult = MXP_SoftMotion.MXP_ReadCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = True
            nResult = MXP_SoftMotion.MXP_ReadCamTableCmd(nMotionIndex, ctypes.byref(nIn))
            if nResult != 0:
                ClearIndex(nMotionIndex)
                return nResult

            time.sleep(nWaitTime/1000)
            nOut = MXP_SoftMotion.MXP_READCAMTABLE_OUT()

            nResult = MXP_SoftMotion.MXP_GetReadCamTableOutParam(nMotionIndex, ctypes.byref(nOut))
            if nResult != 0:
                ClearIndex(nMotionIndex)
                return nResult

            stStatus.TableRowCount = nOut.DataSize
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored

            for i in range(nOut.DataSize):
                stStatus.CamDataArray[i] = nOut.CamDataArray[i]

            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('AX_CamReadTable', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamIn(self, nMasterAxis:c_uint32, nSlaveAxis:c_uint32, fMasterOffset:c_float
                 , fSlaveOffset:c_float, fMasterScaling:c_float, fSlaveScaling:c_float, fMasterSyncPosition:c_float
                 , fMasterStartDistance:c_float, nStartMode:MXP_STARTMODE_ENUM, nMasterValSource:MXP_SOURCE_ENUM,
                 nCamTableID: c_uint16):
        ''' Engage the electronic CAM(CAM table must have been set by AX_CamTableSelect)

        :param nMasterAxis: Master Axis number(0 ~ 127)
        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param fMasterOffset: Set the offset for the table master position
        :param fSlaveOffset: Set the offset for the table slave position
        :param fMasterScaling: Set the scaling factor for the table master position
        :param fSlaveScaling: Set the scaling factor for the table slave position
        :param fMasterSyncPosition: Set the position where synchronization of the slave axis is completed
        :param fMasterStartDistance: Set the master distance for the slave to start synchronizing with the master
        :param nStartMode: Set the talbe position date type to start synchronizition
        :param nMasterValSource: Select the source data of the master axis for synchronization
        :param nCamTableID: Select the CAM table ID for synchronization
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_CAMIn)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn = MXP_SoftMotion.MXP_CAMIN_IN()
            nIn.Master = nMasterAxis
            nIn.Slave = nSlaveAxis
            nIn.MasterOffset = fMasterOffset
            nIn.SlaveOffset = fSlaveOffset
            nIn.MasterScaling = fMasterScaling
            nIn.SlaveScaling = fSlaveScaling
            nIn.MasterSyncPosition = fMasterSyncPosition
            nIn.MasterStartDistance = fMasterStartDistance
            nIn.StartMode = nStartMode
            nIn.MasterValueSource = nMasterValSource
            nIn.CamTableID = nCamTableID
            nIn.BufferMode =MXP_BUFFERMODE_ENUM.MXP_ABORTING
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_CamInCmd(nMotionIndex, ctypes.byref(nIn))

            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_CamInCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_CamIn', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamIn_MasterIO(self, nExternalENC_SlaveNo:c_uint32,nExternalENC_SlavePos:c_uint32,nExternalENC_SlaveSize:c_byte,
                          nExternalENC_Resolution:c_uint32,fExternalENC_PulseToCamMasterUnit:c_float,
                          nSlaveAxis:c_uint32, fMasterOffset:c_float, fSlaveOffset:c_float, fMasterScaling:c_float,
                          fSlaveScaling:c_float, fMasterSyncPosition:c_float, fMasterStartDistance:c_float,
                          nStartMode:MXP_STARTMODE_ENUM, nMasterValSource:MXP_SOURCE_ENUM, nCamTableID: c_uint16):
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_CAMIn)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn = MXP_SoftMotion.MXP_CAMIN_EX_IN()
            nIn.MasterType = MXP_CAM_MASTER_TYPE.MXP_CAM_MASTER_TYPE_EXTENAL_ENC
            nIn.ExternalENCInfo.ExternalEncResolution = nExternalENC_Resolution
            nIn.ExternalENCInfo.PulseToCAMMasterUnit = fExternalENC_PulseToCamMasterUnit
            nIn.ExternalENCInfo.SlaveNo = nExternalENC_SlaveNo
            nIn.ExternalENCInfo.SlavePos = nExternalENC_SlavePos
            nIn.ExternalENCInfo.SlaveSize = c_byte(nExternalENC_SlaveSize)

            nIn.Master = 0
            nIn.Slave = nSlaveAxis
            nIn.MasterOffset = fMasterOffset
            nIn.SlaveOffset = fSlaveOffset
            nIn.MasterScaling = fMasterScaling
            nIn.SlaveScaling = fSlaveScaling
            nIn.MasterSyncPosition = fMasterSyncPosition
            nIn.MasterStartDistance = fMasterStartDistance
            nIn.StartMode = nStartMode
            nIn.MasterValueSource = nMasterValSource
            nIn.CamTableID = nCamTableID
            nIn.BufferMode =MXP_BUFFERMODE_ENUM.MXP_ABORTING
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_CamInCmd_Ex(nMotionIndex, ctypes.byref(nIn))

            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_CamInCmd_Ex(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_CamIn_MasterIO', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamInMonitor(self, nSlaveAxis: c_uint32, stStatus: PROCESS_CHECK):
        ''' Return a Status and ErrorID of the CAM table which is executed AX_CamIn command

        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param stStatus: Return the Status to check Cam In(Type:PROCESS_CHECK)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveAxis, ECmdType.e_CAMIn)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nOut = MXP_SoftMotion.MXP_CAMIN_OUT()

            nResult = MXP_SoftMotion.MXP_GetCamInOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.InSync
            stStatus.ErrorOn = nOut.Errored

            return nResult
        except Exception as ex:
            print('AX_CamInMonitor', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_CamOut(self, nSlaveAxis:c_uint32):
        ''' Disengage a slave axis from the master axis

        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nSlaveAxis, ECmdType.e_CAMIn)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR
            nIn = MXP_SoftMotion.MXP_CAMOUT_IN()
            nIn.Slave = nSlaveAxis
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_CamOutCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_CamOutCmd(nMotionIndex, ctypes.byref(nIn))
            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('AX_CamOut', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamScaling(self, nMasterAxis:c_uint32,nSlaveAxis:c_uint32, nActivationMode:MXP_ACTIVATIONMODE,
                      fActivationPos:c_float,fMasterScaling:c_float,fSlaveScaling:c_float):
        ''' A CAM plate coupling can be scaled with AX_CamScaling

        :param nMasterAxis: Master Axis number(0 ~ 127)
        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param nActivationMode: Specify the scaling time and position
        :param fActivationPos: Master position at which a cam plate is scaled, dapending on the ActivationMode
        :param fMasterScaling: Scaling of the master position of the cam plate
        :param fSlaveScaling: Scaling of the slave position of the cam plate
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_CAMTableOption)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn = MXP_SoftMotion.MXP_CAMSCALING_IN()
            nIn.Master = nMasterAxis
            nIn.Slave = nSlaveAxis
            nIn.ActivationMode = nActivationMode
            nIn.ActivationPosition = fActivationPos
            nIn.MasterScaling = fMasterScaling
            nIn.SlaveScaling = fSlaveScaling

            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_CamScalingCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_CamScalingCmd(nMotionIndex, ctypes.byref(nIn))
            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('AX_CamScaling', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_Phasing(self, nMasterAxis:c_uint32,nSlaveAxis:c_uint32,fPhaseShift:c_float):
        ''' Achieve an offset of the slave axis with respect to the master axis

        :param nMasterAxis: Master Axis number(0 ~ 127)
        :param nSlaveAxis: Slave Axis number(0 ~ 127)
        :param fPhaseShift: The calculated phase shift is transferred to the slave axis as the master axis position
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nSlaveAxis, ECmdType.e_CAMTableOption)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn = MXP_SoftMotion.MXP_PHASING_IN()
            nIn.Master = nMasterAxis
            nIn.Slave = nSlaveAxis
            nIn.PhaseShift = fPhaseShift
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_PhasingCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_PhasingCmd(nMotionIndex, ctypes.byref(nIn))
            ClearIndex(nMotionIndex)
            return nResult
        except Exception as ex:
            print('AX_Phasing', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_CamReadSlavePositionRequest(self, nCamTableID:c_uint16,bExecute:c_bool,fMasterPos:c_float):
        ''' Determine the slave position at a certain point of a cam plate table

        :param nCamTableID: CAM table ID to request(0~63)
        :param bExecute: Execute the command with rising edge
        :param fMasterPos: Master position within the table for which the slave position is to be determined
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nCamTableID, ECmdType.e_ReadCAMSlavePos)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn =  MXP_SoftMotion.MXP_RDCAMTABLESLAVEPOS_IN()
            nIn.CamTable = nCamTableID
            nIn.MasterPosition = fMasterPos
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_RdCamTableSlavePosCmd(nMotionIndex, ctypes.byref(nIn))

            if bExecute:
                nIn.Execute = 1
                nResult = MXP_SoftMotion.MXP_RdCamTableSlavePosCmd(nMotionIndex, ctypes.byref(nIn))
            else:
                ClearIndex(nMotionIndex)
            return nResult

        except Exception as ex:
            print('AX_CamReadSlavePositionRequest', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def AX_CamReadSlavePositionReply(self, nCamTableID: c_uint16, stStatus: READ_CAMSLAVEPOSITION_REPLY):
        ''' Return the slave position at a certain point of a cam plate table

        :param nCamTableID: CAM table ID to reply(0~63)
        :param stStatus: Return the Cam slave position(Type:READ_CAMSLAVEPOSITION_REPLY)
        :return: he result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndexCheck(nCamTableID, ECmdType.e_ReadCAMSlavePos)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_NO_ERROR

            nOut = MXP_SoftMotion.MXP_RDCAMTABLESLAVEPOS_OUT()

            nResult = MXP_SoftMotion.MXP_GetRdCamTableSlavePosOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored
            stStatus.SlavePos = nOut.SlavePosition

            return nResult
        except Exception as ex:
            print('AX_CamReadSlavePositionReply', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    def AX_CamReadSlavePosition(self, nCamTableID:c_uint16,fMasterPos:c_float,
                                nWaitTime: c_int32, stStatus:READ_CAMSLAVEPOSITION_REPLY):
        ''' Determine the slave position at a certain point of a cam plate table

        :param nCamTableID: CAM table ID to request(0~63)
        :param bExecute: Execute the command with rising edge
        :param fMasterPos: Master position within the table for which the slave position is to be determined
        :param nWaitTime: return check wait time
        :param stStatus: return AX_CamReadSlavePosition result
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nCamTableID, ECmdType.e_ReadCAMSlavePos)
            if nMotionIndex == 0:
                return MXP_FUNCTION_STATUS.RET_ERROR_FAIL_INDEX_CHECK
            nIn =  MXP_SoftMotion.MXP_RDCAMTABLESLAVEPOS_IN()
            nIn.CamTable = nCamTableID
            nIn.MasterPosition = fMasterPos
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_RdCamTableSlavePosCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_RdCamTableSlavePosCmd(nMotionIndex, ctypes.byref(nIn))

            if nResult !=0:
                ClearIndex(nMotionIndex)
                return nResult
            time.sleep(nWaitTime/1000)

            nOut = MXP_SoftMotion.MXP_RDCAMTABLESLAVEPOS_OUT()

            nResult = MXP_SoftMotion.MXP_GetRdCamTableSlavePosOutParam(nMotionIndex, ctypes.byref(nOut))
            if nResult !=0:
                ClearIndex(nMotionIndex)
                return nResult

            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored
            stStatus.SlavePos = nOut.SlavePosition


            ClearIndex(nMotionIndex)
            return nResult

        except Exception as ex:
            print('AX_CamReadSlavePosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    #endregion


    #region ProfileMove


    def AX_GetProfileTable(self, nUerTable , nUserTableCount: c_uint32,
                  stMotionTable):
        ''' When driving the Recipe, convert the transfer table(Step,Position,Velocity) according to the Step to the table for the MXP and return it

        :param nUerTable: Sets the UserTable. It starts from 0
        :param nUserTableCount: Set the total driving step of the user table
        :param stMotionTable: Return the profile table value
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nReadData = MXP_SoftMotion.MXP_PROFILE_TABLE_ARRAY_IN()
            nMotionTableCount = c_uint32()
            nResult = MXP_SoftMotion.MXP_GetProfileTable_Ex( ctypes.byref(nUerTable) , nUserTableCount,  byref(nMotionTableCount)
                                                         , ctypes.byref(stMotionTable) )
            return nResult
        except Exception as ex:
            print('Ax_GetProfileTable', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_ProfileMove(self, nAxisNo:c_uint32 , nMotionTableCount: c_uint32,nIOTableCount: c_uint32,nRepeatCount: c_uint16,
                       fStartDwell: c_float,fEndDwell:c_float,nReverseMode:c_uint16,stMotionTable,stIoTable):
        ''' It is a function that makes profile movement

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127)
        :param nMotionTableCount: Set the profile table count
        :param nIOTableCount: Set the IO table count
        :param nRepeatCount: Set the repeat count for how many iterations motion
        :param fStartDwell: Set the Waiting time before driving (msec)
        :param fEndDwell: When setting the RepeatCount, Set the waiting time before return operation (msec)
        :param nReverseMode: Set the reverse mode(1 : reverse mode)
        :param stMotionTable: return the profile table value
        :param stIoTable: return the IO table value
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_PROFILEMOVE_INDEX
            stMotionTable.DataSize = nMotionTableCount

            stIoTable.DataSize = nIOTableCount

            nProfileIn.Axis = nAxisNo
            nProfileIn.EndDwell = fEndDwell
            nProfileIn.IOTablesize = nIOTableCount
            nProfileIn.RepeatCount = nRepeatCount
            nProfileIn.ReverseMode = nReverseMode
            nProfileIn.StartDwell = fStartDwell
            nProfileIn.Tablesize = nMotionTableCount
            nProfileIn.Execute = 0

            nResult = MXP_SoftMotion.MXP_ProfileMoveCmd_Ex(nMotionIndex, ctypes.byref(nProfileIn),
                                                           ctypes.byref(stMotionTable), ctypes.byref(stIoTable))
            nProfileIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_ProfileMoveCmd_Ex(nMotionIndex, ctypes.byref(nProfileIn),
                                                           ctypes.byref(stMotionTable), ctypes.byref(stIoTable))


            return nResult
        except Exception as ex:
            print('AX_ProfileMove', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_ProfileMoveCheck(self, nAxisNo:c_uint32 , stStatus: PROCESS_CHECK):
        ''' It checks the operating status of the profile movement

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127)
        :param stStatus: Return the Profile move out value(Type:PROCESS_CHECK)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_PROFILEMOVE_INDEX
            nOut = MXP_SoftMotion.MXP_PROFILE_MOVE_OUT()
            nResult = MXP_SoftMotion.MXP_ProfileMoveOutParam_Ex(nMotionIndex, ctypes.byref(nProfileIn), ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.Errored

            return nResult
        except Exception as ex:
            print('AX_ProfileMoveCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    #endregion
    # region TouchProbe

    def AX_TouchProbe1Set(self, nAxisNo:c_uint32 , nMode: MXP_TRIGGER_MODE , nTriggerType:MXP_TRIGGER_TYPE
                         ,nTriggerEdge:MXP_TRIGGER_EDGE):
        ''' Configure the touch probe function of the servo drive.
         The touch probe function reads the position value of the servo drive when the specified sensor sends an input signal

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :param nMode: >Select a trigger mode(Use MXP_TRIGEER_MODE)
        :param nTriggerType: Select a trigger type(Use MXP_TRIGGER_TYPE)
        :param nTriggerEdge: Select a trigger edge(Use MXP_TRIGGER_EDGE)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nAxisNo, ECmdType.e_TouchprobeSet)
            nIn = MXP_SoftMotion.MXP_SETTOUCHPROBEFUNC_IN()

            nFuncArray = bytearray(2)
            nChageData = int2bytes(mTouchprobeFunc[nAxisNo])

            if len(nChageData) != 0:
                nFuncArray[0:len(nChageData) - 1] = nChageData

            if nMode == MXP_TRIGGER_MODE.e_Single:
                nFuncArray[0] = 0 + pow(2,1) * nMode +  pow(2,2) * nTriggerType

                nDataArray = bytearray(2)
                nDataArray[0] = nFuncArray[0]
                nDataArray[1] = nFuncArray[1]
                mTouchprobeFunc[0] = int.from_bytes(nDataArray, 'little', signed=False)

                nIn.Axis  = nAxisNo
                nIn.FuncData = mTouchprobeFunc[nAxisNo]
                nIn.Enable = 1
                nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))

                nIn.Enable = 0
                nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
                ClearIndex(nMotionIndex)

            nFuncArray[0] = 1 + pow(2, 1) * nMode + pow(2, 2) * nTriggerType

            if nTriggerEdge == MXP_TRIGGER_EDGE.e_Falling:
                nFuncArray[0] = nFuncArray[0]
            else:
                nFuncArray[0] = nFuncArray[0] + pow(2, 4) * 1

            if nTriggerEdge == MXP_TRIGGER_EDGE.e_Rising:
                nFuncArray[0] = nFuncArray[0]
            else:
                nFuncArray[0] = nFuncArray[0] + pow(2, 5) * 1


            nDataArray = bytearray(2)
            nDataArray[0] = nFuncArray[0]
            nDataArray[1] = nFuncArray[1]
            mTouchprobeFunc[nAxisNo] = int.from_bytes(nDataArray, 'little', signed=False)


            nIn.Axis = nAxisNo
            nIn.FuncData = mTouchprobeFunc[nAxisNo]
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Enable = 0
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('MC_TouchProbe1Set', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_TouchProbe1SingleModeReSet(self, nAxisNo:c_uint32):
        ''' Reset the touchprobe1

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nAxisNo, ECmdType.e_TouchprobeSet)
            nIn = MXP_SoftMotion.MXP_SETTOUCHPROBEFUNC_IN()

            nFuncArray = bytearray(2)
            nChageData = int2bytes(mTouchprobeFunc[nAxisNo])

            if len(nChageData) != 0:
                nFuncArray[0:len(nChageData) - 1] = nChageData

            nDataArray = bytearray(2)
            nDataArray[0] = 0
            nDataArray[1] = nFuncArray[1]
            mTouchprobeFunc[nAxisNo] = int.from_bytes(nDataArray, 'little', signed=False)

            nIn.Axis = nAxisNo
            nIn.FuncData = mTouchprobeFunc[nAxisNo]
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Enable = 0
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('MC_TouchProbe1SingleModeReSet', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_TouchProbe2Set(self, nAxisNo:c_uint32 , nMode: MXP_TRIGGER_MODE , nTriggerType:MXP_TRIGGER_TYPE
                         ,nTriggerEdge:MXP_TRIGGER_EDGE):
        ''' Configure the touch probe function of the servo drive.
         The touch probe function reads the position value of the servo drive when the specified sensor sends an input signal

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :param nMode: >Select a trigger mode(Use MXP_TRIGEER_MODE)
        :param nTriggerType: Select a trigger type(Use MXP_TRIGGER_TYPE)
        :param nTriggerEdge: Select a trigger edge(Use MXP_TRIGGER_EDGE)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nAxisNo, ECmdType.e_TouchprobeSet)
            nIn = MXP_SoftMotion.MXP_SETTOUCHPROBEFUNC_IN()

            nFuncArray = bytearray(2)
            nChageData = int2bytes(mTouchprobeFunc[nAxisNo])
            if len(nChageData) != 0:
                nFuncArray[0:len(nChageData) - 1] = nChageData


            if nMode == MXP_TRIGGER_MODE.e_Single:
                nFuncArray[1] = 0 + pow(2,1) * nMode +  pow(2,2) * nTriggerType

                nDataArray = bytearray(2)
                nDataArray[0] = nFuncArray[0]
                nDataArray[1] = nFuncArray[1]
                mTouchprobeFunc[0] = int.from_bytes(nDataArray, 'little', signed=False)

                nIn.Axis  = nAxisNo
                nIn.FuncData = mTouchprobeFunc[nAxisNo]
                nIn.Axis = nAxisNo
                nIn.FuncData = mTouchprobeFunc[nAxisNo]

                nIn.Enable = 1
                nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))

                nIn.Enable = 0
                nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
                ClearIndex(nMotionIndex)

            nFuncArray[1] = 1 + pow(2, 1) * nMode + pow(2, 2) * nTriggerType

            if nTriggerEdge == MXP_TRIGGER_EDGE.e_Falling:
                nFuncArray[1] = nFuncArray[1]
            else:
                nFuncArray[1] = nFuncArray[1] + pow(2, 4) * 1

            if nTriggerEdge == MXP_TRIGGER_EDGE.e_Rising:
                nFuncArray[1] = nFuncArray[1]
            else:
                nFuncArray[1] = nFuncArray[1] + pow(2, 5) * 1

            nDataArray = bytearray(2)
            nDataArray[0] = nFuncArray[0]
            nDataArray[1] = nFuncArray[1]
            mTouchprobeFunc[0] = int.from_bytes(nDataArray, 'little', signed=False)

            nIn.Axis = nAxisNo
            nIn.FuncData = mTouchprobeFunc[nAxisNo]
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))

            nIn.Enable = 0
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref( nIn))
            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('MC_TouchProbe2Set', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_TouchProbe2SingleModeReSet(self, nAxisNo:c_uint32 ):
        ''' Reset the touchprobe2

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = GetMotionIndex(nAxisNo, ECmdType.e_TouchprobeSet)
            nIn = MXP_SoftMotion.MXP_SETTOUCHPROBEFUNC_IN()

            nFuncArray = bytearray(2)
            nChageData = int2bytes(mTouchprobeFunc[nAxisNo])

            if len(nChageData) != 0:
                nFuncArray[0:len(nChageData) - 1] = nChageData

            nDataArray = bytearray(2)
            nDataArray[0] = nFuncArray[0]
            nDataArray[1] = 0
            mTouchprobeFunc[nAxisNo] = int.from_bytes(nDataArray, 'little', signed=False)

            nIn.Axis = nAxisNo
            nIn.FuncData = mTouchprobeFunc[nAxisNo]
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Enable = 0
            nResult = MXP_SoftMotion.MXP_SetTouchProbeFunctionCmd(nMotionIndex, ctypes.byref(nIn))
            ClearIndex(nMotionIndex)

            return nResult
        except Exception as ex:
            print('MC_TouchProbe2SingleModeReSet', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_TouchProbe1ReadState(self, nAxisNo:c_uint32 , stState: strTouchprobeState):
        ''' Read the current status of the touch probe

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :param stState: Returns the state of the touch probe(Type : strTouchprobeState)
        :return: The result of calling of the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALTOUCHPROBESTATUS_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALTOUCHPROBESTATUS_OUT()
            nIn.Axis  = nAxisNo
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadActualTouchProbeStatus(ctypes.byref(nIn) , ctypes.byref(nOut))

            nFuncArray = bytearray(2)
            nChageData = int2bytes(nOut.Status)

            if len(nChageData) != 0:
                nFuncArray[0:len(nChageData) - 1] = nChageData
            nbitArray = int2Bites(nFuncArray[0])
          #  print(nbitArray)
            stState.TouchprobeUsing = nbitArray[0]
            stState.TouchprobeRisingEdgeSave = nbitArray[1]
            stState.TouchprobeFallingEdgeSave = nbitArray[2]
            stState.TouchprobeRisingPositionUpdate = nbitArray[6]
            stState.TouchprobeFallingPositionUpdate = nbitArray[7]

            return nResult
        except Exception as ex:
            print('MC_TouchProbe1ReadState', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_TouchProbe2ReadState(self, nAxisNo:c_uint32 , stState: strTouchprobeState):
        ''' Read the current status of the touch probe

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :param stState: Returns the state of the touch probe(Type : strTouchprobeState)
        :return: The result of calling of the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALTOUCHPROBESTATUS_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALTOUCHPROBESTATUS_OUT()
            nIn.Axis  = nAxisNo
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadActualTouchProbeStatus(ctypes.byref(nIn) , ctypes.byref(nOut))

            nFuncArray = bytearray(2)
            nChageData = int2bytes(nOut.Status)

            if len(nChageData) != 0:
                nFuncArray[0:len(nChageData) - 1] = nChageData

            nbitArray = int2Bites(nFuncArray[1])

            stState.TouchprobeUsing = nbitArray[0]
            stState.TouchprobeRisingEdgeSave = nbitArray[1]
            stState.TouchprobeFallingEdgeSave = nbitArray[2]
            stState.TouchprobeRisingPositionUpdate = nbitArray[6]
            stState.TouchprobeFallingPositionUpdate = nbitArray[7]

            return nResult
        except Exception as ex:
            print('MC_TouchProbe2ReadState', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_TouchProbe1ReadPosition(self, nAxisNo: c_uint32, nTriggerEdge : MXP_TRIGGER_EDGE,
                             stPosition:TouchProbeReadPos_Reply):
        '''  Read the actual position obtained by the touch probe of the servo drive

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :param nTriggerEdge: Select an edge (Use MXP_TOUCHPROBE_EDGE_ENUM)
        :param stPosition: Return the actual position of the touch probe(Use TouchProbeReadPos_Reply)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALTOUCHPROBEPOSITION_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALTOUCHPROBEPOSITION_EX_OUT()

            nIn.Axis = nAxisNo
            nIn.Channel = MXP_SoftMotion.MXP_TOUCHPROBE_CHNL_ENUM.MXP_TOUCH_CH1

            nIn.Edge = nTriggerEdge
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadActualTouchProbePosition_Ex(ctypes.byref(nIn), ctypes.byref(nOut))
            stPosition.EdgePositivePosition = nOut.EdgePositivePosition
            stPosition.EdgeNegativePosition  = nOut.EdgeNegativePosition


            return nResult
        except Exception as ex:
            print('AX_TouchProbe1ReadPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_TouchProbe2ReadPosition(self, nAxisNo: c_uint32, nTriggerEdge : MXP_TRIGGER_EDGE,
                             stPosition:TouchProbeReadPos_Reply):
        '''  Read the actual position obtained by the touch probe of the servo drive

        :param nAxisNo: Set the axis on which to use the touch probe(0~127)
        :param nTriggerEdge: Select an edge (Use MXP_TOUCHPROBE_EDGE_ENUM)
        :param stPosition: Return the actual position of the touch probe(Use TouchProbeReadPos_Reply)
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_READACTUALTOUCHPROBEPOSITION_IN()
            nOut = MXP_SoftMotion.MXP_READACTUALTOUCHPROBEPOSITION_EX_OUT()

            nIn.Axis = nAxisNo
            nIn.Channel = MXP_SoftMotion.MXP_TOUCHPROBE_CHNL_ENUM.MXP_TOUCH_CH2

            nIn.Edge = nTriggerEdge
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_ReadActualTouchProbePosition_Ex(ctypes.byref(nIn), ctypes.byref(nOut))
            stPosition.EdgePositivePosition = nOut.EdgePositivePosition
            stPosition.EdgeNegativePosition = nOut.EdgeNegativePosition


            return nResult
        except Exception as ex:
            print('AX_TouchProbe2ReadPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR



    ...
    # endregion
    # region UnitChange
    def AX_AccDecToAccTime(self, nAxisNo:c_uint32 , fTargetVel: c_float , fAccDec: c_float
                           , fJerk: c_float, stData: AccDecToAccTime_Reply):
        ''' Return to Change MXP Unit to Time value

        :param nAxisNo: Set the number of the axis(0~127)
        :param fTargetVel: Set the Velocity value
        :param fAccDec: Set the Acc/Dec value
        :param fJerk: Set the Jerk value
        :param stData: Return the Time Value after calcurating
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_ACCDECTOACCTIME_IN()
            nOut = MXP_SoftMotion.MXP_ACCDECTOACCTIME_OUT()
            nIn.Axis = nAxisNo
            nIn.TargetVel = fTargetVel
            nIn.AccDec = fAccDec
            nIn.Jerk = fJerk
            nIn.Enable = 1

            nResult = MXP_SoftMotion.MXP_AccDecToAccTime(ctypes.byref(nIn), ctypes.byref(nOut))
            stData.AccDecBuildUp = nOut.AccDecBuildUp
            stData.LimitAccDec = nOut.LimitAccDec
            stData.AccDecRampDown = nOut.AccDecRampDown

            return nResult
        except Exception as ex:
            print('MC_AccDecToAccTime', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_AccTimeToAccDec(self, nAxisNo:c_uint32 , fTargetVel: c_float , fAccDecBuildUp: c_float
                           , fLimitAccDec: c_float,fAccDecRampDown:c_float, stData: AccTimeToAccDec_Reply):
        ''' Return to Change Time value to MXP Unit

        :param nAxisNo: Set the number of the axis(0~127)
        :param fTargetVel: Set the Velocity value
        :param fAccDecBuildUp: Set the AccDecBuildUp value
        :param fLimitAccDec: Set the LimitAccDec value
        :param fAccDecRampDown: Set the AccDecRampDown value
        :param stData: Return the MXP Unit Value after calcurating
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nIn = MXP_SoftMotion.MXP_ACCTIMETOACCDEC_IN()
            nOut = MXP_SoftMotion.MXP_ACCTIMETOACCDEC_OUT()
            nIn.Axis = nAxisNo
            nIn.TargetVel = fTargetVel
            nIn.AccDecBuildUp = fAccDecBuildUp
            nIn.LimitAccDec = fLimitAccDec
            nIn.AccDecRampDown = fAccDecRampDown
            nIn.Enable = 1
            nResult = MXP_SoftMotion.MXP_AccTimeToAccDec(ctypes.byref(nIn), ctypes.byref(nOut))
            stData.Accdec = nOut.AccDec
            stData.Jerk = nOut.Jerk

            return nResult
        except Exception as ex:
            print('MC_AccTimeToAccDec', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    # endregion


    # region DirectCmd


    def AX_MoveDirectTorque(self, nAxisNo:c_uint32 , fTorque: c_float ):
        ''' Move the axis at the torque specified in the torque parameter

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127)
        :param fTorque: Set the torque to be commanded
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_DIRECTTORQUECONTROL_IN()

            nIn.Axis = nAxisNo
            nIn.Torque = fTorque
            nIn.Enable = 1

            nResult = MXP_SoftMotion.MXP_DirectTorqueControlCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_MoveDirectTorque', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MoveDirectVelocity(self, nAxisNo:c_uint32, fVelocity: c_float ):
        ''' Move the axis at the velocity specified in the Velocity parameter

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127)
        :param fVelocity: Set the movement velocity
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVEDIRECTVELOCITY_IN()
            nIn.Axis = nAxisNo
            nIn.Velocity = fVelocity
            nIn.Enable = 1
            print(nIn.Velocity)
            nResult = MXP_SoftMotion.MXP_MoveDirectVelocityCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_MoveDirectVelocity', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MoveDirectPosition(self, nAxisNo:c_uint32 , fPosition: c_float ):
        ''' Move the axis at the position specified in the position parameter

        :param nAxisNo: Set the number of the axis to which the motion command is issued(0~127)
        :param fPosition: Set the target position
        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nMotionIndex = MC_SINGLEAXIS_INDEX + nAxisNo
            nIn = MXP_SoftMotion.MXP_MOVEDIRECTPOSITION_IN()

            nIn.Axis = nAxisNo
            nIn.Position = fPosition
            nIn.Enable = 1

            nResult = MXP_SoftMotion.MXP_MoveDirectPositionCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_MoveDirectPosition', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    ...
    # endregion
    # region CCC
    def AX_MultiAxisCCCSet(self, nAxisCount:c_uint16 , arrAxis,nMode:c_uint16 ):
        ''' Move the axis at the position specified in the position parameter


        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisNo = arrAxis[0]
            nMotionIndex = GetMotionIndex(nAxisNo,ECmdType.e_CCCSet)
            nIn = MXP_SoftMotion.MXP_MULTIAXISCOUPLESET_IN()


            for i in range(arrAxis[0]):
                nIn.ArrayAxisNo[i] = arrAxis[i]

            nIn.AxisCount = nAxisCount
            nIn.Mode = nMode
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MultiAxisCCCSetCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MultiAxisCCCSetCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_MultiAxisCCCSet', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MultiAxisCCCSetCheck(self, nAxisCount:c_uint16 , arrAxis, stStatus:PROCESS_CHECK):
        ''' Move the axis at the position specified in the position parameter


        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisNo = arrAxis[0]
            nMotionIndex = GetMotionIndex(nAxisNo,ECmdType.e_CCCSet)
            nOut = MXP_SoftMotion.MXP_MULTIAXISCOUPLESET_OUT()
            nResult = MXP_SoftMotion.MXP_GetMultiAxisCCCSetOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.bError

            return nResult
        except Exception as ex:
            print('AX_MultiAxisCCCSetCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_MultiAxisCCCReset(self, nAxisCount:c_uint16 , arrAxis):
        ''' Move the axis at the position specified in the position parameter
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisNo = arrAxis[0]
            nMotionIndex = GetMotionIndex(nAxisNo,ECmdType.e_CCCReset)
            nIn = MXP_SoftMotion.MXP_MULTIAXISCOUPLERESET_IN()


            for i in range(arrAxis[0]):
                nIn.ArrayAxisNo[i] = arrAxis[i]

            nIn.AxisCount = nAxisCount
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MultiAxisCCCReSetCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MultiAxisCCCReSetCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('MXP_MultiAxisCCCReSetCmd', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_MultiAxisCCCResetCheck(self, nAxisCount:c_uint16 , arrAxis, stStatus:PROCESS_CHECK):
        ''' Move the axis at the position specified in the position parameter


        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisNo = arrAxis[0]
            nMotionIndex = GetMotionIndex(nAxisNo,ECmdType.e_CCCReset)
            nOut = MXP_SoftMotion.MXP_MULTIAXISCOUPLERESET_OUT()
            nResult = MXP_SoftMotion.MXP_GetMultiAxisCCCReSetOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.bError

            return nResult
        except Exception as ex:
            print('AX_MultiAxisCCCResetCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_MultiAxisCCCGainSet(self, nAxisCount:c_uint16 , arrAxis, arrSingleAxisGain,
                               arrCCCGain,nMultiControlKffGain:c_uint16):
        ''' Move the axis at the position specified in the position parameter
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisNo = arrAxis[0]
            nMotionIndex = GetMotionIndex(nAxisNo,ECmdType.e_CCCGainSet)
            nIn = MXP_SoftMotion.MXP_MULTIAXISCOUPLEGAINSET_IN()

            print('GainSet Start')
            for i in range(nAxisCount):
                nIn.ArrayAxisNo[i] = arrAxis[i]
                nIn.ArraySingleAxisGain[i].P_Gain = arrSingleAxisGain.SingleGain[i].P_Gain
                nIn.ArraySingleAxisGain[i].I_Gain = arrSingleAxisGain.SingleGain[i].I_Gain
                nIn.ArraySingleAxisGain[i].D_Gain = arrSingleAxisGain.SingleGain[i].D_Gain
                nIn.ArraySingleAxisGain[i].FeedForward_A_Gain = arrSingleAxisGain.SingleGain[i].FeedForward_A_Gain
                nIn.ArraySingleAxisGain[i].FeedForward_V_Gain = arrSingleAxisGain.SingleGain[i].FeedForward_V_Gain

                nIn.ArrayCCCGain[i].CCC_Wi = arrCCCGain.CCCGain[i].CCC_Wi
                nIn.ArrayCCCGain[i].CCC_Wp = arrCCCGain.CCCGain[i].CCC_Wp

            print('GainSet Comp')
            nIn.AxisCount = nAxisCount
            nIn.MultiControlKffGain = nMultiControlKffGain
            nIn.Execute = 0
            nResult = MXP_SoftMotion.MXP_MultiAxisCCCGainSetCmd(nMotionIndex, ctypes.byref(nIn))
            nIn.Execute = 1
            nResult = MXP_SoftMotion.MXP_MultiAxisCCCGainSetCmd(nMotionIndex, ctypes.byref(nIn))

            return nResult
        except Exception as ex:
            print('AX_MultiAxisCCCGainSet', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def AX_MultiAxisCCCGainSetCheck(self, nAxisCount:c_uint16 , arrAxis, stStatus:PROCESS_CHECK):
        ''' Move the axis at the position specified in the position parameter


        :return: The result of calling the function is returned
        '''
        try:
            nResult = MXP_FUNCTION_STATUS
            nAxisNo = arrAxis[0]
            nMotionIndex = GetMotionIndex(nAxisNo,ECmdType.e_CCCGainSet)
            nOut = MXP_SoftMotion.MXP_MULTIAXISCOUPLEGAINSET_OUT()
            nResult = MXP_SoftMotion.MXP_GetMultiAxisCCCGainSetOutParam(nMotionIndex, ctypes.byref(nOut))
            stStatus.ErrorID = nOut.ErrorID
            stStatus.Busy = nOut.Busy
            stStatus.Done = nOut.Done
            stStatus.ErrorOn = nOut.bError

            return nResult
        except Exception as ex:
            print('AX_MultiAxisCCCGainSetCheck', ex)
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR
    ...
    # endregion


    # region SequenceMove




    def AX_SequenceMove(self,nAxisNo:c_uint32, nSequenceCount:c_uint16,arrData,nStartStep):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.nMotionIndex =  MC_SINGLEAXIS_INDEX + nAxisNo
            if mAxisSequenceData[nAxisNo].bRunFlag:
                return MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_INVAILDSTATE
            mAxisSequenceData[nAxisNo].bRunFlag = True
            mAxisSequenceData[nAxisNo].nSendCount = 0
            mAxisSequenceData[nAxisNo].nState.Busy = True
            mAxisSequenceData[nAxisNo].nState.Done = False
            mAxisSequenceData[nAxisNo].nState.ErrorOn = False
            mAxisSequenceData[nAxisNo].nState.ErrorID = 0
            mAxisSequenceData[nAxisNo].nCurBlock = 0
            mAxisSequenceData[nAxisNo].DataClear()

            for i in range(nSequenceCount):
                mAxisSequenceData[nAxisNo].DataAdd(arrData[i])

            mAxisSequenceData[nAxisNo].nStartStep = nStartStep

            return nResult
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_SequenceMove(self,nAxesGroup:c_uint32, nSequenceCount:c_uint16,arrData,nStartStep):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.nMotionIndex =  MC_GROUPAXIS_INDEX + nAxesGroup
            if mGroupSequenceData[nAxesGroup].bRunFlag:
                return MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_INVAILDSTATE
            mGroupSequenceData[nAxesGroup].bRunFlag = True
            mGroupSequenceData[nAxesGroup].nSendCount = 0
            mGroupSequenceData[nAxesGroup].nState.Busy = True
            mGroupSequenceData[nAxesGroup].nState.Done = False
            mGroupSequenceData[nAxesGroup].nState.ErrorOn = False
            mGroupSequenceData[nAxesGroup].nState.ErrorID = 0
            mGroupSequenceData[nAxesGroup].nCurBlock = 0
            mGroupSequenceData[nAxesGroup].DataClear()

            for i in range(nSequenceCount):
                mGroupSequenceData[nAxesGroup].DataAdd(arrData[i])

            mGroupSequenceData[nAxesGroup].nStartStep = nStartStep

            return nResult
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_SequenceMove_File(self, strFilePath, nStartStep, strFileReadError):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.nAxisNo =[0]
            self.nData = []
            self.strFileReadError = []

            self.strSplitPath = strFilePath.split('/')
            self.strSplitPath = self.strSplitPath[len(self.strSplitPath )-1].split('.')

            if self.strSplitPath[len(self.strSplitPath)-1] == 'txt':
                if self.TxtReader.AxisSequenceFileLoad(strFilePath, self.nAxisNo,self.nData, self.strFileReadError):
                    strFileReadError = self.strFileReadError[0]
                    if len(self.nData) < nStartStep:
                        return MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_READ_FAIL
                    self.AX_SequenceMove(self.nAxisNo[0],len(self.nData) , self.nData, nStartStep)
                    return MXP_FUNCTION_STATUS.RET_NO_ERROR
                else:
                    return MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_READ_FAIL
            return nResult
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def GRP_SequenceMove_File(self, strFilePath, nStartStep, strFileReadError):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.nGroupNo =[0]
            self.nData = []
            self.strFileReadError = []

            self.strSplitPath = strFilePath.split('/')
            self.strSplitPath = self.strSplitPath[len(self.strSplitPath )-1].split('.')

            if self.strSplitPath[len(self.strSplitPath)-1] == 'txt':

                if self.TxtReader.GroupSequenceFileLoad(strFilePath, self.nGroupNo,self.nData, self.strFileReadError):
                    strFileReadError = self.strFileReadError[0]
                    if len(self.nData) < nStartStep:
                        return MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_READ_FAIL

                    self.GRP_SequenceMove(self.nGroupNo[0],len(self.nData) , self.nData, nStartStep)
                    return MXP_FUNCTION_STATUS.RET_NO_ERROR
                else:
                    return MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_READ_FAIL




            return nResult
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def SYS_GetAxisBufferInfo(self,nAxisNo:c_uint32, nSaveNum,nReadNum,nCurBlock):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.nReadNum = c_uint16()
            self.nSaveNum = c_uint16()
            self.nCurBlock = c_uint16()

            nResult = MXP_SoftMotion.MXP_ReadAxisBufferInfo(nAxisNo,byref(self.nSaveNum), byref(self.nReadNum), byref( self.nCurBlock))
            if nResult != 0:
                return nResult
            nSaveNum[0] = self.nSaveNum
            nReadNum[0] = self.nReadNum
            nCurBlock[0] = self.nCurBlock

            if mAxisSequenceData[nAxisNo].nSendCount == 0:
                nCurBlock[0] = 0
            return nResult
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def SYS_GetGroupBufferInfo(self,nAxesGroup:c_uint32, nSaveNum,nReadNum,nCurBlock):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.nReadNum = c_uint16()
            self.nSaveNum = c_uint16()
            self.nCurBlock  = c_uint16()
            nResult = MXP_SoftMotion.MXP_ReadGroupBufferInfo(nAxesGroup,byref(self.nSaveNum), byref(self.nReadNum), byref( self.nCurBlock))
            if nResult != 0:
                return nResult
            nSaveNum[0] = self.nSaveNum
            nReadNum[0] = self.nReadNum
            nCurBlock[0] = self.nCurBlock

            if mGroupSequenceData[nAxesGroup].nSendCount ==0:
                nCurBlock[0] = 0
            return nResult
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_SequenceMoveSetVaildCheck(self,nAxisNo:c_uint32, nSequenceCount:c_uint16,bFirstStep:c_bool):
        self.nMaxCount  = 100
        self.nVaildCount  = 0
        self.nCountOffset  = 0

        if mAxisSequenceData[nAxisNo].nStartStep!=0:
            self.nCountOffset = mAxisSequenceData[nAxisNo].nStartStep -1
        self.nCmdBufferUsingCount  = (mAxisSequenceData[nAxisNo].nSendCount - self.nCountOffset ) % self.nMaxCount
        if bFirstStep:
            self.nCmdBufferUsingCount = mAxisSequenceData[nAxisNo].nSaveNum
        if self.nCmdBufferUsingCount != mAxisSequenceData[nAxisNo].nSaveNum:
            return False
        if mAxisSequenceData[nAxisNo].nSaveNum == mAxisSequenceData[nAxisNo].nReadNum:
            self.nVaildCount  = 100
        elif mAxisSequenceData[nAxisNo].nSaveNum > mAxisSequenceData[nAxisNo].nReadNum:
            self.nVaildCount = self.nMaxCount - mAxisSequenceData[nAxisNo].nSaveNum + mAxisSequenceData[nAxisNo].nReadNum
        elif mAxisSequenceData[nAxisNo].nSaveNum < mAxisSequenceData[nAxisNo].nReadNum:
            self.nVaildCount =  mAxisSequenceData[nAxisNo].nReadNum - mAxisSequenceData[nAxisNo].nSaveNum
        self.nVaildCount = self.nVaildCount - 5

        if nSequenceCount < self.nVaildCount:
            return True
        else:
            return False


    def GRP_SequenceMoveSetVaildCheck(self,nAxesGroup:c_uint32, nSequenceCount:c_uint16,bFirstStep:c_bool):
        self.nMaxCount  = 100
        self.nVaildCount  = 0
        self.nCountOffset  = 0

        if mGroupSequenceData[nAxesGroup].nStartStep!=0:
            self.nCountOffset = mGroupSequenceData[nAxesGroup].nStartStep -1
        self.nCmdBufferUsingCount  = (mGroupSequenceData[nAxesGroup].nSendCount - self.nCountOffset ) % self.nMaxCount
        if bFirstStep:
            self.nCmdBufferUsingCount = mGroupSequenceData[nAxesGroup].nSaveNum
        if self.nCmdBufferUsingCount != mGroupSequenceData[nAxesGroup].nSaveNum:
            return False
        if mGroupSequenceData[nAxesGroup].nSaveNum == mGroupSequenceData[nAxesGroup].nReadNum:
            self.nVaildCount  = 100
        elif mGroupSequenceData[nAxesGroup].nSaveNum > mGroupSequenceData[nAxesGroup].nReadNum:
            self.nVaildCount = self.nMaxCount - mGroupSequenceData[nAxesGroup].nSaveNum + mGroupSequenceData[nAxesGroup].nReadNum
        elif mGroupSequenceData[nAxesGroup].nSaveNum < mGroupSequenceData[nAxesGroup].nReadNum:
            self.nVaildCount =  mGroupSequenceData[nAxesGroup].nReadNum - mGroupSequenceData[nAxesGroup].nSaveNum
        self.nVaildCount = self.nVaildCount - 5

        if nSequenceCount < self.nVaildCount:
            return True
        else:
            return False



    def AX_SequenceMoveCmdSet(self, nAxisNo:c_uint32 , nStartindex:c_uint16, nEndIndex:c_int16 ):
        try:
            nResult = MXP_FUNCTION_STATUS
            for i in range(nStartindex,nEndIndex):
                self.nBlockIndex  = i+1
                self.nCurCmd = StSequenceMove()
                self.nCurCmd = mAxisSequenceData[nAxisNo].nData[i]
                if self.nCurCmd.nCmdType == ESequenceCmdType.e_AbsMove:
                    nResult = self.AX_MoveAbsolute_Ex(nAxisNo,self.nBlockIndex, self.nCurCmd.fPos, self.nCurCmd.fVel, self.nCurCmd.fAcc
                                                      , self.nCurCmd.fDec, self.nCurCmd.fJerk, self.nCurCmd.nDirection,self.nCurCmd.nBufferMode )
                elif self.nCurCmd.nCmdType == ESequenceCmdType.e_RelativeMove:
                    nResult = self.AX_MoveRelative_Ex(nAxisNo, self.nBlockIndex, self.nCurCmd.fPos, self.nCurCmd.fVel,
                                                      self.nCurCmd.fAcc, self.nCurCmd.fDec, self.nCurCmd.fJerk, self.nCurCmd.nBufferMode)
                elif self.nCurCmd.nCmdType == ESequenceCmdType.e_IO:
                    nResult = self.AX_BufferedIO_Ex(nAxisNo, self.nBlockIndex, self.nCurCmd.nIOSlaveNo,
                                                    self.nCurCmd.nIOBitNo, self.nCurCmd.bIOBitSet)
                elif  self.nCurCmd.nCmdType == ESequenceCmdType.e_Dwell:
                    nResult = self.AX_Dwell_Ex(nAxisNo,  self.nBlockIndex, self.nCurCmd.fDwellTime)

                if nResult !=0:
                    return nResult
                mAxisSequenceData[nAxisNo].nSendCount = self. nBlockIndex
            return 0
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_SequenceMoveCmdSet(self, nAxesGroup:c_uint32 , nStartindex:c_uint16, nEndIndex:c_int16 ):
        try:
            nResult = MXP_FUNCTION_STATUS
            self.stPosition = GROUP_POS()
            for i in range(nStartindex,nEndIndex):
                self.nBlockIndex  = i+1
                self.nCurCmd = StGroupSequenceMove()
                self.nCurCmd = mGroupSequenceData[nAxesGroup].nData[i]
                if self.nCurCmd.nCmdType == ESequenceCmdType.e_AbsMove:
                    self.stPosition.nX = self.nCurCmd.fXPos
                    self.stPosition.nY = self.nCurCmd.fYPos
                    self.stPosition.nZ = self.nCurCmd.fZPos
                    self.stPosition.nU = self.nCurCmd.fUPos
                    self.stPosition.nV = self.nCurCmd.fVPos
                    self.stPosition.nW = self.nCurCmd.fWPos
                    self.stPosition.nA = self.nCurCmd.fAPos
                    self.stPosition.nB = self.nCurCmd.fBPos
                    self.stPosition.nC = self.nCurCmd.fCPos

                    nResult = self.GRP_MoveLinearAbsolute_Ex(nAxesGroup,self.nBlockIndex, self.stPosition, self.nCurCmd.fVel, self.nCurCmd.fAcc
                                                      , self.nCurCmd.fDec, self.nCurCmd.fJerk,self.nCurCmd.nBufferMode )
                elif self.nCurCmd.nCmdType == ESequenceCmdType.e_RelativeMove:
                    self.stPosition.nX = self.nCurCmd.fXPos
                    self.stPosition.nY = self.nCurCmd.fYPos
                    self.stPosition.nZ = self.nCurCmd.fZPos
                    self.stPosition.nU = self.nCurCmd.fUPos
                    self.stPosition.nV = self.nCurCmd.fVPos
                    self.stPosition.nW = self.nCurCmd.fWPos
                    self.stPosition.nA = self.nCurCmd.fAPos
                    self.stPosition.nB = self.nCurCmd.fBPos
                    self.stPosition.nC = self.nCurCmd.fCPos

                    nResult = self.GRP_MoveLinearRelative_Ex(nAxesGroup, self.nBlockIndex, self.stPosition, self.nCurCmd.fVel,
                                                      self.nCurCmd.fAcc, self.nCurCmd.fDec, self.nCurCmd.fJerk, self.nCurCmd.nBufferMode)

                elif self.nCurCmd.nCmdType == ESequenceCmdType.e_IO:
                    nResult = self.GRP_BufferedIO_Ex(nAxesGroup, self.nBlockIndex, self.nCurCmd.nIOSlaveNo,
                                                    self.nCurCmd.nIOBitNo, self.nCurCmd.bIOBitSet)
                elif  self.nCurCmd.nCmdType == ESequenceCmdType.e_Dwell:
                    nResult = self.GRP_Dwell_Ex(nAxesGroup,  self.nBlockIndex, self.nCurCmd.fDwellTime)

                if nResult !=0:
                    return nResult
                mGroupSequenceData[nAxesGroup].nSendCount = self. nBlockIndex
            return 0
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_SequenceBufferStateCheck(self, nAxisNo):
        try:
            self.bAxisReadCheck = [0]
            self.nAxisState = MXP_AxisStateBit()
            self.AX_ReadyCheck(nAxisNo,self.bAxisReadCheck)
            self.AX_ReadStatus(nAxisNo,self.nAxisState)

            if self.nAxisState.Disable or self.nAxisState.ErrorStop or self.nAxisState.PowerOn == False or self.nAxisState.Stopping or mAxisSequenceData[nAxisNo].nState.ErrorOn:
                return MXP_SequenceBufferState.e_Fail
            if (mAxisSequenceData[nAxisNo].nCurBlock == mAxisSequenceData[nAxisNo].nSendCount) and (self.bAxisReadCheck[0] == True):
                return MXP_SequenceBufferState.e_Complete
            if mAxisSequenceData[nAxisNo].nSendCount == 0:
                return MXP_SequenceBufferState.e_Null
            #if mAxisSequenceData[nAxisNo].nCurBlock != mAxisSequenceData[nAxisNo].nSendCount:
                #print(mAxisSequenceData[nAxisNo].nCurBlock,mAxisSequenceData[nAxisNo].nSendCount,self.bAxisReadCheck[0])
            return MXP_SequenceBufferState.e_Runing
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR
    def GRP_SequenceBufferStateCheck(self, nAxesGroup):
        try:
            self.bAxisReadCheck = [0]
            self.nGroupState = MXP_AxisStateBit()
            self.GRP_ReadyCheck(nAxesGroup,self.bAxisReadCheck)
            self.GRP_ReadStatus(nAxesGroup,self.nGroupState)

            if self.nGroupState.Disable or self.nGroupState.ErrorStop or self.nGroupState.Stopping or \
                    mGroupSequenceData[nAxesGroup].nState.ErrorOn:
                return MXP_SequenceBufferState.e_Fail
            if (mGroupSequenceData[nAxesGroup].nCurBlock == mGroupSequenceData[nAxesGroup].nSendCount) and (self.bAxisReadCheck[0] == True):
                return MXP_SequenceBufferState.e_Complete
            if mGroupSequenceData[nAxesGroup].nSendCount == 0:
                return MXP_SequenceBufferState.e_Null
            #if mAxisSequenceData[nAxisNo].nCurBlock != mAxisSequenceData[nAxisNo].nSendCount:
                #print(mAxisSequenceData[nAxisNo].nCurBlock,mAxisSequenceData[nAxisNo].nSendCount,self.bAxisReadCheck[0])
            return MXP_SequenceBufferState.e_Runing
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def AX_SequenceMoveCheck(self, nAxisNo:c_uint32, nCurStep,strCurStepName, nRemainCount,stStatus):
        try:
            nRemainCount[0] = len( mAxisSequenceData[nAxisNo].nData) - mAxisSequenceData[nAxisNo].nCurBlock
            nCurStep[0] = mAxisSequenceData[nAxisNo].nCurBlock

            stStatus[0] = mAxisSequenceData[nAxisNo].nState
            self.nIndex = 0
            if nCurStep[0] == 0:
                self.nIndex = 0
            else:
                self.nIndex = nCurStep[0] -1
            strCurStepName[0] = mAxisSequenceData[nAxisNo].nData[self.nIndex].strStepName
            return 0
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def GRP_SequenceMoveCheck(self, nAxesGroup:c_uint32, nCurStep,strCurStepName, nRemainCount,stStatus):
        try:
            nRemainCount[0] = len( mGroupSequenceData[nAxesGroup].nData) - mGroupSequenceData[nAxesGroup].nCurBlock
            nCurStep[0] = mGroupSequenceData[nAxesGroup].nCurBlock

            stStatus[0] = mGroupSequenceData[nAxesGroup].nState
            self.nIndex = 0
            if nCurStep[0] == 0:
                self.nIndex = 0
            else:
                self.nIndex = nCurStep[0] -1
            strCurStepName[0] = mGroupSequenceData[nAxesGroup].nData[self.nIndex].strStepName

            return 0
        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR


    def SEQ_AxisSequenceMoveManager(self,nAxisNo:c_uint32):
        try:
            self.nSendMaxCount = 30

            if mAxisSequenceData[nAxisNo].bRunFlag and (nTaskPos[nAxisNo] < 800 and nTaskPos[nAxisNo] > 0):

                self.nSaveNum =[0]
                self.nReadNum =[0]
                self.nCurBlock =[0]

                nResult[nAxisNo] = self.SYS_GetAxisBufferInfo( nAxisNo, self.nSaveNum,
                                           self.nReadNum ,self.nCurBlock)
                mAxisSequenceData[nAxisNo].nSaveNum = self.nSaveNum.value
                mAxisSequenceData[nAxisNo].nReadNum = self.nReadNum.value
                mAxisSequenceData[nAxisNo].nCurBlock = self.nCurBlock.value

                #print('case1',mAxisSequenceData[nAxisNo].nSaveNum,mAxisSequenceData[nAxisNo].nReadNum,mAxisSequenceData[nAxisNo].nCurBlock)
                if nResult[nAxisNo] != 0:
                    nTaskPos[nAxisNo] = 800

            if nTaskPos[nAxisNo] >0 and nTaskPos[nAxisNo] <800 \
                    and mAxisSequenceData[nAxisNo].bRunFlag == False:
                nTaskPos[nAxisNo]  = 800


            if  nTaskPos[nAxisNo] == 0:
                bReadyCheck = [0]
                if mAxisSequenceData[nAxisNo].bRunFlag:
                    mAxisSequenceData[nAxisNo].nCurBlock = 0
                    if mAxisSequenceData[nAxisNo].nStartStep !=0:
                        mAxisSequenceData[nAxisNo].nStartStep = mAxisSequenceData[nAxisNo].nStartStep-1
                    else:
                        mAxisSequenceData[nAxisNo].nStartStep = 0
                    nResult[nAxisNo] = self.AX_ReadyCheck(nAxisNo,bReadyCheck)
                    if bReadyCheck[0] == False:
                        nTaskPos[nAxisNo] = 800
                        return
                    self.nSendCmdCount = len(mAxisSequenceData[nAxisNo].nData) - mAxisSequenceData[nAxisNo].nSendCount
                    if self.nSendCmdCount >= self. nSendMaxCount:
                        self.nSendCmdCount = self.nSendMaxCount
                    if self.AX_SequenceMoveSetVaildCheck(nAxisNo,self.nSendCmdCount,True):
                        print('SEQ_AxisSequenceMoveManager cmd Set', nAxisNo , mAxisSequenceData[nAxisNo].nSendCount,mAxisSequenceData[nAxisNo].nSendCount + self.nSendCmdCount)
                        nResult[nAxisNo] = self.AX_SequenceMoveCmdSet(nAxisNo,
                                                        mAxisSequenceData[nAxisNo].nSendCount,mAxisSequenceData[nAxisNo].nSendCount + self.nSendCmdCount)
                        if nResult[nAxisNo] !=0:
                            nTaskPos[nAxisNo] = 800
                            return

                        nTaskPos[nAxisNo] =100
                        return

            if  nTaskPos[nAxisNo] ==100:
                self.nSendCmdCount = len(mAxisSequenceData[nAxisNo].nData) - mAxisSequenceData[nAxisNo].nSendCount
                if self.nSendCmdCount >= self.nSendMaxCount:
                    self.nSendCmdCount = self.nSendMaxCount
                elif self.nSendCmdCount ==0:
                   nTaskPos[nAxisNo] = 200
                   return

                if self.AX_SequenceMoveSetVaildCheck(nAxisNo, self.nSendCmdCount,False):

                    nResult[nAxisNo] = self.AX_SequenceMoveCmdSet(nAxisNo, mAxisSequenceData[nAxisNo].nSendCount,
                                                                  mAxisSequenceData[nAxisNo].nSendCount + self.nSendCmdCount )
                    if nResult[nAxisNo] != 0:
                        nTaskPos[nAxisNo] = 800
                        return

                    nTaskPos[nAxisNo] = 100
                    return

            if nTaskPos[nAxisNo] == 200:
                print('BufferState',self.AX_SequenceBufferStateCheck(nAxisNo))
                if self.AX_SequenceBufferStateCheck(nAxisNo) == MXP_SequenceBufferState.e_Complete:
                    nTaskPos[nAxisNo] = 1000
                elif  self.AX_SequenceBufferStateCheck(nAxisNo) == MXP_SequenceBufferState.e_Fail:
                    nResult[nAxisNo] = MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_PROCESS_FAIL
                    print('SEQ_AxisSequenceMoveManager ErrorCheck6')
                    nTaskPos[nAxisNo] = 800

            if  nTaskPos[nAxisNo] ==800:

                mAxisSequenceData[nAxisNo].bRunFlag = False
                mAxisSequenceData[nAxisNo].nState.Busy = False
                mAxisSequenceData[nAxisNo].nState.Done = False
                mAxisSequenceData[nAxisNo].nState.ErrorOn = True
                if nResult[nAxisNo] !=0:
                    mAxisSequenceData[nAxisNo].nState.ErrorID = nResult[nAxisNo]
                else:
                    mAxisSequenceData[nAxisNo].nState.ErrorID = MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_PROCESS_FAIL

                nTaskPos[nAxisNo] = 0


            if nTaskPos[nAxisNo] == 1000:
                mAxisSequenceData[nAxisNo].bRunFlag = False
                mAxisSequenceData[nAxisNo].nState.Busy = False
                mAxisSequenceData[nAxisNo].nState.Done = True
                mAxisSequenceData[nAxisNo].nState.ErrorOn = False
                mAxisSequenceData[nAxisNo].nState.ErrorID = 0
                nTaskPos[nAxisNo] = 0

        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR




    def SEQ_GroupSequenceMoveManager(self,nAxesGroup:c_uint32):
        try:
            self.nSendMaxCount = 30

            if mGroupSequenceData[nAxesGroup].bRunFlag and (nGroupTaskPos[nAxesGroup] < 800 and nGroupTaskPos[nAxesGroup] > 0):

                self.nSaveNum =[0]
                self.nReadNum =[0]
                self.nCurBlock =[0]

                nGroupResult[nAxesGroup] = self.SYS_GetGroupBufferInfo(nAxesGroup, self.nSaveNum,
                                           self.nReadNum ,self.nCurBlock)
                mGroupSequenceData[nAxesGroup].nSaveNum = self.nSaveNum.value
                mGroupSequenceData[nAxesGroup].nReadNum = self.nReadNum.value
                mGroupSequenceData[nAxesGroup].nCurBlock = self.nCurBlock.value

                #print('case1',mAxisSequenceData[nAxisNo].nSaveNum,mAxisSequenceData[nAxisNo].nReadNum,mAxisSequenceData[nAxisNo].nCurBlock)
                if nGroupResult[nAxesGroup] != 0:
                    nGroupTaskPos[nAxesGroup] = 800

            if nGroupTaskPos[nAxesGroup] >0 and nGroupTaskPos[nAxesGroup] <800 \
                    and mGroupSequenceData[nAxesGroup].bRunFlag == False:
                nGroupTaskPos[nAxesGroup]  = 800


            if  nGroupTaskPos[nAxesGroup] == 0:
                bReadyCheck = [0]
                if mGroupSequenceData[nAxesGroup].bRunFlag:
                    mGroupSequenceData[nAxesGroup].nCurBlock = 0
                    if mGroupSequenceData[nAxesGroup].nStartStep !=0:
                        mGroupSequenceData[nAxesGroup].nStartStep = mGroupSequenceData[nAxesGroup].nStartStep-1
                    else:
                        mGroupSequenceData[nAxesGroup].nStartStep = 0
                    nGroupResult[nAxesGroup] = self.GRP_ReadyCheck(nAxesGroup,bReadyCheck)
                    if bReadyCheck[0] == False:
                        print('SEQ_GroupSequenceMoveManager ErrorCheck3')
                        nGroupTaskPos[nAxesGroup] = 800
                        return
                    self.nSendCmdCount = len(mGroupSequenceData[nAxesGroup].nData) - mGroupSequenceData[nAxesGroup].nSendCount
                    if self.nSendCmdCount >= self. nSendMaxCount:
                        self.nSendCmdCount = self.nSendMaxCount
                    if self.GRP_SequenceMoveSetVaildCheck(nAxesGroup,self.nSendCmdCount,True):
                        nGroupResult[nAxesGroup] = self.GRP_SequenceMoveCmdSet(nAxesGroup,
                                                        mGroupSequenceData[nAxesGroup].nSendCount,mGroupSequenceData[nAxesGroup].nSendCount + self.nSendCmdCount)
                        if nGroupResult[nAxesGroup] !=0:
                            nGroupTaskPos[nAxesGroup] = 800
                            return

                        nGroupTaskPos[nAxesGroup] =100
                        return

            if  nGroupTaskPos[nAxesGroup] ==100:
                self.nSendCmdCount = len(mGroupSequenceData[nAxesGroup].nData) - mGroupSequenceData[nAxesGroup].nSendCount
                if self.nSendCmdCount >= self.nSendMaxCount:
                    self.nSendCmdCount = self.nSendMaxCount
                elif self.nSendCmdCount ==0:
                   nGroupTaskPos[nAxesGroup] = 200
                   return

                if self.GRP_SequenceMoveSetVaildCheck(nAxesGroup, self.nSendCmdCount,False):

                    nGroupResult[nAxesGroup] = self.GRP_SequenceMoveCmdSet(nAxesGroup, mGroupSequenceData[nAxesGroup].nSendCount,
                                                                  mGroupSequenceData[nAxesGroup].nSendCount + self.nSendCmdCount )
                    if nGroupResult[nAxesGroup] != 0:
                        print('SEQ_GroupSequenceMoveManager ErrorCheck5')
                        nGroupTaskPos[nAxesGroup] = 800
                        return

                    nGroupTaskPos[nAxesGroup] = 100
                    return

            if nGroupTaskPos[nAxesGroup] == 200:
                if self.GRP_SequenceBufferStateCheck(nAxesGroup) == MXP_SequenceBufferState.e_Complete:
                    nGroupTaskPos[nAxesGroup] = 1000
                elif  self.GRP_SequenceBufferStateCheck(nAxesGroup) == MXP_SequenceBufferState.e_Fail:
                    nGroupResult[nAxesGroup] = MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_PROCESS_FAIL
                    print('SEQ_GroupSequenceMoveManager ErrorCheck6')
                    nGroupTaskPos[nAxesGroup] = 800

            if  nGroupTaskPos[nAxesGroup] ==800:

                mGroupSequenceData[nAxesGroup].bRunFlag = False
                mGroupSequenceData[nAxesGroup].nState.Busy = False
                mGroupSequenceData[nAxesGroup].nState.Done = False
                mGroupSequenceData[nAxesGroup].nState.ErrorOn = True
                if nGroupResult[nAxesGroup] !=0:
                    mGroupSequenceData[nAxesGroup].nState.ErrorID = nGroupResult[nAxesGroup]
                else:
                    mGroupSequenceData[nAxesGroup].nState.ErrorID = MXP_FUNCTION_STATUS.RET_SEQUENCEMOVE_PROCESS_FAIL

                nGroupTaskPos[nAxesGroup] = 0

            if nGroupTaskPos[nAxesGroup] == 1000:
                mGroupSequenceData[nAxesGroup].bRunFlag = False
                mGroupSequenceData[nAxesGroup].nState.Busy = False
                mGroupSequenceData[nAxesGroup].nState.Done = True
                mGroupSequenceData[nAxesGroup].nState.ErrorOn = False
                mGroupSequenceData[nAxesGroup].nState.ErrorID = 0
                nGroupTaskPos[nAxesGroup] = 0

        except Exception as ex:
            return MXP_FUNCTION_STATUS.RET_ERROR_EXCEPTIONERROR

    def tick(self):
        for i in range(128):
            self.SEQ_AxisSequenceMoveManager(i)
        for i in range(32):
            self.SEQ_GroupSequenceMoveManager(i)

        t = threading.Timer(0.5,self.tick).start()



    # endregion

MXP = MXPEasyClass()
MXP.tick()
#MXP.SEQ_AxisSequenceMoveManager(0)
#Test = MXPEasyClass()
#array =[]
strError = [0]
#AxisNo = [0]
#strFilePath = "D:/Build/Document/4_개발모델/제어기과제/MXP4.0/2_분석설계/API 언어벌 개발/배포경로/Example/MXPEasyClass/SequenceMoveData/SingleAxis/AxisMove.txt"
#strFilePath ='D:\\Build\Document\\4_개발모델\\제어기과제\\MXP4.0\\2_분석설계\\API 언어벌 개발\\배포경로\\Example\\MXPEasyClass\\SequenceMoveData\\SingleAxis\\AxisMove.txt'

#if MXP.AX_SequenceMove_File(strFilePath,0,strError) == 0:
#    print('AX_SequenceMove_File Fail' ,str(strError[0]) )

#else:

#    print('AX_SequenceMove_File Success' ,str(strError[0]) )



#if Test.AxisSequenceFileLoad(strFilePath,AxisNo,array,strError):
#    print( str(strError[0]) + '\t' + str(AxisNo[0])+ '\t' + str( array[0].strStepName) + '\t' + str(array[len(array)-1 ].strStepName) )
#else:

#    print(str(strError[0]) + '\t' + str(AxisNo[0]) + '\t' + str(array[0].strStepName) + '\t' + str(array[len(array) - 1].strStepName))

#Test = DataVaildCheck()

#bBoolArray = []

#for i in  range(EAxisSequenceData.e_End) :
 #   bBoolArray.append(0)

#bBoolArray[EAxisSequenceData.e_AxisGroupNo] = 1

#nIndata  = StSequenceMove()

#Test.FCheckDataVaild(nIndata,bBoolArray)

