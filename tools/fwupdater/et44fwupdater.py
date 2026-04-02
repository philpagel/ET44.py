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
            timeout=0.1,
            xonxoff=0,
            rtscts=0,
        )
    except serial.serialutil.SerialException:
        sys.exit(f"Error: Cannot open serial device {args.serialdev}")

    dev.flush()
    dev.reset_input_buffer()
    dev.reset_output_buffer()

    trigger(dev)
    bootloader(dev, 1)
    upload(dev, args.hexfile)
    bootloader(dev, 2)


def logger(*dat, end="\n", flush=True):
    "print logging output"
    if not args.quiet:
        print(" ".join(dat), end=end, flush=flush)


def trigger(dev):
    "trigger bootloader"

    logger("Sending magic number. Please turn on the device now.")

    dev.flush()
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


def bootloader(dev, item):
    "Wait for booloader menu and select item"

    logger("Waiting for bootloader")
    menucomplete = 0
    while True:
        line = dev.readline().decode("gbk", errors="replace").rstrip()
        if len(line) > 0:
            logger(">", line)
        if "帮助" in line:  # "Help"
            menucomplete = 1
        if "----------------------" in line and menucomplete:
            dev.write(f"{item}".encode("gbk"))  # select option 1: file upload
            logger(f"Selecting: [{item}].")
        if "准备接收文件" in line:  # "Ready to receive file"
            return


def upload(dev, hexfile):
    "upload hexfile"

    try:
        filesize = os.path.getsize(hexfile)
    except:
        sys.exit(f"Error: cannot open hexfile '{hexfile}'")
    logger(f"Uploading '{hexfile}': {filesize} bytes")

    try:
        infile = open(hexfile, "r")
    except:
        sys.exit(f"Error: cannot open hexfile '{hexfile}'")

    sent = 0
    time.sleep(0.5)
    dev.reset_input_buffer()
    for lno, line in enumerate(infile, 1):
        line = line.encode("ascii")
        dev.write(line)
        dev.flush()
        dev.reset_output_buffer()
        sent += len(line)
        percent = (sent / filesize) * 100
        logger(f"\rProgress: {sent}/{filesize} bytes {percent:0.0f}%", end="")

        time.sleep(0.5)
        timeout = time.time() + 5 # timeout 5 seconds
        while True:
            if time.time() > timeout:
                sys.exit("ACK timeout")
            if dev.in_waiting:
                x = dev.read(1)
                if x == b".":  # ACK (".")
                    break
                else:
                    msg = x + dev.readline()
                    msg = msg.decode("gbk", errors="replace")
                    msg = msg.rstrip()
                    logger("\n> " + msg)
                if "空间溢出" in msg:
                    sys.exit(f"Overflow in line: {lno}")
                if "写入错误" in msg:
                    sys.exit(f"Write Error in line: {lno}")
                if "无效命令" in msg:
                    sys.exit(f"Invalid command")
                if msg.startswith("***") and msg.endswith("!"):
                    sys.exit(f"Unknown Error '{msg}' in line: {lno}")
            time.sleep(0.001)
    infile.close()
    logger()

    # keep reading output after upload
    while line := dev.readline().decode("gbk", errors="replace").rstrip():
        if len(line) > 0:
            logger(">", line)
        if "下载成功!" in line:  # "Download successful!"
            logger("Upload finished.")
            break


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="ET44xx/ET45xx LCR-meter firmware update tool v0.1",
        epilog="""1. Turn off the device and connect RS232 lead. 
        2. Start this programm. 3. Turn on the device and wait until upload and programming are finished""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-s", "--serialdev", default="/dev/ttyUSB1", help="Serial device"
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
