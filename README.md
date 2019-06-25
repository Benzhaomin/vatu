# Vega Auto-tuner

*Disclaimer: this tool is still in development. Default settings should be
safe but if in doubt please read the disclaimer.*

A tool to record and fine-tune power and clocks on AMD Radeon RX Vega cards.
Useful for undervolting and overclocking your card to its sweet spot or to
whatever spot is the sweetest to you.

## Install

```
git clone https://github.com/Benzhaomin/vatu.git
cd vatu
virtualenv3 venv
source venv/bin/activate
pip install -e .
```

## Dev

Install +

```
pip install -e .[dev]
nosetests
flake8
```

## Config

A default config file is read from (config.default.yaml). Each field can
be overriden in a local config.yml file of specified with the -c flag on the
command line.

```
cp vatu/config/
```

Main settings to look at:

- files: full path to file-like interfaces to the driver
- readonly: set to true to never actually change any setting (true by default)



## Usage

```
$ vatu --help
Usage: vatu [OPTIONS] COMMAND [ARGS]...

  Vega Auto Tuner

Options:
  -v, --verbose
  -c, --config TEXT  load configuration from this file
  --help             Show this message and exit.

Commands:
  autotune  (WIP) try to reach a power, clock or temperature target
  show      show the card's current state
```

### vatu show

Quick monitoring of temperatures, clocks, voltages and Power Play states.

```
$ watch sudo vatu show
```

### vatu autotune

Start an auto-tuning run, playing with settings and looking at sensors to try
to reach a target clock. Settings are printed along the way and reverted back
on exit.

```
$ sudo vatu autotune --help
Usage: vatu autotune [OPTIONS]

Options:
  -d, --duration INTEGER
  -i, --interval INTEGER
  --help                  Show this message and exit.
```

## Auto-tuning

Set a limit and let Vatu try to find the optimal settings for your card.

Actual core clock is a best-effort value that satisfies three things:
- total power limit
- max temperature
- stability

If the card can't reach its target clock without hitting a limit, it will simply clock a bit lower
or just jump down a power state.

Overclock example with the default 1200 mV core:
- 1500 Mhz P7 => 1500 Mhz actual
- 1600 Mhz P7 => 1570 Mhz actual
- 1700 Mhz P7 => 1640 Mhz actual or crash

Undervolt example with 1600 Mhz P7:
- 1200 mV => 1570 Mhz actual
- 1150 mV => 1540 Mhz actual
- 1100 mV => 1500 Mhz actual
- 1050 mV => drop to P6


### Speedy Tuner

Example of a quick run raising core clock every two second as pstate is stable
and we're not hitting any power/temp/clock limits.

```
$ sudo vatu -c config.yml -v autotune -d 30 -i 2
INFO - Initial state  95% 48C 172.0W / 220W # 1384Mhz@1100mV P5 1400Mhz@1100mV #  945Mhz P3  945Mhz@1050mV
INFO -  80% 48C 171.0W / 220W # 1378Mhz@1100mV P5 1400Mhz@1100mV #  945Mhz P3  945Mhz@1050mV
INFO - core p-level isn't stable, not doing anything this tick
INFO -  92% 48C 174.0W / 220W # 1372Mhz@1100mV P5 1400Mhz@1100mV #  945Mhz P3  945Mhz@1050mV
INFO - core p-level isn't stable, not doing anything this tick
INFO -  98% 46C 175.0W / 220W # 1377Mhz@1100mV P5 1400Mhz@1100mV #  945Mhz P3  945Mhz@1050mV
INFO - p-level stable and high enough, raising core clock to 1405MHz
INFO -  84% 48C 166.0W / 220W # 1372Mhz@1100mV P5 1405Mhz@1100mV #  945Mhz P3  945Mhz@1050mV
INFO - p-level stable and high enough, raising core clock to 1410MHz
INFO - Reached final state  84% 48C 166.0W / 220W # 1382Mhz@1100mV P5 1410MHz@1100mV #  945Mhz P3  945Mhz@1050mV
INFO - Restoring initial state  95% 48C 172.0W / 220W # 1384Mhz@1100mV P5 1400Mhz@1100mV #  945Mhz P3  945Mhz@1050mV
````

### Starving Tuner

(NOT IMPLEMENTED YET)

- I want a 1600 MHz core clock
- try the default 1.2 Vcore, pstate stable and clock delta is ok
- lower vcore by 10mV get a 1590 MHz clock
- ???
- sweet-spot
