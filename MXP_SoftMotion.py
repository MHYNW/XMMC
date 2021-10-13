


from ctypes import *
from enum import IntEnum
import ctypes
import ctypes.wintypes

#region Enum Define


class EC_NETWORK_CMD(IntEnum):
    NET_STATE_INIT_CMD = 0
    NET_STATE_PREOP_CMD = 1
    NET_STATE_BOOT_CMD = 2
    NET_STATE_SAFEOP_CMD = 3
    NET_STATE_OP_CMD = 4


class MXP_INTERPOLATION_ENUM(IntEnum):
    CAM_Profile_Monotone_Cubic = 0   #System is NOT licensed.
    CAM_Profile_Linear = 1    #System is no working.
    CAM_Profile_Polynom3 = 2    #System is killing.
    CAM_Profile_Polynom5 = 3    #System is killed.
    CAM_Profile_ModifiedSine = 4    #System is creating.
    CAM_Profile_Cycloid = 5    #System is created.
    CAM_Profile_Sinusline = 6    #System is initializing.
    CAM_Profile_Polynom7 = 7    #System is initialized.

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
        ("Position", c_float ),
        ("Velocity", c_float),
        ("Acc", c_float),
        ("Dec", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("Buffermode", c_int32)]

class MXP_File_TABLE_IN(Structure):
    _fields_ = [
        ("TableindexNo", c_byte),
        ("Position", c_float ),
        ("Velocity", c_float),
        ("nTime", c_float),
        ("nDiffPosition", c_float),
        ("nDiffVelocity", c_float),
        ("nAcc", c_float)]

class MXP_IO_TABLE_IN(Structure):
    _fields_ = [
        ("TableindexNo", c_byte),
        ("SlaveNo", c_uint16 ),
        ("BitPos" , c_uint16 ),
        ("BitValue", c_byte)]

class MXP_EXECUTIONMODE_ENUM(IntEnum):
    MXP_IMMEDIATELY = 0
    MXP_QUEUD = 1
class MXP_TRANSITIONMODE_ENUM(IntEnum):
    MXP_TM_NONE = 0
    MXP_TM_STARTVELOCITY = 1
    MXP_TM_CONSTANTVELOCITY = 2
    MXP_TM_CORNERDISTANCE = 3
    MXP_TM_MAXCORNERDEVIATION = 4
class MXP_COORDSYSTEM_ENUM(IntEnum):
    MXP_ACS = 1
    MXP_MCS = 2
    MXP_PCS = 3
class MXP_CIRCLEMODE_ENUM(IntEnum):
    MXP_BORDER = 1
    MXP_CENTER = 2
    MXP_RADIUS = 3
class MXP_SYNCMODE_ENUM(IntEnum):
    MXP_SHORTEST = 1
    MXP_CATCHUP = 2
    MXP_SLOWDOWN = 3
class MXP_SWITCHMODE_ENUM(IntEnum):
    MXP_ON = 0
    MXP_OFF = 1
    MXP_EDGE_ON = 2
    MXP_EDGE_OFF = 3
    MXP_EDGE_SWITCH_POSITIVE = 4
    MXP_EDGE_SWITCH_NEGATIVE = 5
class MXP_TOUCHPROBE_CHNL_ENUM(IntEnum):
    MXP_TOUCH_CH1 = 0
    MXP_TOUCH_CH2 = 1
class MXP_CONTROLMODE_ENUM(IntEnum):
    MXP_PP = 0
    MXP_CSP = 1
    MXP_CSV = 2
    MXP_CST = 3
class MXP_PDODIRECTION_ENUM(IntEnum):
    MXP_PDO_Tx = 0 #  'Slave -> MXP : ex)ActualPosition
    MXP_PDO_Rx = 1 # 'MXP -> Slave : ex)TargetPosition

class MXP_AXISPARAMETER_ENUM(IntEnum):
    Param_Index_USE_AXIS = 100
    Param_Index_SYS_POS_UINT = 101
    Param_Index_SYS_FEED_UNIT = 102
    Param_Index_PUINT = 103
    Param_Index_FUINT = 104
    Param_Index_ACCELTIME = 105
    Param_Index_DECELTIME = 106
    Param_Index_SCURVE_RATIO = 107
    Param_Index_GEAR_RATIO_MOTOR = 108
    Param_Index_GEAR_RATIO_MECHA = 109
    Param_Index_MECHA_DISTANCE = 110
    Param_Index_ENC_RESOLUTION =111
    Param_Index_SERVO_MODE = 112
    Param_Index_AXIS_SPINDLE_SET = 113
    Param_Index_AXIS_ModuloMax = 114

    Param_Index_MAX_FEED_RPD = 200
    Param_Index_MAX_M_FEED = 201
    Param_Index_USE_SL = 202
    Param_Index_SOFTLIMITM = 203
    Param_Index_SOFTLIMITP =204
    Param_Index_USE_EL = 205
    Param_Index_POL_EL = 206
    Param_Index_USE_FOLLOWING_ERR = 207
    Param_Index_RG_FOLLOWING_ERR = 208
    Param_Index_USE_INPOSITION = 209
    Param_Index_INPOSITION_RANGE = 210
    Param_Index_AXIS_IDCHK_EN = 211
    Param_Index_AXIS_NODE_ID = 222

    Param_Index_ENC_TYPE = 300
    Param_Index_AXIS_SINGLE_TURN_REG = 301
    Param_Index_HOMING_MODE = 302
    Param_Index_HOMING_METHOD_1ST = 303
    Param_Index_HOMING_SPEED_1ST = 304
    Param_Index_HOMING_ACCDEC_TIME_1ST = 305
    Param_Index_HOMING_OFFSET_1ST = 306
    Param_Index_HOMING_SHIFT_1ST = 306
    Param_Index_HOME_AUTO_SEARCHING_1ST = 308
    Param_Index_HOMING_METHOD_2ND = 309
    Param_Index_HOMING_SPEED_2ND = 310
    Param_Index_HOMING_ACCDEC_TIME_2ND = 311
    Param_Index_HOMING_OFFSET_2ND =312
    Param_Index_HOMING_SHIFT_2ND = 313
    Param_Index_HOME_AUTO_SEARCHING_2ND = 314

    Param_Index_USE_GROUP = 400
    Param_Index_GROUP_ID_SEL = 401
    Param_Index_GROUP_AXIS_SEL= 402

    Param_Index_AXIS_P_GAIN = 500
    Param_Index_AXIS_C_P_GAIN = 501
    Param_Index_AXIS_C_I_GAIN = 502

    Param_Index_USE_EXT_TIME_BASE = 600
    Param_Index_EXT_TIME_BASE_COUNTS = 601
    Param_Index_EXT_TIME_BASE_SLAVE_NO = 602
    Param_Index_EXT_TIME_BASE_SLAVE_START_POS = 603
    Param_Index_EXT_TIME_BASE_SLAVE_SIZE = 604
    Param_Index_EXT_TIME_BASE_MODULO = 605

    Param_Index_DUALFEEDBACK_ENABLE = 700
    Param_Index_DUALFEEDBACK_SLAVENO = 701
    Param_Index_DUALFEEDBACK_POS = 702
    Param_Index_DUALFEEDBACK_SIZE = 703
    Param_Index_DUALFEEDBACK_PULSE_PER_ROTATE = 704
...
#endregion

#region System


MXPDll = WinDLL('C:\WINDOWS\system32\MXP_SoftMotion.dll')
MXP_IsInited = MXPDll['MXP_IsInited']
MXP_IsInited.argtype = (POINTER(c_byte))
MXP_IsInited.restype = c_int32

MXP_InitKernel = MXPDll['MXP_InitKernel']
MXP_InitKernel.argtype = (POINTER(c_uint32))
MXP_InitKernel.restype = c_int32

MXP_InitKernel_Developer = MXPDll['MXP_InitKernel_Developer']
MXP_InitKernel_Developer.argtype = (POINTER(c_uint32))
MXP_InitKernel_Developer.restype = c_int32


MXP_SystemRun = MXPDll['MXP_SystemRun']
MXP_SystemRun.restype = c_int32

MXP_SystemStop = MXPDll['MXP_SystemStop']
MXP_SystemStop.restype = c_int32


MXP_SystemReset = MXPDll['MXP_SystemReset']
MXP_SystemReset.restype = c_int32

MXP_Destroy = MXPDll['MXP_Destroy']
MXP_Destroy.restype = c_int32

MXP_Destroy_Developer = MXPDll['MXP_Destroy_Developer']
MXP_Destroy_Developer.restype = c_int32


MXP_Destroy = MXPDll['MXP_Destroy']
MXP_Destroy.restype = c_int32

MXP_GetKernelStatus = MXPDll['MXP_GetKernelStatus']
MXP_GetKernelStatus.argtype = (POINTER(c_int32))
MXP_GetKernelStatus.restype = c_int32


MXP_CheckFeature = MXPDll['MXP_CheckFeature']
MXP_CheckFeature.argtype =  c_uint16, (POINTER(c_byte))
MXP_CheckFeature.restype = c_int32

MXP_GetOnlineMode = MXPDll['MXP_GetOnlineMode']
MXP_GetOnlineMode.argtype =  (POINTER(c_byte))
MXP_GetOnlineMode.restype = c_int32


MXP_GetSlaveNoFromNodeId = MXPDll['MXP_GetSlaveNoFromNodeId']
MXP_GetSlaveNoFromNodeId.argtype =  c_uint32, (POINTER(c_int32))
MXP_GetSlaveNoFromNodeId.restype = c_int32

MXP_GetAxisNoFromNodeId = MXPDll['MXP_GetAxisNoFromNodeId']
MXP_GetAxisNoFromNodeId.argtype =  c_uint32, (POINTER(c_int32))
MXP_GetAxisNoFromNodeId.restype = c_int32



MXP_GetSlaveName = MXPDll['MXP_GetSlaveName']
MXP_GetSlaveName.argtype = c_uint32 ,  ctypes.wintypes.LPWSTR
MXP_GetSlaveName.restype = c_int32

MXP_SM_IsSimulationMode = MXPDll['MXP_SM_IsSimulationMode']
MXP_SM_IsSimulationMode.argtype =  (POINTER(c_uint32))
MXP_SM_IsSimulationMode.restype = c_int32

MXP_IsSlaveOnline = MXPDll['MXP_IsSlaveOnline']
MXP_IsSlaveOnline.argtype =  [c_uint32, (POINTER(c_uint32))]
MXP_IsSlaveOnline.restype = c_int32

MXP_GetSlaveCount = MXPDll['MXP_GetSlaveCount']
MXP_GetSlaveCount.argtype =  [c_uint32, (POINTER(c_uint16))]
MXP_GetSlaveCount.restype = c_int32

MXP_QueryNodeType = MXPDll['MXP_QueryNodeType']
MXP_QueryNodeType.argtype =  [c_uint32, (POINTER(c_uint32))]
MXP_QueryNodeType.restype = c_int32



class HEARTBEAT(Structure):
    _fields_ = [
        ("AX", c_int32),
        ("Main", c_int32),
        ("Motion", c_int32),
        ("Scheduler", c_int32),
        ("Modbus", c_int32),
        ("EtherCAT", c_int32)]

class CREATION(Structure):
    _fields_ = [
        ("Main", c_int32),
        ("Motion", c_int32),
        ("Scheduler", c_int32),
        ("Modbus", c_int32),
        ("EtherCAT", c_int32)]

class MODE(Structure):
    _fields_ = [
        ("Start", c_int32),
        ("Init", c_int32),
        ("Ready", c_int32),
        ("Run", c_int32),
        ("bStop", c_int32),
        ("Reserved1", c_int32),
        ("Download", c_int32),
        ("Clear", c_int32),
        ("Reserved2", c_int32)]

class SETTINGTIME(Structure):
    _fields_ = [
        ("Sheduler", c_float),
        ("Motion", c_float),
        ("EtherCATIO", c_float),
        ("EtherCATMaster", c_float)]

class CURRENTTIME(Structure):
    _fields_ = [
        ("Sheduler", c_float),
        ("Motion", c_float),
        ("EtherCATIO", c_float),
        ("EtherCATMaster", c_float)]

class MINTIME(Structure):
    _fields_ = [
        ("Sheduler", c_float),
        ("Motion", c_float),
        ("EtherCATIO", c_float),
        ("EtherCATMaster", c_float)]

class MAXTIME(Structure):
    _fields_ = [
        ("Sheduler", c_float),
        ("Motion", c_float),
        ("EtherCATIO", c_float),
        ("EtherCATMaster", c_float)]

class CURRENTOPTIME(Structure):
    _fields_ = [
        ("Sheduler", c_float),
        ("Motion", c_float),
        ("EtherCATIO", c_float),
        ("EtherCATMaster", c_float)]

class MAXOPTIME(Structure):
    _fields_ = [
        ("Sheduler", c_float),
        ("Motion", c_float),
        ("EtherCATIO", c_float),
        ("EtherCATMaster", c_float)]

class ETHERCAT_STATE(Structure):
    _fields_ = [
        ("DCfaultCnt", c_int32),
        ("DCSlotPos", c_float),
        ("DCPrevInterval", c_float),
        ("DcPlus", c_int32),
        ("DcMinus", c_int32),
        ("QueuedSendFrames", c_uint32),
        ("QueuedLostFrames", c_uint32),
        ("QueuedSendFramesPerSec", c_float),

        ("CyclicSendFrames", c_uint32),
        ("CyclicLostFrames", c_uint32),
        ("CyclicSendFramesPerSec", c_float),

        ("RxErrorCnt", c_uint32),
        ("TxErrorCnt", c_uint32),

        ("Master", c_int32),
        ("Slaves", c_int32 * 132)]
class ETHERCATLINKSTATUS(Structure):
    _fields_ = [
        ("Master", c_int32),
        ("Slaves", c_int32 * 132)]

class ALARM(Structure):
    _fields_ = [
        ("History", c_int32 * 20)]

class ECATErr(Structure):
    _fields_ = [
        ("LinkLost", c_byte * 4),
        ("InvalidFrameCnt", c_byte * 4),
        ("RxErrCnt", c_byte * 4),
        ("ForwardRxErrCnt", c_byte * 4),
        ("EcatPUErrorCnt", c_byte),
        ("PDIErrorCnt", c_byte),
        ("AlstatusCode", c_byte)]

class PID(Structure):
    _fields_ = [
        ("UserApp", c_uint32),
        ("Mpm", c_uint32),
        ("Main", c_uint32),
        ("Motion", c_uint32),
        ("Scheduler", c_uint32),
        ("Modbus", c_uint32),
        ("EtherCAT", c_uint32)]

class SCANTIME(Structure):
    _fields_ = [
        ("Settingtime", SETTINGTIME),
        ("CurrentTime", CURRENTTIME),
        ("MinTime", MINTIME),
        ("MaxTime", MAXTIME),
        ("CurrentOPTime", CURRENTOPTIME),
        ("MaxOPTime", MAXOPTIME)]


class MXP_SYSINFO_OUT(Structure):
    _fields_ = [
        ("Heartbeat", HEARTBEAT),
        ("Creation", CREATION),
        ("Mode", MODE),
        ("Scantime", SCANTIME),
        ("EthercatState", ETHERCAT_STATE),
        ("ECatError", ECATErr * 132),
        ("EthercatLinkState", ETHERCATLINKSTATUS),
        ("Alarm", ALARM),
        ("Pid", PID),
        ("VerboseMode", c_byte)]

MXP_GetSystemInformation = MXPDll['MXP_GetSystemInformation']
MXP_GetSystemInformation.argtype = [POINTER(MXP_SYSINFO_OUT)]
MXP_GetSystemInformation.restype = c_int32


MXP_ET_SetMasterOnlineMode = MXPDll['MXP_ET_SetMasterOnlineMode']
MXP_ET_SetMasterOnlineMode.argtype = [c_int32]
MXP_ET_SetMasterOnlineMode.restype = c_int32

MXP_ET_SetSlaveOnlineMode = MXPDll['MXP_ET_SetSlaveOnlineMode']
MXP_ET_SetSlaveOnlineMode.argtype = [c_int32 , c_int32]
MXP_ET_SetSlaveOnlineMode.restype = c_int32

...
#endregion


#region Axis
class MXP_POWER_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8),
        ("EnablePositive", c_uint8),
        ("EnableNegative", c_uint8)]
class MXP_POWER_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Status", c_byte),
        ("Valid", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16)]

MXP_PowerCmd = MXPDll['MXP_PowerCmd']
MXP_PowerCmd.argtype = [c_uint32, POINTER(MXP_POWER_IN)]
MXP_PowerCmd.restype = c_int32
MXP_GetPowerOutParam = MXPDll['MXP_GetPowerOutParam']
MXP_GetPowerOutParam.argtype = c_uint32, POINTER(MXP_POWER_OUT)
MXP_GetPowerOutParam.restype = c_int32

class MXP_RESET_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8)]

MXP_ResetCmd = MXPDll['MXP_ResetCmd']
MXP_ResetCmd.argtype = [c_uint32, POINTER(MXP_RESET_IN)]
MXP_ResetCmd.restype = c_int32


class MXP_HOME_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8),
        ("Position", c_float),
        ("BufferMode", c_int32)]

MXP_HomeCmd = MXPDll['MXP_HomeCmd']
MXP_HomeCmd.argtype = [c_uint32, POINTER(MXP_HOME_IN)]
MXP_HomeCmd.restype = c_int32


class MXP_SETPOSITION_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8),
        ("Position", c_float),
        ("Relative", c_byte),
        ("BufferMode", c_int32)]

MXP_SetPositionCmd = MXPDll['MXP_SetPositionCmd']
MXP_SetPositionCmd.argtype = [c_uint32, POINTER(MXP_SETPOSITION_IN)]
MXP_SetPositionCmd.restype = c_int32

class MXP_HALT_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("BufferMode", c_int32)]

MXP_HaltCmd = MXPDll['MXP_HaltCmd']
MXP_HaltCmd.argtype = [c_uint32, POINTER(MXP_HALT_IN)]
MXP_HaltCmd.restype = c_int32

class MXP_STOP_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8),
        ("Deceleration", c_float),
        ("Jerk", c_float )]

MXP_StopCmd = MXPDll['MXP_StopCmd']
MXP_StopCmd.argtype = [c_uint32, POINTER(MXP_STOP_IN)]
MXP_StopCmd.restype = c_int32

class MXP_MOVEABSOLUTE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8 ),
        ("ContinuousUpdate", c_uint8),
        ("Position", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("BufferMode", c_int32)]

class MXP_MOVEABSOLUTE_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Done", c_uint8 ),
        ("Busy", c_uint8),
        ("Active", c_uint8),
        ("CommandAborted", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16)]

MXP_MoveAbsoluteCmd = MXPDll['MXP_MoveAbsoluteCmd']
MXP_MoveAbsoluteCmd.argtype = [c_uint32, POINTER(MXP_MOVEABSOLUTE_IN)]
MXP_MoveAbsoluteCmd.restype = c_int32

MXP_GetMoveAbsoluteOutParam = MXPDll['MXP_GetMoveAbsoluteOutParam']
MXP_GetMoveAbsoluteOutParam.argtype = [c_uint32, POINTER(MXP_MOVEABSOLUTE_OUT)]
MXP_GetMoveAbsoluteOutParam.restype = c_int32

class MXP_MOVERELATIVE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8 ),
        ("ContinuousUpdate", c_uint8),
        ("Distance", c_float ),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("BufferMode", c_int32)]

MXP_MoveRelativeCmd = MXPDll['MXP_MoveRelativeCmd']
MXP_MoveRelativeCmd.argtype = [c_uint32, POINTER(MXP_MOVERELATIVE_IN)]
MXP_MoveRelativeCmd.restype = c_int32


class MXP_DWELL_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8 ),
        ("TimeValue", c_float),
        ("BufferMode", c_int32)]

MXP_DwellCmd = MXPDll['MXP_DwellCmd']
MXP_DwellCmd.argtype = [c_uint32, POINTER(MXP_DWELL_IN)]
MXP_DwellCmd.restype = c_int32

class MXP_BUFFEREDDIGITALIO_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8 ),
        ("SlaveNo", c_uint16),
        ("BitPosition", c_uint16),
        ("BitValue", c_byte),
        ("BufferMode", c_int32)]

MXP_BufferedDigitalioCmd = MXPDll['MXP_BufferedDigitalioCmd']
MXP_BufferedDigitalioCmd.argtype = [c_uint32, POINTER(MXP_BUFFEREDDIGITALIO_IN)]
MXP_BufferedDigitalioCmd.restype = c_int32


#region 'SequenceMove Axis'

class MXP_MOVEABSOLUTE_EX_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8 ),
        ("ContinuousUpdate", c_uint8),
        ("Position", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("BufferMode", c_int32)]
MXP_MoveAbsoluteCmd_Ex = MXPDll['MXP_MoveAbsoluteCmd_Ex']
MXP_MoveAbsoluteCmd_Ex.argtype = [c_uint32, POINTER(MXP_MOVEABSOLUTE_EX_IN)]
MXP_MoveAbsoluteCmd_Ex.restype = c_int32

class MXP_MOVERELATIVE_EX_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8 ),
        ("ContinuousUpdate", c_uint8),
        ("Distance", c_float ),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("BufferMode", c_int32)]

MXP_MoveRelativeCmd_Ex = MXPDll['MXP_MoveRelativeCmd_Ex']
MXP_MoveRelativeCmd_Ex.argtype = [c_uint32, POINTER(MXP_MOVERELATIVE_EX_IN)]
MXP_MoveRelativeCmd_Ex.restype = c_int32


class MXP_DWELL_EX_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8 ),
        ("TimeValue", c_float),
        ("BufferMode", c_int32)]

MXP_DwellCmd_Ex = MXPDll['MXP_DwellCmd_Ex']
MXP_DwellCmd_Ex.argtype = [c_uint32, POINTER(MXP_DWELL_EX_IN)]
MXP_DwellCmd_Ex.restype = c_int32

class MXP_BUFFEREDDIGITALIO_EX_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8 ),
        ("SlaveNo", c_uint16),
        ("BitPosition", c_uint16),
        ("BitValue", c_byte),
        ("BufferMode", c_int32)]

MXP_BufferedDigitalioCmd_Ex = MXPDll['MXP_BufferedDigitalioCmd_Ex']
MXP_BufferedDigitalioCmd_Ex.argtype = [c_uint32, POINTER(MXP_BUFFEREDDIGITALIO_EX_IN)]
MXP_BufferedDigitalioCmd_Ex.restype = c_int32


#endregion


class MXP_MOVEVELOCITY_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8 ),
        ("ContinuousUpdate", c_uint8),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("Direction", c_int32),
        ("BufferMode", c_int32)]

MXP_MoveVelocityCmd = MXPDll['MXP_MoveVelocityCmd']
MXP_MoveVelocityCmd.argtype = [c_uint32, POINTER(MXP_MOVEVELOCITY_IN)]
MXP_MoveVelocityCmd.restype = c_int32


class MXP_SETOVERRIDE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8 ),
        ("VelFactor", c_float),
        ("AccFactor", c_float ),
        ("JerkFactor", c_float)]

MXP_SetOverrideCmd = MXPDll['MXP_SetOverrideCmd']
MXP_SetOverrideCmd.argtype = [c_uint32, POINTER(MXP_SETOVERRIDE_IN)]
MXP_SetOverrideCmd.restype = c_int32


...
#endregion

#region Monitoring
class MXP_READSTATUS_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READSTATUS_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8 ),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("ErrorStop", c_uint8),
        ("Disabled", c_uint8),
        ("Stopping", c_uint8),
        ("Homing", c_uint8),
        ("Standstill", c_uint8),
        ("DiscreteMotion", c_uint8),
        ("ContinuousMotion", c_uint8),
        ("SynchronizedMotion", c_uint8)]

MXP_ReadStatus = MXPDll['MXP_ReadStatus']
MXP_ReadStatus.argtype = [POINTER(MXP_READSTATUS_IN) ,POINTER(MXP_READSTATUS_OUT)]
MXP_ReadStatus.restype = c_int32

class MXP_READMOTIONSTATE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8),
        ("MCSource", c_int32)]

class MXP_READMOTIONSTATE_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("ConstantVelocity", c_uint8),
        ("Accelerating", c_uint8),
        ("Decelerating", c_uint8),
        ("DirectionPositive", c_uint8),
        ("DirectionNegative", c_uint8)]

MXP_ReadMotionState = MXPDll['MXP_ReadMotionState']
MXP_ReadMotionState.argtype = [POINTER(MXP_READMOTIONSTATE_IN) ,POINTER(MXP_READMOTIONSTATE_OUT)]
MXP_ReadMotionState.restype = c_int32


class MXP_READAXISINFO_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]
class MXP_READAXISINFO_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("HomeAbsSwitch", c_uint8),
        ("LimitSwitchPos", c_uint8),
        ("LimitSwitchNeg", c_uint8),
        ("Simulation", c_uint8),
        ("CommunicationReady", c_uint8),
        ("ReadyForPowerOn", c_uint8),
        ("PowerOn", c_uint8),
        ("IsHomed", c_uint8),
        ("AxisWarning", c_uint8)]

MXP_ReadAxisInfo = MXPDll['MXP_ReadAxisInfo']
MXP_ReadAxisInfo.argtype = [POINTER(MXP_READAXISINFO_IN), POINTER(MXP_READAXISINFO_OUT)]
MXP_ReadAxisInfo.restype = c_int32

class MXP_READACTUALPOSITION_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READACTUALPOSITION_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Position", c_float)]

MXP_ReadActualPosition = MXPDll['MXP_ReadActualPosition']
MXP_ReadActualPosition.argtype = [POINTER(MXP_READACTUALPOSITION_IN), POINTER(MXP_READACTUALPOSITION_OUT)]
MXP_ReadActualPosition.restype = c_int32


class MXP_READACTUALVELOCITY_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READACTUALVELOCITY_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Velocity", c_float)]

MXP_ReadActualVelocity = MXPDll['MXP_ReadActualVelocity']
MXP_ReadActualVelocity.argtype = [POINTER(MXP_READACTUALVELOCITY_IN), POINTER(MXP_READACTUALVELOCITY_OUT)]
MXP_ReadActualVelocity.restype = c_int32


class MXP_READACTUALTORQUE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READACTUALTORQUE_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Torque", c_float)]

MXP_ReadActualTorque = MXPDll['MXP_ReadActualTorque']
MXP_ReadActualTorque.argtype = [POINTER(MXP_READACTUALTORQUE_IN), POINTER(MXP_READACTUALTORQUE_OUT)]
MXP_ReadActualTorque.restype = c_int32


class MXP_READFOLLOWINGERRORVALUE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READFOLLOWINGERRORVALUE_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("FollowingErrorValue", c_float)]

MXP_ReadFollowingErrorValue = MXPDll['MXP_ReadFollowingErrorValue']
MXP_ReadFollowingErrorValue.argtype = [POINTER(MXP_READFOLLOWINGERRORVALUE_IN), POINTER(MXP_READFOLLOWINGERRORVALUE_OUT)]
MXP_ReadFollowingErrorValue.restype = c_int32


class MXP_READCOMMANDPOSITION_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READCOMMANDPOSITION_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("CommandPosition", c_float)]

MXP_ReadCommandPosition = MXPDll['MXP_ReadCommandPosition']
MXP_ReadCommandPosition.argtype = [POINTER(MXP_READCOMMANDPOSITION_IN), POINTER(MXP_READCOMMANDPOSITION_OUT)]
MXP_ReadCommandPosition.restype = c_int32


class MXP_READCOMMANDVELOCITY_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READCOMMANDVELOCITY_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("CommandVelocity", c_float)]

MXP_ReadCommandVelocity = MXPDll['MXP_ReadCommandVelocity']
MXP_ReadCommandVelocity.argtype = [POINTER(MXP_READCOMMANDVELOCITY_IN), POINTER(MXP_READCOMMANDVELOCITY_OUT)]
MXP_ReadCommandVelocity.restype = c_int32

class MXP_READAXISERROR_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8)]

class MXP_READAXISERROR_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("AxisErrorID", c_uint16),
        ("AuxErrorID", c_float)]

MXP_ReadAxisError = MXPDll['MXP_ReadAxisError']
MXP_ReadAxisError.argtype = [POINTER(MXP_READAXISERROR_IN), POINTER(MXP_READAXISERROR_OUT)]
MXP_ReadAxisError.restype = c_int32



class MXP_GROUPREADCOMMANDVELOCITY_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Enable", c_uint8),
        ("CoordSystem", c_uint16)]

class MXP_GROUPREADCOMMANDVELOCITY_OUT(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("CommandVelocity", c_float),
        ("PathCommandVelocity", c_float)]

MXP_GroupReadCommandVelocity = MXPDll['MXP_GroupReadCommandVelocity']
MXP_GroupReadCommandVelocity.argtype = [POINTER(MXP_GROUPREADCOMMANDVELOCITY_IN), POINTER(MXP_GROUPREADCOMMANDVELOCITY_OUT)]
MXP_GroupReadCommandVelocity.restype = c_int32

class MXP_GROUPREADCOMMANDPOSITION_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Enable", c_uint8),
        ("CoordSystem", c_uint16)]

class MXP_GROUPREADCOMMANDPOSITION_OUT(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("PositionX", c_float),
        ("PositionY", c_float),
        ("PositionZ", c_float),
        ("PositionU", c_float),
        ("PositionV", c_float),
        ("PositionW", c_float),
        ("PositionA", c_float),
        ("PositionB", c_float),
        ("PositionC", c_float)]

MXP_GroupReadCommandPosition = MXPDll['MXP_GroupReadCommandPosition']
MXP_GroupReadCommandPosition.argtype = [POINTER(MXP_GROUPREADCOMMANDPOSITION_IN), POINTER(MXP_GROUPREADCOMMANDPOSITION_OUT)]
MXP_GroupReadCommandPosition.restype = c_int32

class MXP_GROUPREADACTUALVELOCITY_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Enable", c_uint8),
        ("CoordSystem", c_uint16)]

class MXP_GROUPREADACTUALVELOCITY_OUT(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Velocity", c_float),
        ("PathVelocity", c_float)]

MXP_GroupReadActualVelocity = MXPDll['MXP_GroupReadActualVelocity']
MXP_GroupReadActualVelocity.argtype = [POINTER(MXP_GROUPREADACTUALVELOCITY_IN), POINTER(MXP_GROUPREADACTUALVELOCITY_OUT)]
MXP_GroupReadActualVelocity.restype = c_int32


class MXP_GROUPREADACTUALPOSITION_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Enable", c_uint8),
        ("CoordSystem", c_uint16)]

class MXP_GROUPREADACTUALPOSITION_OUT(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("PositionX", c_float),
        ("PositionY", c_float),
        ("PositionZ", c_float),
        ("PositionU", c_float),
        ("PositionV", c_float),
        ("PositionW", c_float),
        ("PositionA", c_float),
        ("PositionB", c_float),
        ("PositionC", c_float)]

MXP_GroupReadActualPosition = MXPDll['MXP_GroupReadActualPosition']
MXP_GroupReadActualPosition.argtype = [POINTER(MXP_GROUPREADACTUALPOSITION_IN), POINTER(MXP_GROUPREADACTUALPOSITION_OUT)]
MXP_GroupReadActualPosition.restype = c_int32


...
#endregion

#region Group

class MXP_GROUPSTOP_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("BufferMode", c_int32)]


MXP_GroupStopCmd = MXPDll['MXP_GroupStopCmd']
MXP_GroupStopCmd.argtype = [c_uint32 , POINTER(MXP_GROUPSTOP_IN)]
MXP_GroupStopCmd.restype = c_int32


class MXP_MOVELINEARABSOLUTE_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("PositionX", c_float),
        ("PositionY", c_float),
        ("PositionZ", c_float),
        ("PositionU", c_float),
        ("PositionV", c_float),
        ("PositionW", c_float),
        ("PositionA", c_float),
        ("PositionB", c_float),
        ("PositionC", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("CoordSystem", c_int32),
        ("BufferMode", c_int32),
        ("TransitionMode", c_int32),
        ("TransitionParamter", c_float)]


MXP_MoveLinearAbsoluteCmd = MXPDll['MXP_MoveLinearAbsoluteCmd']
MXP_MoveLinearAbsoluteCmd.argtype = [c_uint32 , POINTER(MXP_MOVELINEARABSOLUTE_IN)]
MXP_MoveLinearAbsoluteCmd.restype = c_int32


class MXP_MOVELINEARRELATIVE_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("DistanceX", c_float),
        ("DistanceY", c_float),
        ("DistanceZ", c_float),
        ("DistanceU", c_float),
        ("DistanceV", c_float),
        ("DistanceW", c_float),
        ("DistanceA", c_float),
        ("DistanceB", c_float),
        ("DistanceC", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("CoordSystem", c_int32),
        ("BufferMode", c_int32),
        ("TransitionMode", c_int32),
        ("TransitionParamter", c_float)]


MXP_MoveLinearRelativeCmd = MXPDll['MXP_MoveLinearRelativeCmd']
MXP_MoveLinearRelativeCmd.argtype = [c_uint32 , POINTER(MXP_MOVELINEARRELATIVE_IN)]
MXP_MoveLinearRelativeCmd.restype = c_int32

# region ExFunctionGroup
class MXP_MOVELINEARABSOLUTE_EX_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8),
        ("PositionX", c_float),
        ("PositionY", c_float),
        ("PositionZ", c_float),
        ("PositionU", c_float),
        ("PositionV", c_float),
        ("PositionW", c_float),
        ("PositionA", c_float),
        ("PositionB", c_float),
        ("PositionC", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("CoordSystem", c_int32),
        ("BufferMode", c_int32),
        ("TransitionMode", c_int32),
        ("TransitionParamter", c_float)]

MXP_MoveLinearAbsoluteCmd_Ex = MXPDll['MXP_MoveLinearAbsoluteCmd_Ex']
MXP_MoveLinearAbsoluteCmd_Ex.argtype = [c_uint32 , POINTER(MXP_MOVELINEARABSOLUTE_EX_IN)]
MXP_MoveLinearAbsoluteCmd_Ex.restype = c_int32


class MXP_MOVELINEARRELATIVE_EX_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8),
        ("DistanceX", c_float),
        ("DistanceY", c_float),
        ("DistanceZ", c_float),
        ("DistanceU", c_float),
        ("DistanceV", c_float),
        ("DistanceW", c_float),
        ("DistanceA", c_float),
        ("DistanceB", c_float),
        ("DistanceC", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("CoordSystem", c_int32),
        ("BufferMode", c_int32),
        ("TransitionMode", c_int32),
        ("TransitionParamter", c_float)]


MXP_MoveLinearRelativeCmd_Ex = MXPDll['MXP_MoveLinearRelativeCmd_Ex']
MXP_MoveLinearRelativeCmd_Ex.argtype = [c_uint32 , POINTER(MXP_MOVELINEARRELATIVE_EX_IN)]
MXP_MoveLinearRelativeCmd_Ex.restype = c_int32


class MXP_GROUPDWELL_EX_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8),
        ("TimeValue", c_float),
        ("BufferMode", c_int32)
        ]

MXP_GroupDwellCmd_Ex = MXPDll['MXP_GroupDwellCmd_Ex']
MXP_GroupDwellCmd_Ex.argtype = [c_uint32 , POINTER(MXP_GROUPDWELL_EX_IN)]
MXP_GroupDwellCmd_Ex.restype = c_int32



class MXP_GROUPBUFFEREDDIGITALIO_EX_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("CommandBlockNo", c_uint16),
        ("Execute", c_uint8),
        ("SlaveNo", c_uint16),
        ("BitPosition", c_uint16),
        ("BitValue", c_byte),
        ("BufferMode", c_int32)
        ]

MXP_GroupBufferedDigitalioCmd_Ex = MXPDll['MXP_GroupBufferedDigitalioCmd_Ex']
MXP_GroupBufferedDigitalioCmd_Ex.argtype = [c_uint32 , POINTER(MXP_GROUPBUFFEREDDIGITALIO_EX_IN)]
MXP_GroupBufferedDigitalioCmd_Ex.restype = c_int32

#endregion





class MXP_GROUPDWELL_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("TimeValue", c_float),
        ("BufferMode", c_int32)
        ]

MXP_GroupDwellCmd = MXPDll['MXP_GroupDwellCmd']
MXP_GroupDwellCmd.argtype = [c_uint32 , POINTER(MXP_GROUPDWELL_IN)]
MXP_GroupDwellCmd.restype = c_int32

class MXP_GROUPBUFFEREDDIGITALIO_OUT(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("SlaveNo", c_uint16),
        ("BitPosition", c_uint16),
        ("BitValue", c_byte),
        ("BufferMode", c_int32)
        ]

MXP_GroupBufferedDigitalioCmd = MXPDll['MXP_GroupBufferedDigitalioCmd']
MXP_GroupBufferedDigitalioCmd.argtype = [c_uint32 , POINTER(MXP_GROUPBUFFEREDDIGITALIO_OUT)]
MXP_GroupBufferedDigitalioCmd.restype = c_int32










class MXP_MOVECIRCULARABSOLUTE_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("CircMode", c_int32),
        ("AuxPoint1", c_float),
        ("AuxPoint2", c_float),
        ("EndPoint1", c_float),
        ("EndPoint2", c_float),
        ("PathChoice", c_int32),
        ("Plane1", c_int32),
        ("Plane2", c_int32),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("CoordSystem", c_int32),
        ("BufferMode", c_int32),
        ("TransitionMode", c_int32),
        ("TransitionParamter", c_float)]



MXP_MoveCircularAbsoluteCmd = MXPDll['MXP_MoveCircularAbsoluteCmd']
MXP_MoveCircularAbsoluteCmd.argtype = [c_uint32 , POINTER(MXP_MOVECIRCULARABSOLUTE_IN)]
MXP_MoveCircularAbsoluteCmd.restype = c_int32


class MXP_MOVECIRCULARRELATIVE_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Execute", c_uint8),
        ("CircMode", c_int32),
        ("AuxPoint1", c_float),
        ("AuxPoint2", c_float),
        ("EndPoint1", c_float),
        ("EndPoint2", c_float),
        ("PathChoice", c_int32),
        ("Plane1", c_int32),
        ("Plane2", c_int32),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("CoordSystem", c_int32),
        ("BufferMode", c_int32),
        ("TransitionMode", c_int32),
        ("TransitionParamter", c_float)]

MXP_MoveCircularRelativeCmd = MXPDll['MXP_MoveCircularRelativeCmd']
MXP_MoveCircularRelativeCmd.argtype = [c_uint32 , POINTER(MXP_MOVECIRCULARRELATIVE_IN)]
MXP_MoveCircularRelativeCmd.restype = c_int32


class MXP_GROUPSETOVERRIDE_IN(Structure):
    _fields_ = [
        ("AxesGroup", c_uint32),
        ("Enable", c_byte),
        ("VelFactor", c_float),
        ("AccFactor", c_float),
        ("JerkFactor", c_float)]

MXP_GroupSetOverrideCmd = MXPDll['MXP_GroupSetOverrideCmd']
MXP_GroupSetOverrideCmd.argtype = [c_uint32 , POINTER(MXP_GROUPSETOVERRIDE_IN)]
MXP_GroupSetOverrideCmd.restype = c_int32

...
#endregion


#region Parameter
class MXP_READPARAMETER_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_uint8),
        ("ParameterNumber", c_int32)]

class MXP_READPARAMETER_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_uint8 ),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Value", c_float)]

MXP_ReadParameter = MXPDll['MXP_ReadParameter']
MXP_ReadParameter.argtype = [POINTER(MXP_READPARAMETER_IN) ,POINTER(MXP_READPARAMETER_IN)]
MXP_ReadParameter.restype = c_int32


class MXP_WRITEPARAMETER_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_uint8),
        ("ParameterNumber", c_uint32),
        ("Value", c_float),
        ("ExecutionMode", c_int32)]

MXP_WriteParameterCmd = MXPDll['MXP_WriteParameterCmd']
MXP_WriteParameterCmd.argtype = [c_uint32 ,POINTER(MXP_WRITEPARAMETER_IN)]
MXP_WriteParameterCmd.restype = c_int32

class MXP_WRITEPARAMETEREX_IN(Structure):
    _fields_ = [
        ("Execute", c_uint8),
        ("ExecutionMode", c_int32)]

MXP_WriteParameterExCmd = MXPDll['MXP_WriteParameterExCmd']
MXP_WriteParameterExCmd.argtype = [c_uint32 ,POINTER(MXP_WRITEPARAMETEREX_IN)]
MXP_WriteParameterExCmd.restype = c_int32

...
#endregion

#region PDO and ET
class MXP_READPDODATA_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Enable", c_uint8),
        ("Direction", c_uint8),
        ("Offset", c_uint16),
        ("Size", c_uint16)]

class MXP_READPDODATA_OUT(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Valid", c_uint8 ),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16)]
MXP_ReadPDOData = MXPDll['MXP_ReadPDOData']
MXP_ReadPDOData.argtype = [POINTER(MXP_READPDODATA_IN) ,POINTER(MXP_READPDODATA_OUT) ,POINTER(c_byte)]
MXP_ReadPDOData.restype = c_int32

class MXP_WRITEPDODATA_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Execute", c_uint8),
        ("Direction", c_uint8),
        ("Offset", c_uint16),
        ("Size", c_uint16)]


MXP_WritePDODataCmd = MXPDll['MXP_WritePDODataCmd']
MXP_WritePDODataCmd.argtype = [c_uint32, POINTER(MXP_WRITEPDODATA_IN),POINTER(c_byte)]
MXP_WritePDODataCmd.restype = c_int32


class MXP_ET_READPARAMETER_IN(Structure):
    _fields_ = [
        ("SlaveNo", c_uint32),
        ("Index", c_uint32),
        ("SubIndex", c_uint32),
        ("BufLen", c_uint32)]

MXP_ET_ReadParameterCmd = MXPDll['MXP_ET_ReadParameterCmd']
MXP_ET_ReadParameterCmd.argtype = [c_uint32, POINTER(MXP_ET_READPARAMETER_IN)]
MXP_ET_ReadParameterCmd.restype = c_int32

class MXP_ET_READPARAMETER_OUT(Structure):
    _fields_ = [
        ("SlaveNo", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Data", c_uint8 *1024)]

MXP_ET_GetReadParameterOutParam = MXPDll['MXP_ET_GetReadParameterOutParam']
MXP_ET_GetReadParameterOutParam.argtype = [c_uint32, POINTER(MXP_ET_READPARAMETER_OUT)]
MXP_ET_GetReadParameterOutParam.restype = c_int32



class MXP_ET_WRITEPARAMETER_IN(Structure):
    _fields_ = [
        ("SlaveNo", c_uint32),
        ("Index", c_uint32),
        ("SubIndex", c_uint32),
        ("BufLen", c_uint32),
        ("Data", c_uint32)]

MXP_ET_WriteParameterCmd = MXPDll['MXP_ET_WriteParameterCmd']
MXP_ET_WriteParameterCmd.argtype = [c_uint32, POINTER(MXP_ET_WRITEPARAMETER_IN)]
MXP_ET_WriteParameterCmd.restype = c_int32


class MXP_ET_WRITEPARAMETER_OUT(Structure):
    _fields_ = [
        ("SlaveNo", c_uint32),
        ("Done", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16)]

MXP_ET_GetWriteParameterOutParam = MXPDll['MXP_ET_GetWriteParameterOutParam']
MXP_ET_GetWriteParameterOutParam.argtype = [c_uint32, POINTER(MXP_ET_WRITEPARAMETER_OUT)]
MXP_ET_GetWriteParameterOutParam.restype = c_int32

#InnData = MXP_READPDODATA_IN(0,1,0,0,2)
#OutData = MXP_READPDODATA_OUT()
#MXP_ReadPDOData()
...
#endregion

#region PLCInterface
MXP_PLC_ReadSystemRegister = MXPDll['MXP_PLC_ReadSystemRegister']
MXP_PLC_ReadSystemRegister.argtype = [c_uint32, c_uint32, c_uint32, POINTER(c_uint32)]
MXP_PLC_ReadSystemRegister.restype = c_int32

MXP_PLC_WriteSystemRegister = MXPDll['MXP_PLC_WriteSystemRegister']
MXP_PLC_WriteSystemRegister.argtype = [c_uint32, c_uint32, c_uint32, c_uint32]
MXP_PLC_WriteSystemRegister.restype = c_int32



MXP_PLC_ReadSystemRegisterEx = MXPDll['MXP_PLC_ReadSystemRegisterEx']
MXP_PLC_ReadSystemRegisterEx.argtype = [c_uint32, c_uint32, c_uint32, POINTER(c_uint64)]
MXP_PLC_ReadSystemRegister.restype = c_int32

MXP_PLC_WriteSystemRegisterEx = MXPDll['MXP_PLC_WriteSystemRegisterEx']
MXP_PLC_WriteSystemRegisterEx.argtype = [c_uint32, c_uint32, c_uint32, c_uint64]
MXP_PLC_WriteSystemRegisterEx.restype = c_int32

...
#endregion


#region IO

class MXP_WRITEOUTPUTS_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Execute", c_uint8),
        ("Size", c_uint16)]

MXP_WriteOutputsCmd = MXPDll['MXP_WriteOutputsCmd']
MXP_WriteOutputsCmd.argtype = [ c_uint32 ,POINTER(MXP_WRITEOUTPUTS_IN), POINTER(c_byte)]
MXP_WriteOutputsCmd.restype = c_int32

class MXP_WRITEDIGITALOUTPUT_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Execute", c_uint8),
        ("OutputNumber", c_int32),
        ("Value", c_ubyte),
        ("ExecutionMode", c_int32)]

MXP_WriteDigitalOutputCmd = MXPDll['MXP_WriteDigitalOutputCmd']
MXP_WriteDigitalOutputCmd.argtype = [ c_uint32 ,POINTER(MXP_WRITEDIGITALOUTPUT_IN)]
MXP_WriteDigitalOutputCmd.restype = c_int32

class MXP_READDIGITALINPUT_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Enable", c_uint8),
        ("InputNumber", c_int32)]

class MXP_READDIGITALINPUT_OUT(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Value", c_uint8) ]
MXP_ReadDigitalInput = MXPDll['MXP_ReadDigitalInput']
MXP_ReadDigitalInput.argtype = [ POINTER(MXP_READDIGITALINPUT_IN) ,POINTER(MXP_READDIGITALINPUT_OUT)]
MXP_ReadDigitalInput.restype = c_int32
class MXP_READDIGITALOUTPUT_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Enable", c_uint8),
        ("OutputNumber", c_int32)]

class MXP_READDIGITALOUTPUT_OUT(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Value", c_uint8) ]

MXP_ReadDigitalOutput = MXPDll['MXP_ReadDigitalOutput']
MXP_ReadDigitalOutput.argtype = [ POINTER(MXP_READDIGITALOUTPUT_IN) ,POINTER(MXP_READDIGITALOUTPUT_OUT)]
MXP_ReadDigitalOutput.restype = c_int32


class MXP_READOUTPUTS_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Enable", c_uint8)]
class MXP_READOUTPUTS_OUT(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Size", c_uint16)]
MXP_ReadOutputs = MXPDll['MXP_ReadOutputs']
MXP_ReadOutputs.argtype = [ POINTER(MXP_READOUTPUTS_IN) ,POINTER(MXP_READOUTPUTS_OUT) ,POINTER(c_uint8)]
MXP_ReadOutputs.restype = c_int32



class MXP_READINPUTS_IN(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Enable", c_uint8)]
class MXP_READINPUTS_OUT(Structure):
    _fields_ = [
        ("SourceNo", c_uint32),
        ("Valid", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("Size", c_uint16)]
MXP_ReadInputs = MXPDll['MXP_ReadInputs']
MXP_ReadInputs.argtype = [ POINTER(MXP_READINPUTS_IN) ,POINTER(MXP_READINPUTS_OUT) ,POINTER(c_byte)]
MXP_ReadInputs.restype = c_int32



...
#endregion



#region Gear
class MXP_GEARIN_IN(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("Execute", c_byte),
        ("ContinuousUpdate", c_byte),
        ("RatioNumerator", c_int32),
        ("RatioDenominator", c_uint32),
        ("MasterValueSource", c_int32),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("BufferMode", c_int32)  ]

class MXP_GEARIN_OUT(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("InGear", c_byte),
        ("Busy", c_byte),
        ("Active", c_byte),
        ("CommandAborted", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16 ) ]

class MXP_GEAROUT_IN(Structure):
    _fields_ = [
        ("Slave", c_uint32),
        ("Execute", c_byte) ]

class MXP_GEAROUT_OUT(Structure):
    _fields_ = [
        ("Slave", c_uint32),
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16 ) ]


MXP_GearInCmd = MXPDll['MXP_GearInCmd']
MXP_GearInCmd.argtype = [ c_uint32, POINTER(MXP_GEARIN_IN)]
MXP_GearInCmd.restype = c_int32

MXP_GetGearInOutParam = MXPDll['MXP_GetGearInOutParam']
MXP_GetGearInOutParam.argtype = [ c_uint32, POINTER(MXP_GEARIN_OUT)]
MXP_GetGearInOutParam.restype = c_int32

MXP_GearOutCmd = MXPDll['MXP_GearOutCmd']
MXP_GearOutCmd.argtype = [ c_uint32, POINTER(MXP_GEAROUT_IN)]
MXP_GearOutCmd.restype = c_int32



class MXP_GEARINPOS_IN(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("Execute", c_byte),
        ("RatioNumerator", c_int32),
        ("RatioDenominator", c_uint32),
        ("MasterValueSource", c_int32),
        ("MasterSyncPosition", c_float),
        ("SlaveSyncPosition", c_float),
        ("SyncMode", c_int32),
        ("MasterStartDistance", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("BufferMode", c_int32)]

class MXP_GEARINPOS_OUT(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("StartSync", c_byte),
        ("InSync", c_byte),
        ("Busy", c_byte),
        ("Active", c_byte),
        ("CommandAborted", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16 )]

MXP_GearInPosCmd = MXPDll['MXP_GearInPosCmd']
MXP_GearInPosCmd.argtype = [ c_uint32, POINTER(MXP_GEARINPOS_IN)]
MXP_GearInPosCmd.restype = c_int32

MXP_GetGearInPosOutParam = MXPDll['MXP_GetGearInPosOutParam']
MXP_GetGearInPosOutParam.argtype = [ c_uint32, POINTER(MXP_GEARINPOS_OUT)]
MXP_GetGearInPosOutParam.restype = c_int32
...
#endregion
#region Enum Define


#region CAM
class MXP_CAMTABLE_REF(Structure):
    _fields_ = [
        ("MasterPos", c_float),
        ("SlavePos", c_float),
        ("SlaveVel", c_float),
        ("SlaveAcc", c_float),
        ("SlaveJerk", c_float),
        ("PointType", c_uint32),
        ("InterpolationType", c_int32)]

class MXP_WRITECAMTABLE_IN(Structure):
    _fields_ = [
        ("CamTable", c_uint32),
        ("Execute", c_byte),
        ("DataSize", c_uint16),
        ("ExecutionMode", c_uint16),
        ("CamDataArray", MXP_CAMTABLE_REF*400)]


class MXP_WRITECAMTABLE_OUT(Structure):
    _fields_ = [
        ("CamTable", c_uint32),
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16)]


MXP_WriteCamTableCmd = MXPDll['MXP_WriteCamTableCmd']
MXP_WriteCamTableCmd.argtype = [ c_uint32, POINTER(MXP_WRITECAMTABLE_IN)]
MXP_WriteCamTableCmd.restype = c_int32

MXP_GetWriteCamTableOutParam = MXPDll['MXP_GetWriteCamTableOutParam']
MXP_GetWriteCamTableOutParam.argtype = [ c_uint32, POINTER(MXP_WRITECAMTABLE_OUT)]
MXP_GetWriteCamTableOutParam.restype = c_int32


class MXP_READCAMTABLE_IN(Structure):
    _fields_ = [
        ("CamTable", c_uint32),
        ("Execute", c_byte)]


class MXP_READCAMTABLE_OUT(Structure):
    _fields_ = [
        ("CamTable", c_uint32),
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16),
        ("DataSize", c_uint16),
        ("CamDataArray", MXP_CAMTABLE_REF*400)]


MXP_ReadCamTableCmd = MXPDll['MXP_ReadCamTableCmd']
MXP_ReadCamTableCmd.argtype = [ c_uint32, POINTER(MXP_READCAMTABLE_IN)]
MXP_ReadCamTableCmd.restype = c_int32


MXP_GetReadCamTableOutParam = MXPDll['MXP_GetReadCamTableOutParam']
MXP_GetReadCamTableOutParam.argtype = [ c_uint32, POINTER(MXP_READCAMTABLE_OUT)]
MXP_GetReadCamTableOutParam.restype = c_int32



class MXP_CAMTABLESELECT_IN(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("CamTable", c_uint32),
        ("Execute", c_uint8),
        ("Periodic", c_uint8),
        ("MasterAbsolute", c_uint8),
        ("SlaveAbsolute", c_uint8),
        ("ExecutionMode", c_int32)]

MXP_CamTableSelectCmd = MXPDll['MXP_CamTableSelectCmd']
MXP_CamTableSelectCmd.argtype = [ c_uint32, POINTER(MXP_CAMTABLESELECT_IN)]
MXP_CamTableSelectCmd.restype = c_int32

class MXP_CAMIN_IN(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("Execute", c_uint8),
        ("ContinuousUpdate", c_uint8),
        ("MasterOffset", c_float),
        ("SlaveOffset", c_float),
        ("MasterScaling", c_float),
        ("SlaveScaling", c_float),
        ("MasterStartDistance", c_float),
        ("MasterSyncPosition", c_float),
        ("StartMode", c_int32),
        ("MasterValueSource", c_int32),
        ("CamTableID", c_uint16),
        ("BufferMode", c_int32)]

MXP_CamInCmd = MXPDll['MXP_CamInCmd']
MXP_CamInCmd.argtype = [ c_uint32, POINTER(MXP_CAMIN_IN)]
MXP_CamInCmd.restype = c_int32


class MXP_CAMIN_OUT(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("InSync", c_uint8),
        ("Busy", c_uint8),
        ("Active", c_uint8),
        ("CommandAborted", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("EndOfProfile", c_uint8)]

MXP_GetCamInOutParam = MXPDll['MXP_GetCamInOutParam']
MXP_GetCamInOutParam.argtype = [ c_uint32, POINTER(MXP_CAMIN_OUT)]
MXP_GetCamInOutParam.restype = c_int32


class MXP_CAMOUT_IN(Structure):
    _fields_ = [
        ("Slave", c_uint32),
        ("Execute", c_uint8)]

MXP_CamOutCmd = MXPDll['MXP_CamOutCmd']
MXP_CamOutCmd.argtype = [ c_uint32, POINTER(MXP_CAMOUT_IN)]
MXP_CamOutCmd.restype = c_int32

class MXP_CAMSCALING_IN(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("Execute", c_uint8),
        ("ActivationMode", c_uint16),
        ("MasterScalingMode", c_uint16),
        ("SlaveScalingMode", c_uint16),
        ("ActivationPosition", c_float),
        ("MasterOffset", c_float),
        ("SlaveOffset", c_float),
        ("MasterScaling", c_float),
        ("SlaveScaling", c_float)]

MXP_CamScalingCmd = MXPDll['MXP_CamScalingCmd']
MXP_CamScalingCmd.argtype = [ c_uint32, POINTER(MXP_CAMSCALING_IN)]
MXP_CamScalingCmd.restype = c_int32


class MXP_PHASING_IN(Structure):
    _fields_ = [
        ("Master", c_uint32),
        ("Slave", c_uint32),
        ("Execute", c_uint8),
        ("PhaseShift", c_float),
        ("Velocity", c_float),
        ("Acceleration", c_float),
        ("Deceleration", c_float),
        ("Jerk", c_float),
        ("BufferMode", c_int32)]

MXP_PhasingCmd = MXPDll['MXP_PhasingCmd']
MXP_PhasingCmd.argtype = [ c_uint32, POINTER(MXP_PHASING_IN)]
MXP_PhasingCmd.restype = c_int32


class MXP_RDCAMTABLESLAVEPOS_IN(Structure):
    _fields_ = [
        ("CamTable", c_uint32),
        ("Execute", c_uint8),
        ("MasterPosition", c_float)]

MXP_RdCamTableSlavePosCmd = MXPDll['MXP_RdCamTableSlavePosCmd']
MXP_RdCamTableSlavePosCmd.argtype = [ c_uint32, POINTER(MXP_RDCAMTABLESLAVEPOS_IN)]
MXP_RdCamTableSlavePosCmd.restype = c_int32


class MXP_RDCAMTABLESLAVEPOS_OUT(Structure):
    _fields_ = [
        ("CamTable", c_uint32),
        ("Done", c_uint8),
        ("Busy", c_uint8),
        ("Errored", c_uint8),
        ("ErrorID", c_uint16),
        ("SlavePosition", c_float)]


MXP_GetRdCamTableSlavePosOutParam = MXPDll['MXP_GetRdCamTableSlavePosOutParam']
MXP_GetRdCamTableSlavePosOutParam.argtype = [ c_uint32, POINTER(MXP_RDCAMTABLESLAVEPOS_OUT)]
MXP_GetRdCamTableSlavePosOutParam.restype = c_int32
...
#endregion
#region Enum Define


#region ProfileMove

class MXP_PROFILE_MOVE_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Execute", c_byte),
        ("Tablesize", c_uint32),
        ("IOTablesize", c_uint32),
        ("RepeatCount", c_byte),
        ("StartDwell", c_float),
        ("EndDwell", c_float),
        ("ReverseMode", c_byte)]

class MXP_PROFILE_MOVE_OUT(Structure):
    _fields_ = [
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Active", c_byte),
        ("CommandAborted", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16)]


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

MXP_GetProfileTable_Ex = MXPDll['MXP_GetProfileTable_Ex']
MXP_GetProfileTable_Ex.argtype = [POINTER(MXP_FILE_TABLE_ARRAY_IN), c_uint32 , POINTER(c_uint32) ,ctypes.POINTER(MXP_PROFILE_TABLE_ARRAY_IN) ]
MXP_GetProfileTable_Ex.restype = c_int32

MXP_ProfileMoveCmd_Ex = MXPDll['MXP_ProfileMoveCmd_Ex']
MXP_ProfileMoveCmd_Ex.argtype = [c_uint32 , POINTER(MXP_PROFILE_MOVE_IN) ,ctypes.POINTER(MXP_PROFILE_TABLE_ARRAY_IN)
                                ,ctypes.POINTER(MXP_IO_TABLE_ARRAY_IN)]
MXP_ProfileMoveCmd_Ex.restype = c_int32


MXP_ProfileMoveOutParam_Ex = MXPDll['MXP_ProfileMoveOutParam_Ex']
MXP_ProfileMoveOutParam_Ex.argtype = [c_uint32 , POINTER(MXP_PROFILE_MOVE_IN) ,ctypes.POINTER(MXP_PROFILE_MOVE_OUT)]
MXP_ProfileMoveOutParam_Ex.restype = c_int32


...
#endregion
#region Enum Define


#region Touchprob


class MXP_SETTOUCHPROBEFUNC_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ('FuncData' , c_uint16)]
MXP_SetTouchProbeFunctionCmd = MXPDll['MXP_SetTouchProbeFunctionCmd']
MXP_SetTouchProbeFunctionCmd.argtype = [c_uint32 , POINTER(MXP_SETTOUCHPROBEFUNC_IN) ]
MXP_SetTouchProbeFunctionCmd.restype = c_int32

class MXP_READACTUALTOUCHPROBESTATUS_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte)]

class MXP_READACTUALTOUCHPROBESTATUS_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_byte),
        ("Busy", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16),
        ("Status", c_uint16)]

MXP_ReadActualTouchProbeStatus = MXPDll['MXP_ReadActualTouchProbeStatus']
MXP_ReadActualTouchProbeStatus.argtype = [POINTER(MXP_READACTUALTOUCHPROBESTATUS_IN) ,POINTER(MXP_READACTUALTOUCHPROBESTATUS_OUT) ]
MXP_ReadActualTouchProbeStatus.restype = c_int32


class MXP_READACTUALTOUCHPROBEPOSITION_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ("Channel", c_int32),
        ("Edge", c_int32)]

class MXP_READACTUALTOUCHPROBEPOSITION_EX_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_byte),
        ("Busy", c_byte),
        ("Errored", c_byte),
        ("ErrorID", c_uint16),
        ("EdgePositivePosition", c_float),
        ("EdgeNegativePosition", c_float)]

MXP_ReadActualTouchProbePosition_Ex = MXPDll['MXP_ReadActualTouchProbePosition_Ex']
MXP_ReadActualTouchProbePosition_Ex.argtype = [POINTER(MXP_READACTUALTOUCHPROBEPOSITION_IN) ,POINTER(MXP_READACTUALTOUCHPROBEPOSITION_EX_OUT) ]
MXP_ReadActualTouchProbePosition_Ex.restype = c_int32

...
#endregion
#region Enum Define


#region UnitChange
class MXP_ACCDECTOACCTIME_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ('TargetVel' , c_float),
        ('AccDec', c_float),
        ('Jerk', c_float)]
class MXP_ACCDECTOACCTIME_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_byte),
        ('Busy' , c_byte),
        ('Errored', c_byte),
        ('ErrorID', c_uint16),
        ('AccDecBuildUp', c_float),
        ('LimitAccDec', c_float),
        ('AccDecRampDown', c_float),
        ('RuildUppc', c_float),
        ('Limitpc', c_float),
        ('RampDownpc', c_float)]
MXP_AccDecToAccTime = MXPDll['MXP_AccDecToAccTime']
MXP_AccDecToAccTime.argtype = [POINTER(MXP_ACCDECTOACCTIME_IN),POINTER(MXP_ACCDECTOACCTIME_OUT) ]
MXP_AccDecToAccTime.restype = c_int32


class MXP_ACCTIMETOACCDEC_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ('TargetVel' , c_float),
        ('AccDecBuildUp', c_float),
        ('LimitAccDec', c_float),
        ('AccDecRampDown', c_float)]

class MXP_ACCTIMETOACCDEC_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Valid", c_byte),
        ('Busy' , c_byte),
        ('Errored', c_byte),
        ('ErrorID', c_uint16),
        ('AccDec', c_float),
        ('Jerk', c_float)]
MXP_AccTimeToAccDec = MXPDll['MXP_AccTimeToAccDec']
MXP_AccTimeToAccDec.argtype = [POINTER(MXP_ACCTIMETOACCDEC_IN),POINTER(MXP_ACCTIMETOACCDEC_OUT) ]
MXP_AccTimeToAccDec.restype = c_int32

...
#endregion
#region Enum Define

#region DirectCmd
class MXP_MOVEDIRECTPOSITION_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ('Position', c_float)]

class MXP_MOVEDIRECTPOSITION_OUT(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Done", c_byte),
        ('Busy' , c_byte),
        ('Active', c_byte),
        ('CommandAborted', c_byte),
        ('Errored', c_byte),
        ('ErrorID', c_uint16)]

MXP_MoveDirectPositionCmd = MXPDll['MXP_MoveDirectPositionCmd']
MXP_MoveDirectPositionCmd.argtype = [c_uint32, POINTER(MXP_MOVEDIRECTPOSITION_IN) ]
MXP_MoveDirectPositionCmd.restype = c_int32

MXP_GetMoveDirectPositionOutParam = MXPDll['MXP_GetMoveDirectPositionOutParam']
MXP_GetMoveDirectPositionOutParam.argtype = [c_uint32, POINTER(MXP_MOVEDIRECTPOSITION_OUT) ]
MXP_GetMoveDirectPositionOutParam.restype = c_int32


class MXP_MOVEDIRECTVELOCITY_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ('Velocity', c_float)]

MXP_MoveDirectVelocityCmd = MXPDll['MXP_MoveDirectVelocityCmd']
MXP_MoveDirectVelocityCmd.argtype = [c_uint32, POINTER(MXP_MOVEDIRECTVELOCITY_IN) ]
MXP_MoveDirectVelocityCmd.restype = c_int32

class MXP_DIRECTTORQUECONTROL_IN(Structure):
    _fields_ = [
        ("Axis", c_uint32),
        ("Enable", c_byte),
        ('Torque', c_float)]

MXP_DirectTorqueControlCmd = MXPDll['MXP_DirectTorqueControlCmd']
MXP_DirectTorqueControlCmd.argtype = [c_uint32, POINTER(MXP_DIRECTTORQUECONTROL_IN) ]
MXP_DirectTorqueControlCmd.restype = c_int32


...
#endregion
#region Enum Define

#region CCC Define
class MXP_MULTIAXISCOUPLESET_IN(Structure):
    _fields_ = [
        ("Execute", c_byte),
        ("ArrayAxisNo", c_uint32*10),
        ("AxisCount", c_uint16),
        ("Mode", c_uint16)]
class MXP_MULTIAXISCOUPLESET_OUT(Structure):
    _fields_ = [
        ("ArrayAxisNo", c_uint32*10),
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Active", c_byte),
        ("CommandAborted", c_byte),
        ("bError", c_byte),
        ("ErrorID", c_uint16)]

class MXP_MULTIAXISCOUPLERESET_IN(Structure):
    _fields_ = [
        ("Execute", c_byte),
        ("ArrayAxisNo", c_uint32*10),
        ("AxisCount", c_uint16)]
class MXP_MULTIAXISCOUPLERESET_OUT(Structure):
    _fields_ = [
        ("ArrayAxisNo", c_uint32*10),
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Active", c_byte),
        ("CommandAborted", c_byte),
        ("bError", c_byte),
        ("ErrorID", c_uint16)]

class MXP_MULTIAXISCOUPLE_SINGLEAXISGAIN(Structure):
    _fields_ = [
        ("FeedForward_V_Gain", c_uint16),
        ("FeedForward_A_Gain", c_uint16),
        ("P_Gain", c_uint16),
        ("I_Gain", c_uint16),
        ("D_Gain", c_uint16)]

class MXP_MULTIAXISCOUPLE_CCCGAIN(Structure):
    _fields_ = [
        ("CCC_Wp", c_uint16),
        ("CCC_Wi", c_uint16)]

class MXP_MULTIAXISCOUPLEGAINSET_IN(Structure):
    _fields_ = [
        ("Execute", c_byte),
        ("ArrayAxisNo", c_uint32*10),
        ("AxisCount", c_uint16),
        ("ArraySingleAxisGain", MXP_MULTIAXISCOUPLE_SINGLEAXISGAIN*10),
        ("ArrayCCCGain", MXP_MULTIAXISCOUPLE_CCCGAIN * 10),
        ("MultiControlKffGain", c_uint16)]

class MXP_MULTIAXISCOUPLEGAINSET_OUT(Structure):
    _fields_ = [
        ("ArrayAxisNo", c_uint32*10),
        ("Done", c_byte),
        ("Busy", c_byte),
        ("Active", c_byte),
        ("CommandAborted", c_byte),
        ("bError", c_byte),
        ("ErrorID", c_uint16)]

MXP_MultiAxisCCCSetCmd = MXPDll['MXP_MultiAxisCCCSetCmd']
MXP_MultiAxisCCCSetCmd.argtype = [c_uint32, POINTER(MXP_MULTIAXISCOUPLESET_IN) ]
MXP_MultiAxisCCCSetCmd.restype = c_int32

MXP_GetMultiAxisCCCSetOutParam = MXPDll['MXP_GetMultiAxisCCCSetOutParam']
MXP_GetMultiAxisCCCSetOutParam.argtype = [c_uint32, POINTER(MXP_MULTIAXISCOUPLESET_OUT) ]
MXP_GetMultiAxisCCCSetOutParam.restype = c_int32

MXP_MultiAxisCCCReSetCmd = MXPDll['MXP_MultiAxisCCCReSetCmd']
MXP_MultiAxisCCCReSetCmd.argtype = [c_uint32, POINTER(MXP_MULTIAXISCOUPLERESET_IN) ]
MXP_MultiAxisCCCReSetCmd.restype = c_int32

MXP_GetMultiAxisCCCReSetOutParam = MXPDll['MXP_GetMultiAxisCCCReSetOutParam']
MXP_GetMultiAxisCCCReSetOutParam.argtype = [c_uint32, POINTER(MXP_MULTIAXISCOUPLERESET_OUT) ]
MXP_GetMultiAxisCCCReSetOutParam.restype = c_int32


MXP_MultiAxisCCCGainSetCmd = MXPDll['MXP_MultiAxisCCCGainSetCmd']
MXP_MultiAxisCCCGainSetCmd.argtype = [c_uint32, POINTER(MXP_MULTIAXISCOUPLEGAINSET_IN) ]
MXP_MultiAxisCCCGainSetCmd.restype = c_int32

MXP_GetMultiAxisCCCGainSetOutParam = MXPDll['MXP_GetMultiAxisCCCGainSetOutParam']
MXP_GetMultiAxisCCCGainSetOutParam.argtype = [c_uint32, POINTER(MXP_MULTIAXISCOUPLEGAINSET_OUT) ]
MXP_GetMultiAxisCCCGainSetOutParam.restype = c_int32


MXP_ReadAxisBufferInfo = MXPDll['MXP_ReadAxisBufferInfo']
MXP_ReadAxisBufferInfo.argtype = [c_uint32, POINTER(c_uint16),POINTER(c_uint16),POINTER(c_uint16)]
MXP_ReadAxisBufferInfo.restype = c_int32

MXP_ReadGroupBufferInfo = MXPDll['MXP_ReadGroupBufferInfo']
MXP_ReadGroupBufferInfo.argtype = [c_uint32, POINTER(c_uint16),POINTER(c_uint16),POINTER(c_uint16)]
MXP_ReadGroupBufferInfo.restype = c_int32

...
#endregion