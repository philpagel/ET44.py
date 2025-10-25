"ET44/E45 series LCR meter"

import sys, time, pyvisa

class ET44:
    "ET44/ET45 series lcr meter"

    # supported test frequencies [Hz]
    _freqrange = {
        "ET4401": (100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000),
        "ET4402": (100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000),
        "ET4410": (100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000, 40000, 50000, 80000, 100000,),
        "ET4501": range(10, 10000),
        "ET4502": range(10, 20000),
        "ET4510": range(10, 100000),
        "RuoShui 4090A": (100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000),
        "RuoShui 4090B": (100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000),
        "RuoShui 4090C": ( 100, 120, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000, 40000, 50000, 80000, 100000,),
        "RuoShui 4091A": range(10, 10000),
        "RuoShui 4091B": range(10, 20000),
        "RuoShui 4091C": range(10, 100000),
    }
    freqrange = None    # set upon initialisation
    # supported voltage levels [mV]
    _voltrange = {
        "ET4401": (100, 300, 600, 1000, 1500, 2000),
        "ET4402": (100, 300, 600, 1000, 1500, 2000),
        "ET4410": (100, 300, 600, 1000, 1500, 2000),
        "ET4501": range(10, 2000),
        "ET4502": range(10, 2000),
        "ET4510": range(10, 2000),
        "RuoShui 4090A": (100, 300, 600, 1000, 1500, 2000),
        "RuoShui 4090B": (100, 300, 600, 1000, 1500, 2000),
        "RuoShui 4090C": (100, 300, 600, 1000, 1500, 2000),
        "RuoShui 4091A": range(10, 2000),
        "RuoShui 4091B": range(10, 2000),
        "RuoShui 4091C": range(10, 2000),
    }
    voltrange = None    # set upon initialisation

    def __init__(
        self,
        RID,
        baudrate=9600,
        eol_r="\r\n",
        eol_w="\r\n",
        delay=0,
        timeout=2000,
        model=None,
    ):
        """
        RID         pyvisa resource ID
        baudrate    must match baudrate set in device (default: 9600)
        eol_r       line terminator for reading from device
        eol_W       line terminator for writing to device
        delay       delay after read/write operation [s]
        timeout     read timeout [ms]
        """
        rm = pyvisa.ResourceManager()
        self.connection = rm.open_resource(RID)
        self.connection.baud_rate = baudrate
        self.connection.query_delay = delay
        self.connection.timeout = timeout
        self.connection.read_termination = eol_r
        self.connection.write_termination = eol_w

        tmp = self.connection.query("*IDN?").split(",")
        self.idn = dict()
        if len(tmp) == 5:
            (
                self.idn["manufacturer"],
                self.idn["model"],
                self.idn["firmware"],
                self.idn["hardware"],
                self.idn["SN"],
            ) = [x.strip() for x in tmp]
        else:
            raise RuntimeError(f"Unable to parse device identification: '{tmp}'")

        # override mdoel string
        if model:
            self.idn["model"] = model

        if self.idn["model"].upper() not in (
            "ET4401",
            "ET4402",
            "ET4410",
            "ET4501",
            "ET4502",
            "ET4510",
            "RuoShui 4090A",
            "RuoShui 4090B",
            "RuoShui 4090C",
            "RuoShui 4091A",
            "RuoShui 4091B",
            "RuoShui 4091C",
        ):
            raise RuntimeError(f"Instrument ID '{self.idn['model']}' not supported.")
        self.freqrange = ET44._freqrange[self.idn["model"]]
        self.voltrange = ET44._voltrange[self.idn["model"]]

    def __del__(self):
        if hasattr(self, "connection"):
            self.connection.close()

    def __str__(self):
        return f"""Model:          {self.idn['model']}
Serial:         {self.idn['SN']}
Firmware:       {self.idn['firmware']}
Hardware:       {self.idn['hardware']}

Voltrange:      {self.voltrange}
Freqrange:      {self.freqrange}

mode:           {self.modeA}, {self.modeB}, {self.SerPar}
speed:          {self.speed}
freq:           {self.freq}
voltage:        {self.volt}
bias:           {self.bias}
"""

    def write(self, command):
        "Write SCPI command to connection and check status"

        ret = self.connection.query(command)
        time.sleep(self.connection.query_delay)
        if ret == "exec success":
            return 0
        elif ret == "cmd err":
            raise RuntimeError(f"Unknown SCPI command '{command}' ('{ret}')")
        elif ret == "execu err":
            raise RuntimeError(f"SCPI command '{command}' failed ('{ret}')")
        else:
            raise RuntimeError(
                f"SCPI command '{command}' returned unknown response ('{ret}')"
            )

    def query(self, command, nrows=1, timeout=None):
        """Write SCPI command to connection and return answer value
        By default, reads 1 line of response.
        If you expect more, you need to set `nrows` to the respective value
        If you expect the respinse to be slow, you can set a ne timout just for
        this request
        """

        if timeout is not None:
            _timeout = self.connection.timeout
            self.connection.timeout = timeout

        self.connection.write(command)
        time.sleep(self.connection.query_delay)
        ret = []
        for i in range(nrows):
            value = self.connection.read()
            time.sleep(self.connection.query_delay)
            ret.append(value)
            if value == "Rcmd err":
                print(f"Command '{command}' failed ({value})", file=sys.stderr)
                return None
        if timeout is not None:
            self.connection.timeout = _timeout
        return ret if len(ret) > 1 else ret[0]

    def close(self):
        "close connection to instument"
        self.connection.close()

    ############################################################
    # Basics

    def beep(self):
        "Sound a beep"
        self.write("SYST:BEEP")

    def trig(self):
        "Send trigger event"
        self.write("*TRG")

    def identify(self):
        "Return instrument identification data"
        return self.query("*IDN?")

    ############################################################
    # Lock/Unlock

    def lock(self):
        "Lock keyboard"
        self.write("SYST:REMote")

    def unlock(self):
        "Unlock keyboard"
        self.write("SYST:LOCAL")

    ############################################################
    # measurement modes

    def setup(
        self,
        modeA=None,
        modeB=None,
        freq=None,
        volt=None,
        bias=None,
        SerPar=None,
        speed=None,
    ):
        "Quick setup method"

        if modeA != None:
            self.modeA = modeA
        if modeB != None:
            self.modeB = modeB
        if SerPar != None:
            self.SerPar = SerPar
        if freq != None:
            self.freq = freq
        if volt != None:
            self.volt = volt
        if bias != None:
            self.bias = bias
        if speed != None:
            self.speed = speed

    @property
    def modeA(self):
        "Primary mode (AUTO | R | C | L | Z | DCR | ECAP)"
        return self.query(f"FUNC:IMP:A?")

    @modeA.setter
    def modeA(self, mode):
        mode = mode.upper()
        modes = (
            "AUTO",
            "R",  # Resistance
            "C",  # Capacitance
            "L",  # Inductance
            "Z",  # Impedance
            "DCR",  # DC Resistance
            "ECAP",  # Electrolytic capacitance
        )
        if mode in modes:
            self.write(f"FUNC:IMP:A {mode}")
        else:
            raise ValueError(f"Mode must be in {modes}")

    @property
    def modeB(self):
        "Secondary mode (X | D | Q | THETA | ESR)"

        ret = self.query(f"FUNC:IMP:B?")
        return "THETA" if ret == "THR" else ret

    @modeB.setter
    def modeB(self, mode):
        mode = mode.upper()
        modes = (
            "X",  # Reactance
            "D",  # Dissipation factor
            "Q",  # Quality factor
            "THETA",  # Phase angle Θ
            "ESR",  # Equivalent series resistance
        )
        if mode in modes:
            mode = "THR" if mode.upper() == "THETA" else mode
            self.write(f"FUNC:IMP:B {mode}")
        else:
            raise ValueError(f"Mode must be in {modes}")

    @property
    def SerPar(self):
        "Equivalent model mode (SER | PAR)"
        mode = self.query(f"FUNC:IMP:EQU?").upper()
        match mode:
            case "SERIAL":
                 mode = "SER"
            case "PALLEL":
                mode = "PAR"
            case _:
                raise RuntimeError(f"Unexpected response: '{mode}'")
        return mode

    @SerPar.setter
    def SerPar(self, mode):
        mode = mode.upper()
        modes = ("SER", "PAR")
        if mode in modes:
            if mode == "PAR":
                mode = "PAL"
            self.write(f"FUNC:IMP:EQU {mode}")
        else:
            raise ValueError(f"Mode must be in {modes}")

    @property
    def speed(self):
        """Speed (FAST | MEDIUM | SLOW)
        Corresponds to 2, 4 or 8 samples/second, respectively.
        Slower = better accuracy
        """
    
        return self.query(f"APERture?").upper()

    @speed.setter
    def speed(self, speed):
        speed = speed.upper()
        speeds = ("FAST", "MEDIUM", "SLOW")
        if speed in speeds:
            self.write(f"APERture {speed}")
        else:
            raise ValueError(f"Speed must be in {speeds}")
    

    ############################################################
    # Voltage and bias (DC offset)

    @property
    def volt(self):
        "Voltage level [mV] for measurement"
        return float(self.query(f"VOLT?"))

    @volt.setter
    def volt(self, V):

        if V in self.voltrange:
            self.write(f"VOLT {int(V)}")
        else:
            raise ValueError(f"V must be in {self.voltrange}mV")

    @property
    def bias(self):
        """DC voltage bias [mV] (0 – 1500)
        aka DC offset
        """
        return float(self.query(f"BIAS:VOLT?"))

    @bias.setter
    def bias(self, bias):

        if 0 <= bias <= 1500:
            self.write(f"BIAS:VOLT {int(bias)}")
        else:
            raise ValueError(f"Bias must be in [0, 1500]mV")


    ############################################################
    # Frequency

    @property
    def freq(self):
        "Measurement frequency [Hz]"
        return float(self.query(f"FREQ?"))

    @freq.setter
    def freq(self, f):
        if f in self.freqrange:
            self.write(f"FREQ {f}")
        else:
            raise ValueError(f"F must be in {self.freqrange}Hz")

    ############################################################
    # Dev/rel mode

    @property
    def rel(self):
        "Relative (delta/dev) mode (ON | OFF)"
        return self.query(f"FUNC:DEV:MODE?").upper()

    @rel.setter
    def rel(self, state):
        state = state.upper()
        if state in ("ON", "OFF"):
            self.write(f"FUNC:DEV:MODE {state}")
        else:
            raise ValueError(f"mode must be in [ON | OFF]")

    ############################################################
    # Range
    # XXX: commented out because non-functional
    # querying auto state works
    # setting auto state does not
    # func:imp:range:val never works for reading/writing

#    @property
#    def range(self):
#        "measurement range (AUTO|30|100|1000|3000|10000|30000|100000)"
#        if self.query(f"FUNC:IMP:RANGE:AUTO?") == "ON":
#            return "AUTO"
#        else:
#            return self.query(f"FUNC:IMP:RANGE:VALUE?")
#
#    @range.setter
#    def range(self, range):
#        ranges = (
#            "AUTO",
#            "30",
#            "100",
#            "300",
#            "1000",
#            "3000",
#            "10000",
#            "30000",
#            "100000",
#        )
#        if range.upper() in ranges:
#            if range.upper() == "AUTO":
#                self.write(f"FUNC:IMP:RANGE:AUTO ON")
#            else:
#                self.write(f"FUNC:IMP:RANGE:AUTO OFF")
#                self.write(f"FUNC:IMP:RANGE:VAL {range}")
#        else:
#            raise ValueError(f"Range must be in {ranges}")

    ############################################################
    # Calibration
    # XXX: not working

#    def cal(self, type):
#        "Calibration (OPEN|SHORT)"
#
#        match type.upper():
#            case "OPEN":
#                self.connection.write("CORR:OPEN:EXEC")
#            case "SHORT":
#                self.connection.write("CORR:SHORT:EXEC")
#            case _:
#                raise ValueError(f"Type must be in (OPEN|SHORT)")

    ############################################################
    # Display switching

    @property
    def display(self):
        "Switch display page (COMP | MEAS | SYS)"
        ret = self.query(f"DISP:PAGE?").upper()
        match ret:
            case "COMPSET":
                ret = "COMP"
            case "MEASUREMENT":
                ret = "MEAS"
            case "SYSTEM":
                ret = "SYS"
            case "STSTEM":
                ret = "SYS"
        return ret

    @display.setter
    def display(self, page):
        page = page.upper()
        if page in ("MEAS", "COMP", "SYS"):
            page = "SYST" if page=="SYS" else page
            self.write(f"DISP:PAGE {page}")
        else:
            raise ValueError(f"Page must be in (MEAS|COMP|SYS)")

    ############################################################
    # Read measurements

    def read(self):
        "Return measurement values (primary, secondary)"

        A, B = self.query("FETCH?").split(",")
        return (float(A), float(B))
