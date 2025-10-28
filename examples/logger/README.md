# Date logger

Little program that will log data from the esr meter over a period of time.

The measurement results are saved in CSV format and as a plots.

## Usage

    usage: logger.py [-h] [-t TIME] [-i INTERVAL] [-r RID] [-s SERPAR] [-v VOLT]
                     [-b BIAS] [-f FREQUENCY] [-S SPEED]
                     {L,C,R,Z} [{Q,X,Theta,D,ESR} ...]

    Frequency sweep measurement

    positional arguments:
      {L,C,R,Z}             Primary parameter
      {Q,X,Theta,D,ESR}     Secondary parameter(s) (default: None)

    options:
      -h, --help            show this help message and exit
      -t, --time TIME       Time to log for [h:m:s]. Until interrupted if not set
                            (default: None)
      -i, --interval INTERVAL
                            Delay between reads [s]. (default: 1)
      -r, --RID RID         VISA resource ID (default: ASRL/dev/ttyACM0::INSTR)
      -s, --SerPar SERPAR   Equivalent model mode (SER | PAR) (default: SER)
      -v, --volt VOLT       Voltage level [mV] for measurement (default: 1000)
      -b, --bias BIAS       DC voltage bias [mV] (0 – 1500) (default: 0)
      -f, --frequency FREQUENCY
                            Measurement frequency [Hz] (default: 100)
      -S, --speed SPEED     Speed (FAST | MEDIUM | SLOW) (default: slow)


### Example

Let's start loging resistance every 5 seconds for an hour:

    ❯ ./logger.py -t 1:00:00 -i 5 R
    timestamp,R
    2025-10-28 22:42:26.343035,1058100000.0
    2025-10-28 22:42:31.357653,-1000000000000000.0
    2025-10-28 22:42:36.358948,-1000000000000000.0
    2025-10-28 22:42:41.362893,-1000000000000000.0
    2025-10-28 22:42:46.393885,2063590000.0
    2025-10-28 22:42:51.440905,2456130000.0

Use shell redirection to save the data
    ❯ ./logger.py -t 1:00:00 -i 5 R  > outfile.csv






