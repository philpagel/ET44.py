# ET44xx/ET45xx firmware updater

East Tester will provide firmware updates upon request, if begged persistently.
They provide a Windows-only updater tool that depends on mscomm32 and the is
pretty hard to get working.  So I wrote this little script to conduct firmware
updates on any OS.

## Status

Work in progress, not functional, yet

## Firmware Upgrade Instructions



1. Turn off the meter
2. Connect meter to computer with RS232 cable. You can use a USB2RS232 cable.
   A simple USB cable will *not* work.
3. Find the firmware file in the archive provided by the manufacturer. It has
   the extension `.hex`. E.g. `V6.00.2522.079.hex`,
   `V6.00.2423.059.hex` or something like that.
4. Start this tool. E.g.:
```sh
./et44fwupdater.py -s /dev/ttyUSB0 V6.00.2522.079.hex   # LINUX
./et44fwupdater.py -s COM3 V6.00.2522.079.hex           # Windows
```
5. Turn on the meter
6. Wait for firmware upload to finish
7. Wait for XXX
8. Done.


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
      -i, --info            Show info only - do not upload anything (default: False)

      -q, --quiet           Run quietly without any output (default: False)

If you find the tool too verbose, use the `-q/--quiet` flag.

When setting `-i/--info`, the program will activate the bootloader but not
trigger the hex file upload. You still need to provide the hexfile argument,
but it is OK if that file doesn't even exist, in this case. This option may be
useful for debugging, later – i.e. finding the bootloader version.


# Images

I have a few firmware images that I found online and/or got from the manufacturer:

* [`V6.00.2522.079.hex`](./images/V6.00.2522.079.hex): VXXXXX



