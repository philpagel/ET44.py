import pytest
from time import sleep
from ET44 import ET44
from .testconfig import *

lcr = ET44(RID)
sleep(5)

print("\nModel:    ", lcr.idn["model"])
print("Firmware: ", lcr.idn["firmware"])
print("Hardware: ", lcr.idn["hardware"])
model = lcr.idn["model"]

def test_write():
    "raw scpi command sending"
    # valid command
    lcr.write("FUNC:IMP:A C")
    # invalid command
    with pytest.raises(RuntimeError):
        lcr.write("FOOBAR 42")
    # failed command
    with pytest.raises(RuntimeError):
        lcr.write("FUNC:IMP:A CCC")


def test_basics():
    """basic commands w/o return value
    just ensure they don't crash"""

    lcr.beep()
    lcr.trig()
    lcr.lock()
    lcr.unlock()

@pytest.mark.parametrize("mode", ["AUTO", "r", "C", "l", "Z", "DcR", "EcAP"])
def test_modeA(mode):
    lcr.modeA = mode
    assert lcr.modeA == mode.upper()

@pytest.mark.parametrize("mode", ["X", "d", "Q", "ThetA", "EsR"])
def test_modeB(mode):
    lcr.modeB = mode
    assert lcr.modeB == mode.upper()

@pytest.mark.parametrize("mode", ["SEr", "PaR"])
def test_Serpar(mode):
    lcr.SerPar = mode
    assert lcr.SerPar == mode.upper()

@pytest.mark.parametrize("mode", ["FAST", "Medium", "slow"])
def test_speed(mode):
    lcr.speed = mode
    assert lcr.speed == mode.upper()

@pytest.mark.parametrize("value", [100, 300, 1000, 2000])
def test_volt(value):
    lcr.volt = value
    assert lcr.volt == value

    with pytest.raises(ValueError):
        lcr.volt = 15000
        lcr.volt = 10

@pytest.mark.parametrize("value", [10, 500, 1000, 1500, 0])
def test_bias(value):
    lcr.bias = value
    assert lcr.bias == value

    with pytest.raises(ValueError):
        lcr.bias = 15000
        lcr.bias = 10

@pytest.mark.parametrize("value", [100, 120, 400, 800, 1000])
def test_freq(value):
    lcr.freq = value
    assert lcr.freq == value

    with pytest.raises(ValueError):
        lcr.freq = 1000000
        lcr.rfreq = 1

def test_rel():
    lcr.rel = "ON"
    assert lcr.rel == "ON"
    lcr.rel = "off"
    assert lcr.rel == "OFF"
    lcr.rel = "on"
    assert lcr.rel == "ON"
    lcr.rel = "Off"
    assert lcr.rel == "OFF"
    lcr.rel = "oN"
    assert lcr.rel == "ON"
    
    with pytest.raises(ValueError):
        lcr.rel = "FOOBAR"

@pytest.mark.parametrize("mode", ["MEas", "COMP", "sys", "meaS"])
def test_display(mode):
    lcr.display = mode
    assert lcr.display == mode.upper()
    
    with pytest.raises(ValueError):
        lcr.display = "FOOBAR"
  

@pytest.mark.parametrize("modeA, modeB, freq, volt, bias, SerPar, speed, trig", 
                         [
                             ("C",   "X",      100,  1000,   0, "Ser", "Slow", "INt"),
                             ("C",   "ESR",    120,   600, 100, "Par", "Medium", "EXT"),
                             ("L",   "Q",     1000,  2000,   0, "Ser", "Slow", "MaN"),
                             ("R",   "Theta", 4000,   300, 200, "SER", "fast", "EXT"),
                             ("DCR", "D",      400,  2000,   0, "par", "Slow", "man"),
                         ])
def test_setup(modeA, modeB, freq, volt, bias, SerPar, speed, trig):
    # ordered parameters
    lcr.setup(modeA, modeB, freq, volt, bias, SerPar, speedm, trigger)
    assert lcr.modeA == modeA.upper()
    assert lcr.modeB == modeB.upper()
    assert lcr.freq == freq
    assert lcr.volt == volt
    assert lcr.bias == bias
    assert lcr.SerPar == SerPar.upper()
    assert lcr.speed == speed.upper()
    assert lcr.trigger == trig.upper()

    # named parameters
    lcr.setup(modeA=modeA, modeB=modeB, freq=freq, volt=volt, bias=bias,
              SerPar=SerPar, speed=speed, trigger=trig)
    assert lcr.modeA == modeA.upper()
    assert lcr.modeB == modeB.upper()
    assert lcr.freq == freq
    assert lcr.volt == volt
    assert lcr.bias == bias
    assert lcr.SerPar == SerPar.upper()
    assert lcr.speed == speed.upper()
    assert lcr.trigger == trig.upper()

def test_setup_missing():
    "test partial re-configuration"

    lcr.setup("C", "X", 100, 1000, 0, "Ser", "Slow")
    assert lcr.modeA == "C"
    assert lcr.modeB == "X"
    assert lcr.freq == 100
    assert lcr.volt == 1000
    assert lcr.bias == 0
    assert lcr.SerPar == "SER"
    assert lcr.speed == "SLOW"

    lcr.setup(SerPar="Par", freq=1000)
    assert lcr.modeA == "C"
    assert lcr.modeB == "X"
    assert lcr.freq == 1000
    assert lcr.volt == 1000
    assert lcr.bias == 0
    assert lcr.SerPar == "PAR"
    assert lcr.speed == "SLOW"

    lcr.setup(freq=2000, modeB="Theta", bias=500)
    assert lcr.modeA == "C"
    assert lcr.modeB == "THETA"
    assert lcr.freq == 2000
    assert lcr.volt == 1000
    assert lcr.bias == 500
    assert lcr.SerPar == "PAR"
    assert lcr.speed == "SLOW"
    
    


def test_read():
    "only test for non.crash"

    assert len(lcr.read()) == 2


