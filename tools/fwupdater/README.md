# ET44xx/ET45xx firmware updater

East Tester will provide firmware updates if begged persistently.  They provide
a Windows-only updater tool in Chinese that depends on mscomm32 and is a real
PITA to get working. So I wrote this little script to conduct firmware updates
on any OS and with less pain.


## Status

[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

I.e. I have successfully flashed an image to my ET4410 LCR meter using a PL2303
USB-to-Serial adapter and this tool on LINUX. I'd be *very* gratefull for
feedback by anyone who was brave enought to give my tool a try.

#### Risk assessment

* If something goes wrong, you may soft-brick your device
* I consider the risk of hard-bricking to be almost non-existant because
  sending a hexfile will preserve the bootloader any you should be able to
  bring your device back to live using this tool or the manufactureres tool (if
  you can get that to work).


## Firmware Upgrade Instructions

1. Turn *off* the meter
2. Connect meter to computer with RS232 cable. USB to serial cables are fine, but
   you may need the appropriate drivers for them.  
   Do not use a regular USB cable!  
   Double-check that you connected to RS232 and *not to the handler port*.
3. Find the firmware file in the archive provided by the manufacturer. It has
   the extension `.hex`. E.g. `V6.00.2522.079.hex`,
   `V6.00.2423.059.hex` or something like that.
4. Start this tool. You may have to make it executable, first (`chmod a+x
   et44fwupdater.py`) or call Python explicitly (`python3 et44fwupdater.py ...`)  
   E.g.:
```sh
./et44fwupdater.py -s /dev/ttyUSB0 V6.00.2522.079.hex   # LINUX
python3 et44fwupdater.py -s COM3 V6.00.2522.079.hex     # Windows
```
5. Turn *on* the meter
6. Wait for firmware upload to finish
7. When flash programming is done, the meter will automatically start the new
   firmware.

The entire process should take about 5 1/2 minutes.

The bootloader is very temperamental: It can take several tries until it
is successfully triggered.


# Example session

```
❯ ./et44fwupdater.py images/ET44_V6.00.2611.089.hex
Sending magic number. Please turn on the device now.
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
Progress: 13237/13237 rows 100%> 下载成功!
Upload finished.
> ----------------------
> [1]下载程序
> [2]运行程序
> [?]帮助
> ----------------------
Selecting: [2].
Update finished. You may turn off the meter now.
```

Lines starting with `>` echo the output received from the device.


## Usage 

```
usage: et44fwupdater.py [-h] [-s SERIALDEV] [-q] hexfile

ET44xx/ET45xx LCR-meter firmware update tool v0.1

positional arguments:
  hexfile               path to hexfile, e.g. image.hex

options:
  -h, --help            show this help message and exit
  -s, --serialdev SERIALDEV
                        Serial device (default: /dev/ttyUSB1)
  -q, --quiet           Run quietly without any output (default: False)
```



# Images

I have a few firmware images that I found online and/or got from the manufacturer:

* [`V6.00.2423.059.hex`](./images/ET44_V6.00.2423.059.hex)
* [`V6.00.2522.079.hex`](./images/ET44_V6.00.2522.079.hex)
* [`V6.00.2611.089.hex`](./images/ET44_V6.00.2611.089.hex)


# Installation

In addition to this script, you need

* A shell (bash, zsh, PowerShell, cmd, ...)
* A working Python3 installation
* The `pyserial` module

In the most simple case, you can install the dependencies like this:

    python3 -m pip install -r requirements.txt

If pip complains that it won't do that, you need a virtual environment. So here
it goes:

    python3 -m venv venv                        # create venv

    source venv/bin/activate                    # activate venv (LINUX/Mac)
    venv\Scripts\activate                       # activate venv (Windows)

    python3 -m pip install -r requirements.txt  # install dependencies

Now you are ready to use the tool. But remember: If you close the shell
and come back later, you need to repeat the activation step.


# Trouble shooting

What to do if things don't work/go wrong and/or you have soft-bricked your
device and/or the update ends in an error message and/or the bootloader will not
launch? Here are some things to check or do:

1. Don't panic! Even if the device appears dead, the bootloader is still there
   and the device will almost certainly be recoverable. (Guess how I know...)
2. Make sure your USB-to-serial cable is supported by your OS. Install drivers
   if necessary.
3. Double check that you are using the *correct* serial device (`COMx` port or
   `/dev/ttyUSBx`).
4. Double-check that your cable is plugged into the RS232 Port, not the handler
   Port, which uses the same physical socket.
5. Try again, several times if necessary.
    - Turn off the meter
    - Kill the updater program
    - Start over
6. When turning the device on, do so swiftly. Sometimes when pressing the power
   button too slowly, triggering the bootloader fails.
7. Reset everything:
    - Unplug the RS232 Cable from the computer. 
    - Maybe even reboot the computer.
    - Turn off the LCR meter and unplug the power lead.
    - Wait for 20 minutes or even over night until the last cap inside has
      fully discharged.
    - Say a few incantations.
    - Start over.

If all of that fails, you are officially entitled to panic (Just kidding.)


