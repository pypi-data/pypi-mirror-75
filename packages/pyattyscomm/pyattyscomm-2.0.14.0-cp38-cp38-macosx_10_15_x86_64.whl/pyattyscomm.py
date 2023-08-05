# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _pyattyscomm
else:
    import _pyattyscomm

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


import weakref

TIMEOUT_IN_SECS = _pyattyscomm.TIMEOUT_IN_SECS

class AttysCommListener(object):
    r"""


    Callback after a sample has arrived. The main class can for example inherit
    class and implement hasSample.  

    C++ includes: AttysCommBase.h

    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def hasSample(self, arg0: "double", arg1: "sample_p") -> "void":
        r"""
        hasSample(AttysCommListener self, double arg0, sample_p arg1)

        Parameters
        ----------
        arg0: double
        arg1: sample_p


        `hasSample(double, sample_p)=0`  

        Provides the timestamp and an array of all channels. This is an abstract method
        and needs to be overloaded with a real method doing the work.  

        """
        return _pyattyscomm.AttysCommListener_hasSample(self, arg0, arg1)
    __swig_destroy__ = _pyattyscomm.delete_AttysCommListener

    def __init__(self):
        r"""
        __init__(AttysCommListener self) -> AttysCommListener

        Parameters
        ----------
        self: PyObject *



        Callback after a sample has arrived. The main class can for example inherit
        class and implement hasSample.  

        C++ includes: AttysCommBase.h

        """
        if self.__class__ == AttysCommListener:
            _self = None
        else:
            _self = self
        _pyattyscomm.AttysCommListener_swiginit(self, _pyattyscomm.new_AttysCommListener(_self, ))
    def __disown__(self):
        self.this.disown()
        _pyattyscomm.disown_AttysCommListener(self)
        return weakref.proxy(self)

# Register AttysCommListener in _pyattyscomm:
_pyattyscomm.AttysCommListener_swigregister(AttysCommListener)

class AttysCommMessage(object):
    r"""


    Callback after an error has occurred. This callback is in particular useful
    after a broken connection has been re-established.  

    C++ includes: AttysCommBase.h

    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def hasMessage(self, arg0: "int", arg1: "char const *") -> "void":
        r"""
        hasMessage(AttysCommMessage self, int arg0, char const * arg1)

        Parameters
        ----------
        arg0: int
        arg1: char const *


        `hasMessage(int, const char *)=0`  

        Provides the error number and a text message about the error.  

        """
        return _pyattyscomm.AttysCommMessage_hasMessage(self, arg0, arg1)
    __swig_destroy__ = _pyattyscomm.delete_AttysCommMessage

    def __init__(self):
        r"""
        __init__(AttysCommMessage self) -> AttysCommMessage

        Parameters
        ----------
        self: PyObject *



        Callback after an error has occurred. This callback is in particular useful
        after a broken connection has been re-established.  

        C++ includes: AttysCommBase.h

        """
        if self.__class__ == AttysCommMessage:
            _self = None
        else:
            _self = self
        _pyattyscomm.AttysCommMessage_swiginit(self, _pyattyscomm.new_AttysCommMessage(_self, ))
    def __disown__(self):
        self.this.disown()
        _pyattyscomm.disown_AttysCommMessage(self)
        return weakref.proxy(self)

# Register AttysCommMessage in _pyattyscomm:
_pyattyscomm.AttysCommMessage_swigregister(AttysCommMessage)

class AttysCommBase(object):
    r"""

    `AttysCommBase()`  

    Platform independent definitions for the Attys  

    Constructors
    ------------
    * `AttysCommBase()`  

        Constructor which is overloaded by AttysComm.  

    Attributes
    ----------
    * `NCHANNELS` : `const int`  
        Total number of channels per samples.  

    * `nMem` : `const int`  
        Number of entries in the ringbuffer. Buffer for 10secs at 1kHz.  

    * `INDEX_Acceleration_X` : `const int`  
        Channel index for X Acceleration.  

    * `INDEX_Acceleration_Y` : `const int`  
        Channel index for Y Acceleration.  

    * `INDEX_Acceleration_Z` : `const int`  
        Channel index for Z Acceleration.  

    * `INDEX_Magnetic_field_X` : `const int`  
        Magnetic field in X direction.  

    * `INDEX_Magnetic_field_Y` : `const int`  
        Magnetic field in Y direction.  

    * `INDEX_Magnetic_field_Z` : `const int`  
        Magnetic field in Z direction.  

    * `INDEX_Analogue_channel_1` : `const int`  
        Index of analogue channel 1.  

    * `INDEX_Analogue_channel_2` : `const int`  
        Index of analogue channel 2.  

    * `INDEX_GPIO0` : `const int`  
        Index of the internal GPIO pin 1.  

    * `INDEX_GPIO1` : `const int`  
        Index of the internal GPIO pin 2.  

    * `ADC_RATE_125HZ` : `const int`  
        Constant defining sampling rate of 125Hz.  

    * `ADC_RATE_250HZ` : `const int`  
        Constant defining sampling rate of 250Hz.  

    * `ADC_RATE_500Hz` : `const int`  
        Constant defining sampling rate of 500Hz (experimental).  

    * `ADC_RATE_1000Hz` : `const int`  
        Constant defining sampling rate of 1000Hz (experimental).  

    * `ADC_DEFAULT_RATE` : `const int`  
        Constant defining the default sampling rate (250Hz).  

    * `ADC_GAIN_6` : `const int`  
        Gain index setting it to gain 6.  

    * `ADC_GAIN_1` : `const int`  
        Gain index setting it to gain 6.  

    * `ADC_GAIN_2` : `const int`  
        Gain index setting it to gain 2.  

    * `ADC_GAIN_3` : `const int`  
        Gain index setting it to gain 3.  

    * `ADC_GAIN_4` : `const int`  
        Gain index setting it to gain 4.  

    * `ADC_GAIN_8` : `const int`  
        Gain index setting it to gain 5.  

    * `ADC_GAIN_12` : `const int`  
        Gain index setting it to gain 6.  

    * `ADC_CURRENT_6NA` : `const int`  
        Bias current of 6nA.  

    * `ADC_CURRENT_22NA` : `const int`  
        Bias current of 22nA.  

    * `ADC_CURRENT_6UA` : `const int`  
        Bias current of 6uA.  

    * `ADC_CURRENT_22UA` : `const int`  
        Bias current of 22uA.  

    * `ADC_MUX_NORMAL` : `const int`  
        Muliplexer routing is normal: ADC1 and ADC2 are connected to the
        sigma/delta.  

    * `ADC_MUX_SHORT` : `const int`  
        Muliplexer routing: inputs are short circuited.  

    * `ADC_MUX_SUPPLY` : `const int`  
        Muliplexer routing: inputs are connected to power supply.  

    * `ADC_MUX_TEMPERATURE` : `const int`  
        Muliplexer routing: ADC measures internal temperature.  

    * `ADC_MUX_TEST_SIGNAL` : `const int`  
        Muliplexer routing: ADC measures test signal.  

    * `ADC_MUX_ECG_EINTHOVEN` : `const int`  
        Muliplexer routing: both positive ADC inputs are connected together.  

    * `ACCEL_2G` : `const int`  
        Setting full scale range of the accelerometer to 2G.  

    * `ACCEL_4G` : `const int`  
        Setting full scale range of the accelerometer to 4G.  

    * `ACCEL_8G` : `const int`  
        Setting full scale range of the accelerometer to 8G.  

    * `ACCEL_16G` : `const int`  
        Setting full scale range of the accelerometer to 16G.  

    * `MESSAGE_CONNECTED` : `const int`  
        Message callback: Connected.  

    * `MESSAGE_ERROR` : `const int`  
        Message callback: Generic error.  

    * `MESSAGE_TIMEOUT` : `const int`  
        Message callback: Reception timeout detected by the watchdog.  

    * `MESSAGE_RECONNECTED` : `const int`  
        Message callback: Managed to reconnect.  

    * `MESSAGE_RECEIVING_DATA` : `const int`  
        Message callback: Receiving data. One off once the connection has been set
        up.  

    * `CHANNEL_DESCRIPTION` : `const std::string`  
        Long descriptions of the channels.  

    * `CHANNEL_SHORT_DESCRIPTION` : `const std::string`  
        Short descriptions of the channels.  

    * `CHANNEL_UNITS` : `std::string const`  
        Units of the channels.  

    * `ADC_SAMPLINGRATE` : `const int`  
        Array of the sampling rates mapping the index to the actual sampling rate.  

    * `ADC_GAIN_FACTOR` : `const int`  
        Mmapping between index and actual gain.  

    * `ADC_REF` : `const float`  
        The voltage reference of the ADC in volts.  

    * `oneG` : `const float`  
        One g in m/s^2.  

    * `ACCEL_FULL_SCALE` : `const float`  
        Mapping of the index to the full scale accelerations.  

    * `MAG_FULL_SCALE` : `const float`  
        Full scale range of the magnetometer in Tesla.  

    * `attysCommMessage` : `AttysCommMessage *`  

    C++ includes: AttysCommBase.h

    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _pyattyscomm.delete_AttysCommBase
    NCHANNELS = _pyattyscomm.AttysCommBase_NCHANNELS
    
    nMem = _pyattyscomm.AttysCommBase_nMem
    
    INDEX_Acceleration_X = _pyattyscomm.AttysCommBase_INDEX_Acceleration_X
    
    INDEX_Acceleration_Y = _pyattyscomm.AttysCommBase_INDEX_Acceleration_Y
    
    INDEX_Acceleration_Z = _pyattyscomm.AttysCommBase_INDEX_Acceleration_Z
    
    INDEX_Magnetic_field_X = _pyattyscomm.AttysCommBase_INDEX_Magnetic_field_X
    
    INDEX_Magnetic_field_Y = _pyattyscomm.AttysCommBase_INDEX_Magnetic_field_Y
    
    INDEX_Magnetic_field_Z = _pyattyscomm.AttysCommBase_INDEX_Magnetic_field_Z
    
    INDEX_Analogue_channel_1 = _pyattyscomm.AttysCommBase_INDEX_Analogue_channel_1
    
    INDEX_Analogue_channel_2 = _pyattyscomm.AttysCommBase_INDEX_Analogue_channel_2
    
    INDEX_GPIO0 = _pyattyscomm.AttysCommBase_INDEX_GPIO0
    
    INDEX_GPIO1 = _pyattyscomm.AttysCommBase_INDEX_GPIO1
    
    CHANNEL_DESCRIPTION = property(_pyattyscomm.AttysCommBase_CHANNEL_DESCRIPTION_get, doc=r"""CHANNEL_DESCRIPTION : a(AttysCommBase::NCHANNELS).q(const).std::string""")
    CHANNEL_SHORT_DESCRIPTION = property(_pyattyscomm.AttysCommBase_CHANNEL_SHORT_DESCRIPTION_get, doc=r"""CHANNEL_SHORT_DESCRIPTION : a(AttysCommBase::NCHANNELS).q(const).std::string""")
    CHANNEL_UNITS = property(_pyattyscomm.AttysCommBase_CHANNEL_UNITS_get, doc=r"""CHANNEL_UNITS : a(AttysCommBase::NCHANNELS).q(const).std::string""")
    ADC_RATE_125HZ = _pyattyscomm.AttysCommBase_ADC_RATE_125HZ
    
    ADC_RATE_250HZ = _pyattyscomm.AttysCommBase_ADC_RATE_250HZ
    
    ADC_RATE_500Hz = _pyattyscomm.AttysCommBase_ADC_RATE_500Hz
    
    ADC_RATE_1000Hz = _pyattyscomm.AttysCommBase_ADC_RATE_1000Hz
    
    ADC_DEFAULT_RATE = _pyattyscomm.AttysCommBase_ADC_DEFAULT_RATE
    
    ADC_SAMPLINGRATE = property(_pyattyscomm.AttysCommBase_ADC_SAMPLINGRATE_get, doc=r"""ADC_SAMPLINGRATE : a(4).q(const).int""")

    def setAdc_samplingrate_index(self, idx: "int") -> "void":
        r"""
        setAdc_samplingrate_index(AttysCommBase self, int idx)

        Parameters
        ----------
        idx: int


        `setAdc_samplingrate_index(int idx)`  

        Sets the sampling rate using the sampling rate index numbers.  

        """
        return _pyattyscomm.AttysCommBase_setAdc_samplingrate_index(self, idx)

    def getSamplingRateInHz(self) -> "int":
        r"""
        getSamplingRateInHz(AttysCommBase self) -> int

        `getSamplingRateInHz() -> int`  

        Gets the sampling rate in Hz (not index number).  

        """
        return _pyattyscomm.AttysCommBase_getSamplingRateInHz(self)

    def getAdc_samplingrate_index(self) -> "int":
        r"""
        getAdc_samplingrate_index(AttysCommBase self) -> int

        `getAdc_samplingrate_index() -> int`  

        Gets the sampling rate in form for the index.  

        """
        return _pyattyscomm.AttysCommBase_getAdc_samplingrate_index(self)
    ADC_GAIN_6 = _pyattyscomm.AttysCommBase_ADC_GAIN_6
    
    ADC_GAIN_1 = _pyattyscomm.AttysCommBase_ADC_GAIN_1
    
    ADC_GAIN_2 = _pyattyscomm.AttysCommBase_ADC_GAIN_2
    
    ADC_GAIN_3 = _pyattyscomm.AttysCommBase_ADC_GAIN_3
    
    ADC_GAIN_4 = _pyattyscomm.AttysCommBase_ADC_GAIN_4
    
    ADC_GAIN_8 = _pyattyscomm.AttysCommBase_ADC_GAIN_8
    
    ADC_GAIN_12 = _pyattyscomm.AttysCommBase_ADC_GAIN_12
    
    ADC_GAIN_FACTOR = property(_pyattyscomm.AttysCommBase_ADC_GAIN_FACTOR_get, doc=r"""ADC_GAIN_FACTOR : a(7).q(const).int""")
    ADC_REF = property(_pyattyscomm.AttysCommBase_ADC_REF_get, doc=r"""ADC_REF : q(const).float""")

    def getADCFullScaleRange(self, channel: "int") -> "float":
        r"""
        getADCFullScaleRange(AttysCommBase self, int channel) -> float

        Parameters
        ----------
        channel: int


        `getADCFullScaleRange(int channel) -> float`  

        Gets the ADC full range. This depends on the gain setting of the ADC.  

        """
        return _pyattyscomm.AttysCommBase_getADCFullScaleRange(self, channel)

    def setAdc0_gain_index(self, idx: "int") -> "void":
        r"""
        setAdc0_gain_index(AttysCommBase self, int idx)

        Parameters
        ----------
        idx: int


        `setAdc0_gain_index(int idx)`  

        Gets the gain index for ADC1.  

        """
        return _pyattyscomm.AttysCommBase_setAdc0_gain_index(self, idx)

    def setAdc1_gain_index(self, idx: "int") -> "void":
        r"""
        setAdc1_gain_index(AttysCommBase self, int idx)

        Parameters
        ----------
        idx: int


        `setAdc1_gain_index(int idx)`  

        Gets the gain index for ADC2.  

        """
        return _pyattyscomm.AttysCommBase_setAdc1_gain_index(self, idx)
    ADC_CURRENT_6NA = _pyattyscomm.AttysCommBase_ADC_CURRENT_6NA
    
    ADC_CURRENT_22NA = _pyattyscomm.AttysCommBase_ADC_CURRENT_22NA
    
    ADC_CURRENT_6UA = _pyattyscomm.AttysCommBase_ADC_CURRENT_6UA
    
    ADC_CURRENT_22UA = _pyattyscomm.AttysCommBase_ADC_CURRENT_22UA
    

    def setBiasCurrent(self, currIndex: "int") -> "void":
        r"""
        setBiasCurrent(AttysCommBase self, int currIndex)

        Parameters
        ----------
        currIndex: int


        `setBiasCurrent(int currIndex)`  

        Sets the bias current which can be switched on.  

        """
        return _pyattyscomm.AttysCommBase_setBiasCurrent(self, currIndex)

    def getBiasCurrent(self) -> "int":
        r"""
        getBiasCurrent(AttysCommBase self) -> int

        `getBiasCurrent() -> int`  

        Gets the bias current as in index.  

        """
        return _pyattyscomm.AttysCommBase_getBiasCurrent(self)

    def enableCurrents(self, pos_ch1: "int", neg_ch1: "int", pos_ch2: "int") -> "void":
        r"""
        enableCurrents(AttysCommBase self, int pos_ch1, int neg_ch1, int pos_ch2)

        Parameters
        ----------
        pos_ch1: int
        neg_ch1: int
        pos_ch2: int


        `enableCurrents(int pos_ch1, int neg_ch1, int pos_ch2)`  

        Switches bias currents on  

        """
        return _pyattyscomm.AttysCommBase_enableCurrents(self, pos_ch1, neg_ch1, pos_ch2)
    ADC_MUX_NORMAL = _pyattyscomm.AttysCommBase_ADC_MUX_NORMAL
    
    ADC_MUX_SHORT = _pyattyscomm.AttysCommBase_ADC_MUX_SHORT
    
    ADC_MUX_SUPPLY = _pyattyscomm.AttysCommBase_ADC_MUX_SUPPLY
    
    ADC_MUX_TEMPERATURE = _pyattyscomm.AttysCommBase_ADC_MUX_TEMPERATURE
    
    ADC_MUX_TEST_SIGNAL = _pyattyscomm.AttysCommBase_ADC_MUX_TEST_SIGNAL
    
    ADC_MUX_ECG_EINTHOVEN = _pyattyscomm.AttysCommBase_ADC_MUX_ECG_EINTHOVEN
    

    def setAdc0_mux_index(self, idx: "int") -> "void":
        r"""
        setAdc0_mux_index(AttysCommBase self, int idx)

        Parameters
        ----------
        idx: int


        `setAdc0_mux_index(int idx)`  

        """
        return _pyattyscomm.AttysCommBase_setAdc0_mux_index(self, idx)

    def setAdc1_mux_index(self, idx: "int") -> "void":
        r"""
        setAdc1_mux_index(AttysCommBase self, int idx)

        Parameters
        ----------
        idx: int


        `setAdc1_mux_index(int idx)`  

        """
        return _pyattyscomm.AttysCommBase_setAdc1_mux_index(self, idx)

    @staticmethod
    def phys2temperature(volt: "float") -> "float":
        r"""
        phys2temperature(float volt) -> float

        Parameters
        ----------
        volt: float


        `phys2temperature(float volt) -> float`  

        Temperature  

        """
        return _pyattyscomm.AttysCommBase_phys2temperature(volt)
    ACCEL_2G = _pyattyscomm.AttysCommBase_ACCEL_2G
    
    ACCEL_4G = _pyattyscomm.AttysCommBase_ACCEL_4G
    
    ACCEL_8G = _pyattyscomm.AttysCommBase_ACCEL_8G
    
    ACCEL_16G = _pyattyscomm.AttysCommBase_ACCEL_16G
    
    oneG = property(_pyattyscomm.AttysCommBase_oneG_get, doc=r"""oneG : q(const).float""")
    ACCEL_FULL_SCALE = property(_pyattyscomm.AttysCommBase_ACCEL_FULL_SCALE_get, doc=r"""ACCEL_FULL_SCALE : a(4).q(const).float""")

    def getAccelFullScaleRange(self) -> "float":
        r"""
        getAccelFullScaleRange(AttysCommBase self) -> float

        `getAccelFullScaleRange() -> float`  

        Returns the accelerometer current full scale reading in m/s^2.  

        """
        return _pyattyscomm.AttysCommBase_getAccelFullScaleRange(self)

    def setAccel_full_scale_index(self, idx: "int") -> "void":
        r"""
        setAccel_full_scale_index(AttysCommBase self, int idx)

        Parameters
        ----------
        idx: int


        `setAccel_full_scale_index(int idx)`  

        Sets the accelerometer full scale range using the index.  

        """
        return _pyattyscomm.AttysCommBase_setAccel_full_scale_index(self, idx)
    MAG_FULL_SCALE = property(_pyattyscomm.AttysCommBase_MAG_FULL_SCALE_get, doc=r"""MAG_FULL_SCALE : q(const).float""")

    def getMagFullScaleRange(self) -> "float":
        r"""
        getMagFullScaleRange(AttysCommBase self) -> float

        `getMagFullScaleRange() -> float`  

        Returns the full scale magnetometer in Tesla.  

        """
        return _pyattyscomm.AttysCommBase_getMagFullScaleRange(self)

    def getIsCharging(self) -> "int":
        r"""
        getIsCharging(AttysCommBase self) -> int

        `getIsCharging() -> int`  

        Charging indicator. Returns one if charging.  

        """
        return _pyattyscomm.AttysCommBase_getIsCharging(self)
    MESSAGE_CONNECTED = _pyattyscomm.AttysCommBase_MESSAGE_CONNECTED
    
    MESSAGE_ERROR = _pyattyscomm.AttysCommBase_MESSAGE_ERROR
    
    MESSAGE_TIMEOUT = _pyattyscomm.AttysCommBase_MESSAGE_TIMEOUT
    
    MESSAGE_RECONNECTED = _pyattyscomm.AttysCommBase_MESSAGE_RECONNECTED
    
    MESSAGE_RECEIVING_DATA = _pyattyscomm.AttysCommBase_MESSAGE_RECEIVING_DATA
    

    def connect(self) -> "void":
        r"""
        connect(AttysCommBase self)

        `connect()=0`  

        Connects to the Attys by opening the socket. Throws char* exception if it fails.  

        """
        return _pyattyscomm.AttysCommBase_connect(self)

    def start(self) -> "void":
        r"""
        start(AttysCommBase self)

        `start()`  

        Starts the data acquisition by starting the main thread. and sending possibly
        init commands.  

        """
        return _pyattyscomm.AttysCommBase_start(self)

    def closeSocket(self) -> "void":
        r"""
        closeSocket(AttysCommBase self)

        `closeSocket()=0`  

        Closes the socket safely.  

        """
        return _pyattyscomm.AttysCommBase_closeSocket(self)

    def hasActiveConnection(self) -> "int":
        r"""
        hasActiveConnection(AttysCommBase self) -> int

        `hasActiveConnection() -> int`  

        Returns one if the connection is active.  

        """
        return _pyattyscomm.AttysCommBase_hasActiveConnection(self)

    def getSampleFromBuffer(self) -> "sample_p":
        r"""
        getSampleFromBuffer(AttysCommBase self) -> sample_p

        `getSampleFromBuffer() -> sample_p`  

        Gets a sample from the ringbuffer. This is a float* array of all channels.  

        """
        return _pyattyscomm.AttysCommBase_getSampleFromBuffer(self)

    def hasSampleAvailable(self) -> "int":
        r"""
        hasSampleAvailable(AttysCommBase self) -> int

        `hasSampleAvailable() -> int`  

        Is set to one if samples are available in the ringbuffer.  

        """
        return _pyattyscomm.AttysCommBase_hasSampleAvailable(self)

    def resetRingbuffer(self) -> "void":
        r"""
        resetRingbuffer(AttysCommBase self)

        `resetRingbuffer()`  

        Resets the ringbuffer to zero content.  

        """
        return _pyattyscomm.AttysCommBase_resetRingbuffer(self)

    def registerCallback(self, f: "AttysCommListener") -> "void":
        r"""
        registerCallback(AttysCommBase self, AttysCommListener f)

        Parameters
        ----------
        f: AttysCommListener *


        `registerCallback(AttysCommListener *f)`  

        Register a realtime callback function which is called whenever a sample has
        arrived. AttysCommListener is an abstract class which needs to implement
        hasSample().  

        """
        return _pyattyscomm.AttysCommBase_registerCallback(self, f)

    def unregisterCallback(self) -> "void":
        r"""
        unregisterCallback(AttysCommBase self)

        `unregisterCallback()`  

        Unregister the realtime sample callback.  

        """
        return _pyattyscomm.AttysCommBase_unregisterCallback(self)

    def registerMessageCallback(self, f: "AttysCommMessage") -> "void":
        r"""
        registerMessageCallback(AttysCommBase self, AttysCommMessage f)

        Parameters
        ----------
        f: AttysCommMessage *


        `registerMessageCallback(AttysCommMessage *f)`  

        Callback which is called whenever a special error/event has occurred.  

        """
        return _pyattyscomm.AttysCommBase_registerMessageCallback(self, f)

    def unregisterMessageCallback(self) -> "void":
        r"""
        unregisterMessageCallback(AttysCommBase self)

        `unregisterMessageCallback()`  

        Unregister the error/event callback.  

        """
        return _pyattyscomm.AttysCommBase_unregisterMessageCallback(self)

    def quit(self) -> "void":
        r"""
        quit(AttysCommBase self)

        `quit()`  

        Call this from the main activity to shut down the connection.  

        """
        return _pyattyscomm.AttysCommBase_quit(self)

    def getBluetoothBinaryAdress(self) -> "unsigned char *":
        r"""
        getBluetoothBinaryAdress(AttysCommBase self) -> unsigned char *

        `getBluetoothBinaryAdress()=0 -> unsigned char *`  

        Returns an array of 14 bytes of the bluetooth address.  

        """
        return _pyattyscomm.AttysCommBase_getBluetoothBinaryAdress(self)

    def getBluetoothAdressString(self, s: "char *") -> "void":
        r"""
        getBluetoothAdressString(AttysCommBase self, char * s)

        Parameters
        ----------
        s: char *


        `getBluetoothAdressString(char *s)=0`  

        returns the MAC address as a string.  

        """
        return _pyattyscomm.AttysCommBase_getBluetoothAdressString(self, s)

    def getAttysName(self) -> "char *":
        r"""
        getAttysName(AttysCommBase self) -> char *

        `getAttysName() -> char *`  

        Returns the name of the Attys  

        """
        return _pyattyscomm.AttysCommBase_getAttysName(self)

    def setAttysName(self, s: "char *") -> "void":
        r"""
        setAttysName(AttysCommBase self, char * s)

        Parameters
        ----------
        s: char *


        `setAttysName(char *s)`  

        Sets the name of the Attys  

        """
        return _pyattyscomm.AttysCommBase_setAttysName(self, s)

    def processRawAttysData(self, data: "char const *") -> "void":
        r"""
        processRawAttysData(AttysCommBase self, char const * data)

        Parameters
        ----------
        data: char const *


        `processRawAttysData(const char *data)`  

        """
        return _pyattyscomm.AttysCommBase_processRawAttysData(self, data)

    def isInitialising(self) -> "int":
        r"""
        isInitialising(AttysCommBase self) -> int

        `isInitialising() -> int`  

        """
        return _pyattyscomm.AttysCommBase_isInitialising(self)

    def setConnected(self, c: "int") -> "void":
        r"""
        setConnected(AttysCommBase self, int c)

        Parameters
        ----------
        c: int


        `setConnected(int c)`  

        """
        return _pyattyscomm.AttysCommBase_setConnected(self, c)
    attysCommMessage = property(_pyattyscomm.AttysCommBase_attysCommMessage_get, _pyattyscomm.AttysCommBase_attysCommMessage_set, doc=r"""attysCommMessage : p.AttysCommMessage""")

# Register AttysCommBase in _pyattyscomm:
_pyattyscomm.AttysCommBase_swigregister(AttysCommBase)

def AttysCommBase_phys2temperature(volt: "float") -> "float":
    r"""
    AttysCommBase_phys2temperature(float volt) -> float

    Parameters
    ----------
    volt: float


    `phys2temperature(float volt) -> float`  

    Temperature  

    """
    return _pyattyscomm.AttysCommBase_phys2temperature(volt)


def Base64encode_len(len: "int") -> "int":
    r"""
    Base64encode_len(int len) -> int

    Parameters
    ----------
    len: int

    """
    return _pyattyscomm.Base64encode_len(len)

def Base64encode(coded_dst: "char *", plain_src: "char const *", len_plain_src: "int") -> "__int64":
    r"""
    Base64encode(char * coded_dst, char const * plain_src, int len_plain_src) -> __int64

    Parameters
    ----------
    coded_dst: char *
    plain_src: char const *
    len_plain_src: int

    """
    return _pyattyscomm.Base64encode(coded_dst, plain_src, len_plain_src)

def Base64decode_len(coded_src: "char const *") -> "__int64":
    r"""
    Base64decode_len(char const * coded_src) -> __int64

    Parameters
    ----------
    coded_src: char const *

    """
    return _pyattyscomm.Base64decode_len(coded_src)

def Base64decode(plain_dst: "char *", coded_src: "char const *") -> "__int64":
    r"""
    Base64decode(char * plain_dst, char const * coded_src) -> __int64

    Parameters
    ----------
    plain_dst: char *
    coded_src: char const *

    """
    return _pyattyscomm.Base64decode(plain_dst, coded_src)
class AttysComm(AttysCommBase):
    r"""

    `AttysComm(void *_btAddr=NULL, int _btAddrLen=0)`  

    AttysComm contains all the neccessary comms to talk to the Attys on Linux,
    Windows and Mac.   AttysComm class contains the device specific definitions and
    implements the abstract classes of AttysCommBase. See AttysCommBase for the
    definitions there. Instances of this class are automatically created by
    AttysScan and the user can ignore definitions here. All relevant user functions
    are in AttysCommBase. Use this class only if you have a fixed bluetooth address
    (Linux/Win) or a fixed bluetooth device (Mac) and won't need to scan for a
    bluetooth device.  

    Constructors
    ------------
    * `AttysComm(void *_btAddr=NULL, int _btAddrLen=0)`  

        Constructor: Win/Linux: takes the bluetooth device structure and its length
        as an argument. For Mac: just a pointer to the bluetooth device (needs
        typecast to *_btAddr) and provide no length.  

    C++ includes: AttysComm.h

    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, _btAddr: "void *"=None, _btAddrLen: "int"=0):
        r"""
        __init__(AttysComm self, void * _btAddr=None, int _btAddrLen=0) -> AttysComm

        Parameters
        ----------
        _btAddr: void *
        _btAddrLen: int


        `AttysComm(void *_btAddr=NULL, int _btAddrLen=0)`  

        Constructor: Win/Linux: takes the bluetooth device structure and its length as
        an argument. For Mac: just a pointer to the bluetooth device (needs typecast to
        *_btAddr) and provide no length.  

        """
        _pyattyscomm.AttysComm_swiginit(self, _pyattyscomm.new_AttysComm(_btAddr, _btAddrLen))

    def connect(self) -> "void":
        r"""
        connect(AttysComm self)

        `connect()`  

        Connects to the Attys by opening the socket. Throws char* exception if it fails.  

        """
        return _pyattyscomm.AttysComm_connect(self)

    def closeSocket(self) -> "void":
        r"""
        closeSocket(AttysComm self)

        `closeSocket()`  

        Closes the socket safely.  

        """
        return _pyattyscomm.AttysComm_closeSocket(self)

    def run(self) -> "void":
        r"""
        run(AttysComm self)

        `run()`  

        Thread which does the data acquisition. Do not call directly.  

        """
        return _pyattyscomm.AttysComm_run(self)

    def quit(self) -> "void":
        r"""
        quit(AttysComm self)

        `quit()`  

        Call this from the main activity to shut down the connection.  

        """
        return _pyattyscomm.AttysComm_quit(self)

    def sendSyncCommand(self, message: "char const *", waitForOK: "int") -> "void":
        r"""
        sendSyncCommand(AttysComm self, char const * message, int waitForOK)

        Parameters
        ----------
        message: char const *
        waitForOK: int


        `sendSyncCommand(const char *message, int waitForOK)`  

        Sends a command to the Attys. Do not use unless you know exactly what you are
        doing.  

        """
        return _pyattyscomm.AttysComm_sendSyncCommand(self, message, waitForOK)

    def sendInit(self) -> "void":
        r"""
        sendInit(AttysComm self)

        `sendInit()`  

        Sends the init sequence to the Attys. Do not use unless you know exactly what
        you are doing.  

        """
        return _pyattyscomm.AttysComm_sendInit(self)

    def start(self) -> "void":
        r"""
        start(AttysComm self)

        `start()`  

        Starts the data acquisition by starting the main thread. and sending possibly
        init commands.  

        """
        return _pyattyscomm.AttysComm_start(self)

    def receptionTimeout(self) -> "void":
        r"""
        receptionTimeout(AttysComm self)

        `receptionTimeout()`  

        Called from the watchdog after a timeout. Do not call this directly.  

        """
        return _pyattyscomm.AttysComm_receptionTimeout(self)

    def getBluetoothBinaryAdress(self) -> "unsigned char *":
        r"""
        getBluetoothBinaryAdress(AttysComm self) -> unsigned char *

        `getBluetoothBinaryAdress() -> unsigned char *`  

        Returns an array of 14 bytes of the bluetooth address.  

        """
        return _pyattyscomm.AttysComm_getBluetoothBinaryAdress(self)

    def getBluetoothAdressString(self, s: "char *") -> "void":
        r"""
        getBluetoothAdressString(AttysComm self, char * s)

        Parameters
        ----------
        s: char *


        `getBluetoothAdressString(char *s)`  

        returns the MAC address as a string.  

        """
        return _pyattyscomm.AttysComm_getBluetoothAdressString(self, s)
    __swig_destroy__ = _pyattyscomm.delete_AttysComm

# Register AttysComm in _pyattyscomm:
_pyattyscomm.AttysComm_swigregister(AttysComm)

class AttysScanListener(object):
    r"""


    Callback which reports the status of the scanner  

    C++ includes: AttysScan.h

    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    __swig_destroy__ = _pyattyscomm.delete_AttysScanListener

    def message(self, arg0: "int const", arg1: "char const *") -> "void":
        r"""
        message(AttysScanListener self, int const arg0, char const * arg1)

        Parameters
        ----------
        arg0: int const
        arg1: char const *


        `message(const int, const char *)=0`  

        """
        return _pyattyscomm.AttysScanListener_message(self, arg0, arg1)

    def __init__(self):
        r"""
        __init__(AttysScanListener self) -> AttysScanListener

        Parameters
        ----------
        self: PyObject *



        Callback which reports the status of the scanner  

        C++ includes: AttysScan.h

        """
        if self.__class__ == AttysScanListener:
            _self = None
        else:
            _self = self
        _pyattyscomm.AttysScanListener_swiginit(self, _pyattyscomm.new_AttysScanListener(_self, ))
    def __disown__(self):
        self.this.disown()
        _pyattyscomm.disown_AttysScanListener(self)
        return weakref.proxy(self)

# Register AttysScanListener in _pyattyscomm:
_pyattyscomm.AttysScanListener_swigregister(AttysScanListener)
cvar = _pyattyscomm.cvar

class AttysScan(object):
    r"""


    Scans for Attys and creates instances of AttysComm for every detected/paired
    Attys. There is no need to create instances of AttysComm yourself. This is done
    by this class automatically.  

    Attributes
    ----------
    * `SCAN_CONNECTED` : `const int`  
        Message index that the connection to an attys has been successful.  

    * `SCAN_SEARCHING` : `const int`  
        Message index that AttysScan is actively scanning  

    * `SCAN_NODEV` : `const int`  
        Message index that no Attys has been detected  

    * `SCAN_SOCKETERR` : `const int`  
        Message that the socket could not be opened  

    * `SCAN_CONNECTING` : `const int`  
        In the process of connecting  

    * `SCAN_CONNECTERR` : `const int`  
        Connection error during scanning  

    * `MAX_ATTYS_DEVS` : `const int`  
        Max number of Attys Devices  

    C++ includes: AttysScan.h

    """

    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    __swig_destroy__ = _pyattyscomm.delete_AttysScan

    def scan(self, maxAttys: "int"=1) -> "int":
        r"""
        scan(AttysScan self, int maxAttys=1) -> int

        Parameters
        ----------
        maxAttys: int


        `scan(int maxAttys=1) -> int`  

        Scans for the specified number of devices and connects to them. By default only
        for one Attys. returns 0 on success  

        """
        return _pyattyscomm.AttysScan_scan(self, maxAttys)
    SCAN_CONNECTED = _pyattyscomm.AttysScan_SCAN_CONNECTED
    
    SCAN_SEARCHING = _pyattyscomm.AttysScan_SCAN_SEARCHING
    
    SCAN_NODEV = _pyattyscomm.AttysScan_SCAN_NODEV
    
    SCAN_SOCKETERR = _pyattyscomm.AttysScan_SCAN_SOCKETERR
    
    SCAN_CONNECTING = _pyattyscomm.AttysScan_SCAN_CONNECTING
    
    SCAN_CONNECTERR = _pyattyscomm.AttysScan_SCAN_CONNECTERR
    
    MAX_ATTYS_DEVS = _pyattyscomm.AttysScan_MAX_ATTYS_DEVS
    

    def registerCallback(self, f: "AttysScanListener") -> "void":
        r"""
        registerCallback(AttysScan self, AttysScanListener f)

        Parameters
        ----------
        f: AttysScanListener *


        `registerCallback(AttysScanListener *f)`  

        Register callback which reports the scanning progress for example for a splash
        screen.  

        """
        return _pyattyscomm.AttysScan_registerCallback(self, f)

    def unregisterCallback(self) -> "void":
        r"""
        unregisterCallback(AttysScan self)

        `unregisterCallback()`  

        Unregisters the callback  

        """
        return _pyattyscomm.AttysScan_unregisterCallback(self)

    def getAttysComm(self, i: "int") -> "AttysComm *":
        r"""
        getAttysComm(AttysScan self, int i) -> AttysComm

        Parameters
        ----------
        i: int


        `getAttysComm(int i) -> AttysComm *`  

        Obtains the pointer to a valid AttysComm class which has been successfully
        detected while scanning.  

        """
        return _pyattyscomm.AttysScan_getAttysComm(self, i)

    def getAttysName(self, i: "int") -> "char *":
        r"""
        getAttysName(AttysScan self, int i) -> char *

        Parameters
        ----------
        i: int


        `getAttysName(int i) -> char *`  

        Gets the Attys name as reported by the bluetooth manager  

        """
        return _pyattyscomm.AttysScan_getAttysName(self, i)

    def getNAttysDevices(self) -> "int":
        r"""
        getNAttysDevices(AttysScan self) -> int

        `getNAttysDevices() -> int`  

        Returns the number of Attys devices  

        """
        return _pyattyscomm.AttysScan_getNAttysDevices(self)

    def __init__(self):
        r"""
        __init__(AttysScan self) -> AttysScan


        Scans for Attys and creates instances of AttysComm for every detected/paired
        Attys. There is no need to create instances of AttysComm yourself. This is done
        by this class automatically.  

        Attributes
        ----------
        * `SCAN_CONNECTED` : `const int`  
            Message index that the connection to an attys has been successful.  

        * `SCAN_SEARCHING` : `const int`  
            Message index that AttysScan is actively scanning  

        * `SCAN_NODEV` : `const int`  
            Message index that no Attys has been detected  

        * `SCAN_SOCKETERR` : `const int`  
            Message that the socket could not be opened  

        * `SCAN_CONNECTING` : `const int`  
            In the process of connecting  

        * `SCAN_CONNECTERR` : `const int`  
            Connection error during scanning  

        * `MAX_ATTYS_DEVS` : `const int`  
            Max number of Attys Devices  

        C++ includes: AttysScan.h

        """
        _pyattyscomm.AttysScan_swiginit(self, _pyattyscomm.new_AttysScan())

# Register AttysScan in _pyattyscomm:
_pyattyscomm.AttysScan_swigregister(AttysScan)



