#!/bin/env python3
"""
Frequency sweep measurement

Saves and plots all measurement data
"""

import argparse, sys, time, math
from decimal import Decimal
from ET44 import ET44
from plotnine import (
    ggplot,
    aes,
    labs,
    geom_point,
    geom_line,
    geom_smooth,
    scale_x_log10,
)
from pandas import DataFrame


def main():
    args = getargs()
    dat = measure(args)
    dat = DataFrame(dat, columns=(["f", args.modeA] + args.modeB))
    dat.to_csv(f"{args.output}.csv", index=False)
    print(dat)
    plot_all(dat, args)


def measure(args):
    """Return list of measurements
    one row per frequency"""

    try:
        lcr = ET44(args.rid)
    except:
        exit(f"Connection to instrument failed")

    lcr.setup(
        modeA=args.modeA,
        SerPar=args.SerPar,
        volt=args.volt,
        bias=args.bias,
        speed=args.speed,
    )

    dat = []
    # continuous freqranges
    if len(lcr.freqrange) > 20:
        freqrange = (
            [10, 15, 20, 30, 50, 80]
            + [100, 150, 200, 300, 500, 800]
            + [1000, 1500, 2000, 3000, 5000, 8000, 10000]
        )
        if max(freqrange) > 10000:
            freqrange += [15000, 20000]
        if max(freqrange) > 20000:
            freqrange += [30000, 50000, 80000, 100000]
    else:
        freqrange = lcr.freqrange

    for freq in freqrange:
        print(".", file=sys.stderr, end="", flush=True)
        lcr.freq = freq
        time.sleep(args.delay)  # allow instrument to settle
        row = []
        for modeB in args.modeB:
            lcr.modeB = modeB
            A, B = lcr.read()
            row.append(B)
        else:
            A, B = lcr.read()
        dat.append([freq / 1000, A] + row)
    return dat


def plot_all(dat, args):
    "Plot all data"

    units = {
        "L": "H",
        "C": "F",
        "R": "Ω",
        "X": "Ω",
        "Z": "Ω",
        "X": "Ω",
        "D": "",
        "Q": "",
        "Theta": "°",
        "ESR": "Ω",
    }

    for mode in [args.modeA] + args.modeB:
        num, prefix, multiplier = to_eng(max(dat[mode]))
        dat[mode] *= multiplier
        unit = units[mode]
        if unit:
            unit = f"[{prefix}{unit}]"
        freqplot(dat, mode, unit, args)


def freqplot(dat, yvar, unit, args):
    "Create one plot"

    plot = (
        ggplot(dat, aes(x="f", y=f"{yvar}"))
        + scale_x_log10()
        + geom_point(color="royalblue")
        + geom_line(color="royalblue")
        + labs(
            title="Frequency Sweep",
            x="f [kHz]",
            y=f"{yvar} {unit}",
        )
    )
    plot.save(f"{args.output}_{yvar}.{args.format}", dpi=args.dpi)


def to_eng(n):
    """return number, prefix and multiplicator for engineering format

    e.g.
    to_eng(10)      # (10, "", 1)
    to_eng(100)     # (100, "", 1)
    to_eng(1000)    # (1.0, "k", 0.001)
    to_eng(0.010)   # (10.0, "m", 1000)
    to_eng(0.0001)  # (100.0, "µ", 1000000)
    """

    sign, digits, exponent = Decimal(n).as_tuple()
    exp = len(digits) + exponent - 1
    eng = math.floor(exp / 3)
    mul = 10 ** (-3 * eng)
    n = n * mul

    if eng >= 0:
        prefix = ["", "k", "M", "G", "T"][eng]
    elif eng < 0:
        prefix = ["", "m", "µ", "n", "p", "f"][abs(eng)]
    return n, prefix, mul


def getargs():
    "return commandline arguments and options"

    parser = argparse.ArgumentParser(
        prog="sweep",
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
        "-i", "--rid", help="VISA resource ID", default="ASRL/dev/ttyACM0::INSTR"
    )
    parser.add_argument(
        "-s", "--SerPar", help="Equivalent model mode (SER | PAR)", default="SER"
    )
    parser.add_argument(
        "-v",
        "--volt",
        type=int,
        help="Voltage level [mV] for measurement",
        default="1000",
    )
    parser.add_argument(
        "-b", "--bias", type=int, help="DC voltage bias [mV] (0 – 1500)", default="0"
    )
    parser.add_argument(
        "-S", "--speed", help="Speed (FAST | MEDIUM | SLOW)", default="slow"
    )
    parser.add_argument(
            "-d", "--delay", type=float, help="Delay [s] after changing settings", default="2.0"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="basename of the output files",
        default="sweep",
    )
    parser.add_argument("-D", "--dpi", help="Image resolution", default=300, type=int)
    parser.add_argument("-f", "--format", help="Image format", default="png")

    return parser.parse_args()


if __name__ == "__main__":
    main()
