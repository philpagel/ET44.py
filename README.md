# ET44

Python class for remote controlling EastTester ET44 and ET45 series lcr meters:
ET4401, ET4402, ET4410, ET4501, ET4502, ET4510.


# Status

[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

This should work fine with all devices of the ET44/ET45 series as listed above.
However, I only have a ET4410 so I have no way of testing it on the other
devices.


| Feature                    | Status |
|--------------------------- |------- |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |
|                            |        |


# In a Nutshell

Here is a little example script that illustrates how things work:

```{python}
#!/bin/env python3
import time, datetime
from ET44 import ET44

# connect to the device
lcr = ET44("ASRL/dev/ttyUSB1::INSTR")

# Set to Cs, Rs

lcr.mode = "series"
lcr.par = "C"
lcr.subpar = "R"

# read measuremnt values

C, ESR = lcr.read()


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
    python -m pydoc ET44.channel

For questions about valid values for all commands and general use of the
device, please refer to the manufacturers *user manual* and/or *scpi manual*.

## Connecting
    
This is how you connect to the device:

    from ET44 import ET44
    el = ET44("ASRL/dev/ttyUSB1::INSTR")

Or, on windows:

    from ET44 import ET44
    el = ET44("ASRL2::INSTR")

Of course, you need to adapt it to the right device for your case.
See [here](https://pyvisa.readthedocs.io/en/1.8/names.html) for details on
pyvisa resource names.

## Instrument

XXX

The instrument instance provides the following methods.

    # sound a beep
    el.beep()
    
    # reset to default
    el.reset()

    # unlock the keypad
    # usually not advisable!
    el.unlock()
    # the next command will automatically lock again

    # send trigger event
    el.trigger()

    # turn all inputs on/off
    el.on()
    el.off()

    # query fan state
    el.fan()

    # Write SCPI command to connection and check status
    # e.g. set channel 1 CV mode voltage setting to 12.5V
    el.write("VOLT1:CV 12.5")
    
    # Write SCPI command to connection and return answer value
    # e.g. query channel 1 CV mode voltage setting
    el.query("VOLT1:CV?")

    # print device and status information
    print(el)


## Channels

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
| `delay`    | delay after read/write operation [s] (default: 0.2)       |
| `timeout`  | timeout [ms] before giving up on `read` requests (default: 1000) |

The most likely candidate to fix weird problems is `delay`. The device manual
does not specify what command frequency or processing time the instrument has
so I used the smallest value that allowed all my test cases to pass. I also
asked ET support about it and the answer was "The time interval should be above
200ms" which matches my own observations, but your mileage may vary.

Example:

    el = EZ44("ASRL/dev/ttyUSB0", delay=0.5, baudrate=14400)


## Talking to the device directly

If you want to play with the device on raw metal and try some SCPI commands
yourself, you can connect to it like so

    tio -e -b 9600 -m INLCRNL,OCRNL /dev/ttyUSB0

You can use other programs like minicom etc. Just make sure to get the weirdly
inconsistent line terminators right.

*Caution:* The device uses an internal usb2serial device (*QinHeng Electronics
CH340 serial converter*) which is detected by the operation system even if the
load is turned off. There is nothing I can do about that. Obviously, you cannot
talk to the device in that state. 


# Contributing

If you think you found a bug or you have an idea for a new feature, please open
an issue here on GitHub. Please **do not submit pull-requests before discussing
the issue** you want to address.

If you want to report a bug, please make sure to replicate the erroneous
behavior at least once before opening an issue and provide all information
necessary to replicate the problem (what commands did you use, what was
connected to the load, what did you observe, what did you expect?).

I would very much appreciate help from people who own any of the various models
listed above: It would be great if they could run the automated tests on their
devices and let me know if that went fine or produced errors. Please get in
touch if you would like to do that. Also any feedback and bug reports are
welcome.

