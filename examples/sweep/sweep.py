#!/bin/env python3
"""
Frequency sweep measurement

Saves and plots all measurement data
"""

import argparse, time
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
    plot(dat, args)


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
    for freq in lcr.freqrange:
        lcr.freq = freq
        time.sleep(2)  # allow instrument to settle
        row = []
        for modeB in args.modeB:
            lcr.modeB = modeB
            A, B = lcr.read()
            row.append(B)
        else:
            A, B = lcr.read()
        dat.append([freq/1000, A] + row)
    return dat


def plot(dat, args):
    "Plot the data"

    plot = (
        ggplot(dat, aes(x="f", y=f"{args.modeA}"))
        + scale_x_log10()
        + geom_point(color="royalblue")
        + geom_line(color="royalblue")
        + labs(title="Frequency Sweep", x="f [kHz]")
    )
    plot.save(f"{args.output}_{args.modeA}.{args.format}", dpi=args.dpi)
    
    for modeB in args.modeB:
        plot = (
            ggplot(dat, aes(x="f", y=f"{modeB}"))
            + scale_x_log10()
            + geom_point(color="royalblue")
            + geom_line(color="royalblue")
            + labs(title="Frequency Sweep", x="f [kHz]")
        )
        plot.save(f"{args.output}_{modeB}.{args.format}", dpi=args.dpi)


def getargs():
    "return commandline arguments and options"

    parser = argparse.ArgumentParser(
        prog="sweep",
        description="Frequency sweep measurement",
        epilog="",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
            "modeA", choices=["L", "C", "R", "Z"], help="Primary parameter"
    )
    parser.add_argument(
        "modeB",
        nargs="*",
        choices=["Q" ,"X" ,"Theta" , "D", "ESR"],
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
        "-o",
        "--output",
        help="basename of the output files",
        default="sweep",
    )
    parser.add_argument("-d", "--dpi", help="Image resolution", default=300, type=int)
    parser.add_argument("-f", "--format", help="Image format", default="png")

    return parser.parse_args()


if __name__ == "__main__":
    main()

