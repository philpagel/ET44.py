#i!/bin/env python3
"""
Log data over time

Save and plot all measurement data
"""

import argparse, time, datetime
from ET44 import ET44

def main():
    global args
    args = getargs()
    if args.time is None:
        args.time = float("Inf")
    else:
        t = args.time.split(":")
        t.reverse()
        t = [int(x) for x in t]
        t = list(zip((1, 60, 3600), t))
        tt = 0
        for x in t:
            tt += x[0] * x[1]
        args.time = tt
    measure()


def measure():
    "Log list of measurements"

    try:
        lcr = ET44(args.RID)
    except:
        exit(f"Connection to instrument failed")

    lcr.modeA = args.modeA
    lcr.SerPar = args.SerPar
    lcr.volt = args.volt
    lcr.bias = args.bias
    lcr.freq = args.frequency
    lcr.speed = args.speed

    print(",".join(["timestamp", args.modeA] + args.modeB), flush=True)
    t0 = time.time()
    while time.time() - t0 < args.time:
        Bs = []
        for modeB in args.modeB:
            lcr.modeB = modeB
            A, B = lcr.read()
            Bs.append(B)
        else:
            A, B = lcr.read()

        print(",".join([ str(x) for x in [str(datetime.datetime.now()), A]+Bs]), flush=True)
        time.sleep(args.interval)
    return dat


def getargs():
    "return commandline arguments and options"

    parser = argparse.ArgumentParser(
        prog="logger.py",
        description="Frequency sweep measurement",
        epilog="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("modeA", choices=["L", "C", "R", "Z"], help="Primary parameter")
    parser.add_argument(
        "modeB",
        nargs="*",
        choices=["Q", "X", "Theta", "D", "ESR"],
        help="Secondary parameter(s)",
    )
    parser.add_argument(
        "-t",
        "--time",
        help="Time to log for [h:m:s]. Until interrupted if not set",
        default=None,
    )
    parser.add_argument(
        "-i", "--interval", type=int, help="Delay between reads [s].", default=1
    )
    parser.add_argument(
        "-r",
        "--RID",
        help="VISA resource ID",
        default="ASRL/dev/ttyACM0::INSTR",
    )
    parser.add_argument(
        "-s", "--SerPar", help="Equivalent model mode (SER | PAR)", default="SER"
    )
    parser.add_argument(
        "-v",
        "--volt",
        type=int,
        help="Voltage level [mV] for measurement",
        default=1000,
    )
    parser.add_argument(
        "-b", "--bias", type=int, help="DC voltage bias [mV] (0 – 1500)", default=0
    )
    parser.add_argument(
        "-f", "--frequency", type=int, help="Measurement frequency [Hz]", default=100
    )
    parser.add_argument(
        "-S", "--speed", help="Speed (FAST | MEDIUM | SLOW)", default="slow"
    )

    return parser.parse_args()


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt: 
        pass
