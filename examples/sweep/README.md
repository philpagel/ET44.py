# Frequency Sweep

Little program that will perform a frequency sweep for a measurement – i.e.
take the same measurement at different frequencies.

The measurement results are saved in CSV format and as a plots.

You need to specify one major mode (L, C or R). You can specify one ore more
secondary modes (X, Q, D, Theta or ESR) if you like. All variables will be
plotted against measurement frequency, individually.

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
      modeA                Primary parameter (L | C | R)
      modeB                Secondary parameter(s) (X | Q | X | Theta | D | ESR)
                           (default: None)

    options:
      -h, --help           show this help message and exit
      -i, --rid RID        VISA resource ID (default: ASRL/dev/ttyACM0::INSTR)
      -s, --SerPar SERPAR  Equivalent model mode (SER | PAR) (default: SER)
      -v, --volt VOLT      Voltage level [mV] for measurement (default: 1000)
      -b, --bias BIAS      DC voltage bias [mV] (0 – 1500) (default: 0)
      -S, --speed SPEED    Speed (FAST | MEDIUM | SLOW) (default: slow)
      -o, --output OUTPUT  basename of the output files (default: sweep)
      -d, --dpi DPI        Image resolution (default: 300)
      -f, --format FORMAT  Image format (default: png)



### Example

Let's measure a 10µF electrolytic capacitor at 1V and 0.5V DC bias:

    ./sweep.py --volt 1000 --bias 500 C ESR Theta

or shorter:

    ./sweep.py -v 1000 -b 500  C ESR Theta

This is the resulting data file (`sweep.csv`):


    f,C,ESR,Theta
    0.1,1.01796e-05,10.3242,-83.6592
    0.12,1.00543e-05,16.5438,-82.8349
    0.2,1.05466e-05,12.3492,-80.705
    0.4,8.94723e-06,9.19684,-78.314
    0.8,8.26526e-06,5.99932,-76.0044
    1.0,8.07564e-06,5.2755,-75.0131
    2.0,7.54325e-06,3.79562,-70.2117
    4.0,7.06028e-06,3.04198,-61.6424
    8.0,6.59577e-06,2.65165,-48.6805
    10.0,6.4403e-06,2.56957,-43.8828
    15.0,6.13587e-06,2.45326,-35.1762
    20.0,5.88219e-06,2.39091,-29.5026
    40.0,5.20424e-06,2.27448,-18.5807
    50.0,4.94981e-06,2.24477,-15.9858
    80.0,4.33676e-06,2.20088,-11.7772
    100.0,3.96105e-06,2.17955,-10.4452

And the generated plots look like this:

<img src="img/sweep_C.png" width=500) />
<img src="img/sweep_ESR.png" width=500) />
<img src="img/sweep_Theta.png" width=500) />

To change the basename of the file use the `-o/--output` option:

    ./sweep.py -v 1000 -b 500  C ESR -o 10µF-cap


