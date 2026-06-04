# ET44xx/ET45xx firmware updater

East Tester will provide firmware images if begged persistently.  Their
Windows-only updater tool is in Chinese, depends on mscomm32 and is a real
PITA to get working. So I wrote my own tool for conducting firmware updates
with less pain.


## Status

[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

I.e. I can reliably flash my ET4410 LCR meter using a PL2303 USB-to-Serial
adapter and this tool on LINUX.

This is a re-write of my original Python script (with the help of AI).
Providing a binary instead of a script should make it easier for
non-programmers to run this without having to install any dependencies. I
currently provide binaries for LINUX and WINDOWS.

I'd be *very* grateful for feedback by anyone who was brave enough to give my
tool a try.


#### Risk assessment

* If something goes wrong, you may soft-brick your device
* I consider the risk of hard-bricking to be almost zero because
  sending a hexfile will preserve the bootloader and you should be able to
  bring your device back to live using this tool or the manufacturer's tool (if
  you can get that to work).


## Installation

Download a binary from the [latest
release](https://github.com/philpagel/ET44.py/releases/latest) and unpack the
archive. No installation required. On Linux and MacOS, make sure to make the
binary executable, first:

    chmod a+x et44fwupdater


## Firmware Upgrade Instructions

1. Turn *off* the meter
2. Connect the meter to your computer with a RS232 cable.  
   USB to serial cables are fine, but you may need to install drivers for them.
   Do not use a regular USB cable!  Double-check that you connected to RS232
   and *not to the handler port*.
3. Find the firmware file in the archive provided by the manufacturer. It has
   the extension `.hex`. E.g. `V6.00.2522.079.hex`, `V6.00.2423.059.hex` or
   something like that. I also have a few images in the [images](images/)
   folder.
4. Open a terminal/shell and run this tool.  
```sh
   ./et44fwupdater -s /dev/ttyUSB0 images/ET44_V6.00.2611.089.hex   # LINUX 
   .\et44fwupdater.exe -s COM3 images\ET44_V6.00.2611.089.hex       # Windows 
```
5. Turn *on* the meter  
   The meter's screen will stay black.  
   You should see a menu in Chinese followed by a progress line on your computer.
6. Wait for firmware upload to finish
7. When flash programming is done, the meter should automatically start the new
   firmware.

The entire process will take about 5 1/2 minutes.

The bootloader is very temperamental: It may take several attempts until it
is successfully triggered.


# Example session

```
❯ ./et44fwupdater -s /dev/ttyUSB1 images/ET44_V6.00.2611.089.hex
Sanity checking hexfile
Waiting for bootloader. Please turn on the device now.
 .        
> 杭州中创
> Bootloader Ver:3.00
> ----------------------
> [1]下载程序
> [2]运行程序
> [?]帮助
> ----------------------
Selecting: [1].
> 删除Flash...
> >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
> 删除完成!
> 准备接收文件...
Uploading 'images/ET44_V6.00.2611.089.hex'
Progress: 13237/13237 rows 100%
> 下载成功!
Upload finished.
> ----------------------
> [1]下载程序
> [2]运行程序
> [?]帮助
> ----------------------
Selecting: [2].
```

Lines starting with `>` echo the output received from the device.


## Usage 

```
ET44xx / ET45xx LCR meter firmware updater

Usage: et44fwupdater [OPTIONS] <HEXFILE>

Arguments:
  <HEXFILE>  Firmware hex file

Options:
  -s, --serialdev <SERIALDEV>  Serial device / COM port [default: /dev/ttyUSB0]
  -b, --baudrate <BAUDRATE>    baud rate [default: 19200]
  -q, --quiet                  Suppress console output
  -h, --help                   Print help
  -V, --version                Print version
```



## Trouble shooting

What to do if things don't work/go wrong and/or you have soft-bricked your
device and/or the update ends in an error message and/or the bootloader will not
launch? Here are some things to check or do:

### The tool cannot connect ot the meter

1. Double check that you are using the *correct* serial device (`COMx` port or
   `/dev/ttyUSBx`).
2. Make sure your USB-to-serial cable is supported by your OS. Install drivers
   if necessary.
3. Double-check that your cable is plugged into the RS232 port, not the
   handler port, which uses the same physical socket.


### The tool hangs or exits with a cryptic error message

If the updater seems stuck after you turn on the meter, the bootloader did not 
fire up. That happens a lot.

1. Try again, many times if necessary.
    - Turn off the meter
    - Kill the updater program
    - Start over
2. Try pressing the power button faster/slower/with more passion/while praying
   to the god of firmware updates
3. Try starting with the meter powered on. Start the updater, then turn the
   meter off and back on.
4. Reset everything:
    - Turn off the LCR meter and unplug the power lead.
    - Unplug the RS232 cable from the computer. 
    - Wait for 20 minutes or even over night until the last cap inside has
      fully discharged.
    - Maybe even reboot the computer.
    - Say a few incantations.
    - Start over.


### The meter is bricked @#!?!!

1. Don't panic! Even if the device appears dead, the bootloader is still there
   and the device will almost certainly be recoverable. (Guess how I know...)
2. Verifiy that the hex file is ok:
    - double check that the hexfile is intended for your specific device and
      you did not accidentally use the firmware file of some other device.
    - verify the checksum if you got it from here.
    - inspect the file in a text editor. It should look something like this:  
```
:020000040800F2
:10000000781A002039020008590C0008D30B0008A8
:10001000550C0008F3040008F1140008000000006B
:10002000000000000000000000000000E50F0008D4

    [...]

:00000001FF
```
3. Reset everything:
    - Unplug the RS232 cable from the computer. 
    - Maybe even reboot the computer.
    - Turn off the LCR meter and unplug the power lead.
    - Wait for 20 minutes or even over night until the last cap inside has
      fully discharged.
    - Say a few incantations.
    - Start over.

If all of that fails, you are officially entitled to panic (Just kidding.)


