# ET44

Python class for remote controlling EastTester ET44 and ET45 series lcr meters:
ET4401, ET4402, ET4410, ET4501, ET4502, ET4510.


# Status

[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

This should work fine with all devices of the ET44/ET45 series as listed above.
However, I only have a ET4410 and no way of testing this on the other devices.


| Feature                       | Status |
|-------------------------------|------- |
| Primary modes R,C,L,DCR,ECAP  |   ✓    |
| Secondary modes X,D,Q,THR,ESR |   ✓    |
| Ser/Par equivalent            |   ✓    |
| Read measurement values       |   ✓    |
| Signal voltage level          |   ✓    |
| Bias (DC offset)              |   ✓    |
| Measurement speed             |   ✓    |
| Relative mode                 |   ✓    |
| Lock/unlock                   |   ✓    |
| Display options               |   ✓    |
| Comparator mode               |   –    |
| Open/short calibration        |  ???   |
| get/set range                 |  ???   |
| output impedance              |  ???   |
| List scanning                 |  ???   |
| min/max/avg                   |  ???   |

Legend:

* `✓`: Implemented and working
* `–` : not implemented
* `???` : Not clear if this is possible / does not work as described in SCPI manual


# In a Nutshell

Here is a little example script that illustrates how things work:

```{python}
#!/bin/env python3
from ET44 import ET44

# connect to the device
lcr = ET44("ASRL/dev/ttyACM0::INSTR")

# configure the device
lcr.setup(
    modeA="C", 
    modeB="Q", 
    freq=100, 
    volt=500, 
    bias=0,
    serpar="SER", 
    speed="Slow"
    )

# take a measurement
C1, ESR1 = lcr.read()

# Change the frequency to 10kHz
lcr.freq = 10000

# measure again
C2, ESR2 = lcr.read()


```


# Installation

1. Download the latest release package (` et44-XXX.tar.gz `) from github.
2. If you want to install in a virtual environment, first, create and activate it:
```
python -m venv .venv
source .venv/bin/activate
```
3. Install the package (replace *XXX* with the correct number)
```
python -m pip install et44-XXX.tar.gz
```


# Reference

The following sections give a tour of available functionality.  Detailed
api-documentation is given in the doc-strings of the classes. Use `pydoc` to
access it:

    python -m pydoc ET44
    python -m pydoc ET44.instrument

For questions about valid values for all commands and general use of the
device, please refer to the manufacturers *user manual* and/or *scpi manual*.


## Connecting
    
This is how you connect to the device:

    from ET44 import ET44
    lcr = ET44("ASRL/dev/ttyACM0::INSTR")

Or, on windows:

    from ET44 import ET44
    lcr = ET44("ASRL2::INSTR")

Of course, you need to adapt it to the right device for your case.
See [here](https://pyvisa.readthedocs.io/en/1.8/names.html) for details on
pyvisa resource names.


## basic commands
    
Send a trigger event

    lcr.trig()

Get the identification data

    lcr.identify()

Print device and status information

    print(lcr)

Sound a beep

    lcr.beep()
    
Lock the keypad
    
    lcr.lock()

And unlock it again
    
    lcr.unlock()

You can also send raw SCPI commands to the device. There are
two different comands for that: `write` and `query`. The former will
send a command and check the status, the latter returns the data returned by
the device:

    # set voltage level to 500mV:
    lcr.write("VOLT: 500")
    
    # query voltage level
    lcr.query("VOLT?")


## Configuring the device

In order to configure the device, you need to set the following paramters:

* *modeA*: primary parameter (R | C | L | Z | DCR | ECAP | AUTO)
* *modeB*: secondary paramter (X | D | Q | Θ | ESR)
* *Serpar*: equivalent model (SER | PAR)
* *signal voltage*
* DC *bias* (= DC offset)
* Measurement *speed*

You can set each of these parameters separately, or all at once (using the
`setup` method).


### Primary mode

The primary mode sets the type of component/parameter you want to measure. The
following modes are supported:

| Mode | Description                                                           |
|------|-----------------------------------------------------------------------|
| AUTO | Automatically detect type fromn connected component. Not recommended. |
| R    | Resistance                                                            |
| C    | Capacitance                                                           |
| L    | Inductance                                                            |
| Z    | Impedance                                                             |
| DCR  | DC resistance                                                         |
| ECAP | Capacitance of electrolytic capacitors                                |

To get/set the primary mode, use the `modeA` method:

    # print current mode
    print(lcr.modeA)

    # set to resistance
    lcr.modeA = "R"

    # set to capacitance
    lcr.modeA = "r"

**Caution:** When set to `AUTO`, you cannot set `modeB` or `SerPar` – the
device will return an error when you try that. But that's not a big deal
because using `Auto` mode doesn't not make much sense in a remot control
scenario, to begin with.


### Secondary mode

The secondary mode sets the secondary parameter you want to measure. The following
modes are supported:

| Mode  | Description                     |
|-------|---------------------------------|
| X     | Reactance                       |
| D     | Dissipation factor              |
| Q     | Quality factor                  |
| Theta | Phase angle Θ                   |
| ESR   | Equivalent series resistance    |

To get/set the secondary mode, use the `modeB` method:

    # print current mode
    print(lcr.modeB)

    # set to ESR
    lcr.modeA = "ESR"

    # set to phase angle
    lcr.modeA = "theta"


### Series/parallel equivalent model

So get/set the series or parallel equivalent model for measurement use the
`Serpar` method:


    # print current mode
    print(lcr.Serpar)

    # set to series
    lcr.SerPar = "Ser"

    # set to parallel
    lcr.SerPar = "PAR"


### Voltage level and bias

You can set signal voltage in the range supported by your specific device.  The
ER44xx models support 6 discrete values (100, 300, 600, 1000, 1500 and 2000V),
while the ET45xx models will accept any integer value in the range [10, 2000]mV.

To get/set the voltage use the `volt` method:

    # show the voltage range supported by your device
    print(lcr._voltrange)

    # print signal voltage
    print(lcr.volt)

    # set voltage to 1V
    lcr.volt = 1000

    # set voltage to 0.6V
    lcr.volt = 600

A DC bias (aka DC offset) in the range [0, 1500]mV can be added to the signal –
e.g. to ensure strictly positive voltage across the component during
measurement. Use the `bias` method to get/set the DC bias:

    # print bias
    print(lcr.bias)

    # set bias o 1V
    lcr.bias = 1000

    # set bias 0.5V
    lcr.volt = 500


### Frequency

Measurement frequency can be set in a range that depends on your specific model:

| Model   | Frequency Range [Hz]                               |
|---------|----------------------------------------------------|
| ET4401  | 100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000  |
| ET4402  | 100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000
| ET4410  | 100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 15000, 20000, 80000, 100000 |
| ET4501  | 10 – 10000                                         |
| ET4502  | 10 – 20000                                         |
| ET4510  | 10 – 100000                                        |

In order to get/set the measurement frequency, use the `freq` method:

    
    # show the frequency range supported by your device
    print(lcr._freqrange)
   
    # print frequency
    print(lcr.freq)

    # set frequency to 10Hz
    lcr.freq = 100

    # set frequency to 10kHz
    lcr.freq = 10000

### Measurement Speed

To get/set the measurement speed, use the `speed` method. Valid modes are `FAST`,
`MED` and `Slow`:

    # print current mode
    print(lcr.speed)

    # set to slow
    lcr.speed = "slow"

    # set to fast
    lcr.speed = "FasT"

Speed is inversely correlated with accuracy. So unless you are in a hurry,
`slow` mode is recommended.


### Relative (Dev) mode

By activating relative mode, the instrument will display/return relative
measurements with respect to the value measured at the time *rel* mode was
activated. To get/set rel mode, use the `rel` method:

    # print current mode
    print(lcr.rel)

    # set rel
    lcr.rel = "ON"

    # return to normal mode
    lcr.rel = "off"


### Quick setup

To set all measurement parameters at once, you can use the `setup method`. The
function accepts all of the setup parameters in single function call and you
can either provide them in the order `modeA, modeB, freq, voltage, bias,
SerPar, speed` or by name. In the latter case you can omit as many parameters
as you like – in that case they will remain unchanged.

E.g.
    
    # Capacitance and Quality factor at 100Hz using a 0.5V signal with no bias 
    # in series mode and fast measurement
    #
    #           ________________________________ modeA
    #          |     ___________________________ modeB
    #          |    |     ______________________ freq
    #          |    |    |     _________________ volt
    #          |    |    |    |    _____________ bias
    #          |    |    |    |   |     ________ SerPar
    #          |    |    |    |   |    |       _ speed
    #          |    |    |    |   |    |      |
    lcr.setup("C", "Q", 100, 500, 0, "SER", "FAST")
    
    # the same using parameter names
    lcr.setup(
        modeA="C", 
        modeB="Q", 
        freq=100, 
        volt=500, 
        bias=0,
        serpar="SER", 
        speed="FAST"
        )
    
    # the same using parameters in a different order
    lcr.setup(
        modeA="C", 
        modeB="Q", 
        serpar="SER", 
        freq=100, 
        speed="FAST"
        volt=500, 
        bias=0,
        )

    # Now change voltage and bias
    lcr.setup(volt=1000, bias=500)

    # Now measure in slow mode
    lcr.setup(speed="slow")

The `setup` method does not include *rel* mode. This is on purpose, as you
probably want to configure the divice first, then connect the DUT and allow the
measurement value to settle before activtin *rel* mode.


## Reading values

After setup, you can start reading measurement values from the device using the
`read` method. `read` is a function and returns a tuple of two floating point values:

* Value of primary parameter (defined by `modeA`)
* Value of secondary parameter (defined by `modeB`)

Example:
   
    # Setup measurement
    lcr.modeA = "C"
    lcr.modeB = "esr"

    # get measurement
    C, ESR = lcr.read()


# Trouble shooting

The SCPI implementation in the instrument is a bit wonky. I spent a lot of time
figuring out some peculiarities and have managed to fully crash the controller
many times. Many of these problems had to do with timing (some commands are
fast, others require some time before you may send a new command). The SCPI
documentation by the manufacturer is a bit obscure and incomplete in some places.

It is quite possible that different models and/or firmware or hardware
revisions behave slightly different than my instrument. If you encounter
problems, you can try tweaking a few parameters:

| parameter  | Description                                               |
|----------  |---------------------------------------------------------  |
| `baudrate` | must match baudrate set in device (default: 9600)         |
| `eol_r`    | line terminator for reading from device (default: "\r\n") |
| `eol_w`    | line terminator for writing to device (default: "\n")     |
| `delay`    | delay after read/write operation [s] (default: 0.0)       |
| `timeout`  | timeout [ms] before giving up on `read` requests (default: 1000) |


Example:

    el = EZ44("ASRL/dev/ttyACM0", delay=0.5, baudrate=14400)


# Contributing

If you think you found a bug or you have an idea for a new feature, please open
an issue here on GitHub. Please **do not submit pull-requests before discussing
the issue** you want to address.

If you want to report a bug, please make sure to replicate the erroneous
behavior at least once before opening an issue and provide all information
necessary to replicate the problem (what commands did you use, what was
connected to the device, what did you observe, what did you expect?).

I would very much appreciate help from people who own any of the various models
listed above: It would be great if they could run the automated tests on their
devices and let me know if that went fine or produced errors. Please get in
touch if you would like to do that. Also any feedback and bug reports are
welcome.

