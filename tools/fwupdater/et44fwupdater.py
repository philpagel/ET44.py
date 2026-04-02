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

    trigger_bootloader(dev)
    handle_menu(dev, 1)
    upload(dev, args.hexfile)
    handle_response(dev)
    handle_menu(dev, 2)
    logger("Update finished. You may turn off the meter now.")


def logger(*dat, end="\n", flush=True):
    "print logging output"
    if not args.quiet:
        print(" ".join(dat), end=end, flush=flush)


def trigger_bootloader(dev):
    "trigger bootloader"

    logger("Sending magic number. Please turn on the device now.")
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


def handle_menu(dev, item):
    "Wait for booloader menu and select item"

    menucomplete = False
    selected = False
    while True:
        line = dev.readline().decode("gbk", errors="replace").rstrip()
        if len(line) > 0:
            logger(">", line)
        if "帮助" in line:  # "Help"
            menucomplete = True
        if "----------------------" in line and menucomplete:
            dev.write(f"{item}".encode("gbk"))  # select option 1: file upload
            logger(f"Selecting: [{item}].")
            selected = True
        if item == 1 and "准备接收文件" in line:  # "Ready to receive file"
            return
        if item == 2 and selected:
            time.sleep(0.5)
            return
        

def upload(dev, hexfile):
    "upload hexfile"

    with open(hexfile, "r") as infile:
        lines = infile.read().splitlines()
    numrows = len(lines)

    logger(f"Uploading '{hexfile}'")
    # dev.reset_input_buffer()
    for i, line in enumerate(lines, 1):
        line += "\n"
        line = line.encode("ascii")
        dev.write(line)
        dev.flush()
        dev.reset_output_buffer()
        percent = (i / numrows) * 100
        logger(f"\rProgress: {i}/{numrows} rows {percent:0.0f}%", end="")

        # wait for "." (ACK)
        timeout = time.time() + 5
        while True:
            if time.time() > timeout:
                sys.exit("ACK timeout")
            time.sleep(0.0001)
            if dev.in_waiting:
                x = dev.read(1)
                if x == b".":  # ACK (".")
                    break
                else:
                    logger()
                    return


def handle_response(dev):
    "Keep reading and handle response"

    t0 = time.time()
    while True:
        if time.time() > t0 + 2:
            sys.exit("Timeout: no response from the device.")
        line = dev.readline().decode("gbk", errors="replace").rstrip()
        if len(line) > 0:
            logger(">", line)
            t0 = time.time()  # extend dealine while data keeps coming
        if "空间溢出" in line:
            sys.exit(f"\nBuffer Overflow")
        if "写入错误" in line:
            sys.exit(f"\nWrite Error")
        if "无效命令" in line:
            sys.exit(f"\nInvalid command")
        if line.startswith("***") and line.endswith("!"):
            sys.exit(f"\nUnknown Error: '{line}'")
        if "下载成功!" in line:
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
