#!/usr/bin/env python3
"Firmware updater for ET44xx/ET45xx LCR meters"

import time, serial, sys, os.path, argparse


def main():

    # connect to serial device
    try:
        dev = serial.Serial(
            args.serialdev,
            baudrate=19200,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=0.01,
            xonxoff=0,
            rtscts=0,
        )
    except serial.serialutil.SerialException:
        sys.exit(f"Error: Cannot open serial device {args.serialdev}")

    trigger(dev)
    bootloader(dev)
    upload(dev, args.hexfile)


def logger(*dat, end="\n", flush=True):
    "print logging output"
    if not args.quiet:
        print(" ".join(dat), end=end, flush=flush)


def trigger(dev):
    "trigger bootloader"

    logger("Sending magic number. Please turn on the device now.")

    # send magic nubmer until we get into bootloader menu
    magic = bytes.fromhex("1b42543936057a")
    pos = 0
    inc = 1
    while True:
        # night rider
        light = [" "] * 10
        light[pos] = "."
        logger("\r" + "".join(light), end="")
        if pos == 9:
            inc = -1
        elif pos == 0:
            inc = 1
        pos += inc

        dev.write(magic)
        dev.flush()
        time.sleep(0.1)
        dev.in_waiting
        if dev.in_waiting > 0:  # load is responding
            break
    logger()


def bootloader(dev):
    "Wait for booloader menu and select upload"
    # Upload hexfile when device is ready

    menucomplete = 0
    while True:
        line = dev.readline().decode("gb2312").rstrip()
        if len(line) > 0:
            logger(">", line)
        if "帮助" in line:  # "Help"
            menucomplete = 1
        if "----------------------" in line and menucomplete:
            if args.info:
                break
            else:
                dev.write("1".encode("gb2312"))  # select option 1: file upload
                logger("Selecting: [1] File Upload.")
        if "准备接收文件" in line:  # "Prepare to receive file"
            return


def upload(dev, hexfile):
    "upload hexfile"

    try:
        filesize = os.path.getsize(hexfile)
    except:
        sys.exit(f"Error: cannot open hexfile '{hexfile}'")
    logger(f"Uploading '{hexfile}': {filesize} bytes")

    try:
        infile = open(hexfile, "rb")
    except:
        sys.exit(f"Error: cannot open hexfile '{hexfile}'")

    sent = 0
    row = 0
    while chunk := infile.readline():
        dev.write(chunk)
        dev.flush()
        line = dev.readline().decode("gb2312").rstrip()
        row += 1
        if line != len(line) * ".": # suppress progress dots
            logger("\n>", line)
        if "空间溢出" in line:
            sys.exit("Device out of memory. Abort.")
        if "写入错误" in line:
            print(":", chunk)
            sys.exit("Write Error. Abort.")
        if line.startswith("***") and line.endswith("!"):
            sys.exit(f"Unknown Error (row {row}). Abort.")
        sent += len(chunk)
        percent = (sent / filesize) * 100
        logger(f"\rProgress: {sent}/{filesize} bytes {percent:0.0f}%", end="")
    infile.close()
    logger()

    while True:
        line = dev.readline().decode("gb2312").rstrip()
        if len(line) > 0:
            logger(">", line)
        if "下载成功!" in line:  # "Download successful!"
            logger("Upload finished.")
            logger("Wait for device to display 'Please Reset!' before cycling power.")
            break


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Perform firmware update on an ET44xx/ET45xx LCR meters.",
        epilog="""Instructions: 1. Turn off the device and connect RS232 lead. 
        2. Start this programm. 3. Turn on the device and wait for program to finish.
        4. When display shows 'Please reset!', power cycle device.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s", "--serialdev", default="/dev/ttyUSB1", help="Serial device"
    )
    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Show info only - do not upload anything",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Run quietly without any output"
    )
    parser.add_argument("hexfile", help="path to hexfile, e.g. image.hex")
    global args
    args = parser.parse_args()

    try:
        main()
    except KeyboardInterrupt:
        pass
