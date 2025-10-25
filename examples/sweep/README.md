# Frequency Sweep

Little program that will perform a frequency sweep for a measurement – i.e.
take the same measurement at different frequencies.

The measurement results are saved in CSV format and as a plots.

You need to specify one major mode (L, C or R). You can specify one ore more
secondary modes (X, Q, D, Theta or ESR), of you like. All variables will be
plotted against measurement freqency, individually.

## Prerequisites

    # create a virtual environment
    python -m venv _venv

    # activate the virtual environment
    source _venv/bin/activate

    # install prerequisites
    python -m pip install -r requirements.txt

## Usage

To get usage help, use the  `-h` option:

    ❯ ./sweep.py -h
    usage: sweep [-h] [-i RID] [-s SERPAR] [-v VOLT] [-b BIAS] [-S SPEED] [-o OUTPUT]
                 [-d DPI] [-f FORMAT]
                 modeA [modeB ...]

    Frequency sweep measurement

    positional arguments:
      modeA                Priamry parameter you want to measure (L | C | R)
      modeB                Secondary parameter(s) you want to measure (X | Q | X |
                           Theta | D | ESR) (default: None)

    options:
      -h, --help           show this help message and exit
      -i, --rid RID        VISA resource ID (default: ASRL/dev/ttyACM0::INSTR)
      -s, --SerPar SERPAR  Equivalent model mode (SER | PAR) (default: SER)
      -v, --volt VOLT      Voltage level [mV] for measurement (default: 1000)
      -b, --bias BIAS      DC voltage bias [mV] (0 – 1500) (default: 0)
      -S, --speed SPEED    Speed (FAST | MEDIUM | SLOW) (default: slow)
      -o, --output OUTPUT  basename of the output files (.csv and .png) (default:
                           sweep)
      -d, --dpi DPI        Image resolution (default: 300)
      -f, --format FORMAT  Image format (default: png)


### Example

Let's measure a 10µF electrolytic capacitor at 1V and 0.5V DC bias:

    ./sweep.py --volt 1000 --bias 500 C ESR

or shorter:

    ./sweep.py -v 1000 -b 500  C ESR

This is the resulting data file (`sweep.csv`):

    f,C,ESR
    0.1,1.01823e-05,17.3947
    0.12,1.00726e-05,16.8874
    0.2,1.02749e-05,12.759
    0.4,8.94043e-06,9.26897
    0.8,8.24663e-06,6.03034
    1.0,8.0558e-06,5.29265
    2.0,7.52614e-06,3.79435
    4.0,7.04582e-06,3.03674
    8.0,6.58554e-06,2.64599
    10.0,6.43442e-06,2.564
    15.0,6.14198e-06,2.44898
    20.0,5.90068e-06,2.38785
    40.0,5.26653e-06,2.27353
    50.0,5.03743e-06,2.2454
    80.0,4.47828e-06,2.20342
    100.0,4.13228e-06,2.18293


And the generated plot (`sweep.pg`) looks like this:

XXX

To change the basename of the file use the `-o/--output` option:

    ./sweep.py -v 1000 -b 500  C ESR -o 10µF-cap


