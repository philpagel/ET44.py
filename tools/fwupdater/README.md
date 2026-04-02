# ET44xx/ET45xx firmware updater

East Tester will provide firmware updates upon request, if begged persistently.
They provide a Windows-only updater tool that depends on mscomm32 and the is
pretty hard to get working. So I wrote this little script to conduct firmware
updates on any OS.

## Status

[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

I.e. I have successfully flashed an image to my ET4410 LCR meter using a PL2303
USB-to-Serial adapter and this tool on LINUX. I'd be *very* gratefull for
feedback by anyone who wav brave enought to give my tool a try.

#### Risk assessment

* If something goes wrong, you may soft-brik your device
* I consider the risk of hard-bricking to be non-existant because
  Sendg a hexfile will preserve the bootloader any you should be able to 
  bring your device back to live using the manufactireres tool but their tool
  is a major PITA. That's why my tool exists in the first place.


## Firmware Upgrade Instructions

1. Turn *off* the meter
2. Connect meter to computer with RS232 cable. USB to serial cables are fine, but
   you may need the appropriate drivers for them.  
   Do not use a regular USB cable!
3. Find the firmware file in the archive provided by the manufacturer. It has
   the extension `.hex`. E.g. `V6.00.2522.079.hex`,
   `V6.00.2423.059.hex` or something like that.
4. Start this tool. E.g.:
```sh
./et44fwupdater.py -s /dev/ttyUSB0 V6.00.2522.079.hex   # LINUX
./et44fwupdater.py -s COM3 V6.00.2522.079.hex           # Windows
```
5. Turn *on* the meter
6. Wait for firmware upload to finish
7. When flash programming is done, the meter will automatically reset.

The bootloader is very temperamental: It can take several tries until it
is successfully triggered.


# Example session

```
❯ ./et44fwupdater.py images/V6.00.2423.059.hex
Sending magic number. Please turn on the device now.
     .
> 杭州中创
> Bootloader Ver:3.00
> ----------------------
> [1]下载程序
> [2]运行程序
> [?]帮助
> ----------------------
Selecting: [1] File Upload.
> 删除Flash...
> >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
> 删除完成!
> 准备接收文件...
Uploading 'images/V6.00.2423.059.hex': 595113 bytes
Progress: 595113/595113 bytes 100%
```

Lines starting with `>` echo the output received from the device.


## Usage 

    usage: et44fwupdater.py [-h] [-s SERIALDEV] [-q] hexfile

    Perform firmware update on an ET44xx/ET45xx LCR meters.

    positional arguments:
      hexfile               path to hexfile, e.g. image.hex

    options:
      -h, --help            show this help message and exit
      -s, --serialdev SERIALDEV
                            Serial device (default: /dev/ttyUSB1)
      -q, --quiet           Run quietly without any output (default: False)

If you find the tool too verbose, use the `-q/--quiet` flag.


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
4. Try again, several times if necessary.
    - Turn off the meter
    - Kill the updater program
    - Start over
5. When turning the device on, do so swiftly. Sometimes when pressing the power
   button slowly, things go wrong.
6. Reset everything:
    - Unplug the RS232 Cable from the computer. 
    - Maybe even reboot the computer.
    - Turn off the LCR meter and unplug the power lead.
    - Wait for 20 minutes or even over night until the last cap inside has
      fully discharged.
    - Say a few incantations.
    - Start over.

If all of that fails, you are officially entitled to panic (Just kidding.)


