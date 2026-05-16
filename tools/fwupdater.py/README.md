# ET44xx/ET45xx firmware updater

East Tester will provide firmware updates if begged persistently.  They provide
a Windows-only updater tool in Chinese that depends on mscomm32 and is a real
PITA to get working. So I wrote this little script to conduct firmware updates
on any OS and with less pain.


## Status

**Deprecated!** 

Please switch to reqritten version of the tool which is provided as binaries
for recent releases. The Python script is no longer maintained and will be
removed from future releases.

-----

I.e. I have successfully flashed an image to my ET4410 LCR meter using a PL2303
USB-to-Serial adapter and this tool on LINUX. User cbelcher2020 on the EEVblog Forum
has successfully flashed his ET4510 on Windows using an FTDI USB-to-serial cable.

I'd be *very* grateful for feedback by anyone who was brave enough to give my
tool a try.


#### Risk assessment

* If something goes wrong, you may soft-brick your device
* I consider the risk of hard-bricking to be almost zero because
  sending a hexfile will preserve the bootloader and you should be able to
  bring your device back to live using this tool or the manufacturer's tool (if
  you can get that to work).


## Firmware Upgrade Instructions

1. Turn *off* the meter
2. Connect the meter to your computer with a RS232 cable.  
   USB to serial cables are fine, but you may need to install drivers for them.
   Do not use a regular USB cable!  Double-check that you connected to RS232
   and *not to the handler port*.
3. Find the firmware file in the archive provided by the manufacturer. It has
   the extension `.hex`. E.g. `V6.00.2522.079.hex`, `V6.00.2423.059.hex` or
   something like that.
4. Start this tool.  
   You may have to make it executable, first (`chmod a+x et44fwupdater.py`) or
   call Python explicitly (`python3 et44fwupdater.py ...`)  E.g.: 
```sh
   ./et44fwupdater.py -s /dev/ttyUSB0 images/ET44_V6.00.2611.089.hex   # LINUX 
   python3 et44fwupdater.py -s COM3 images/ET44_V6.00.2611.089.hex     # Windows 
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
Progress: 13237/13237 rows 100%
> 下载成功!
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
* Ideally `pipx`

You can install this programm via `pip` or just copy it to a folder of oyur
choice, but then you need to make sure, that `pyserial` ist installed as well.

The easiest way to install this is to use [pipx](https://github.com/pypa/pipx).
Download the `et44fwupdater-0.1-py3-none-any.whl` or `et44fwupdater-0.1.tar.gz`
form the latest [release](https://github.com/philpagel/ET44.py/releases) and
install it like this:

```
pipx install et44fwupdater-0.1.tar.gz

# or

pipx install et44fwupdater-0.1-py3-none-any.whl
```

Alternatively, you can install it with `pip`

```
python -m pip install et44fwupdater-0.1.tar.gz

# or

python -m pip install et44fwupdater-0.1-py3-none-any.whl
```

You may need to create a virtual enviroment first. If you don't know what that
is, use `pipx` and thank me later.


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
4. Double-check that your cable is plugged into the RS232 port, not the handler
   port, which uses the same physical socket.
5. Try again, several times if necessary.
    - Turn off the meter
    - Kill the updater program
    - Start over
6. When turning the device on, do so swiftly. Sometimes when pressing the power
   button too slowly, triggering the bootloader fails.
7. Reset everything:
    - Unplug the RS232 cable from the computer. 
    - Maybe even reboot the computer.
    - Turn off the LCR meter and unplug the power lead.
    - Wait for 20 minutes or even over night until the last cap inside has
      fully discharged.
    - Say a few incantations.
    - Start over.

If all of that fails, you are officially entitled to panic (Just kidding.)


