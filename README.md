# Vega Auto-tuner

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

## Run

A run is a record of clocks/voltages settings and sensors readings
during a period of time.

Example:

- 60 seconds
- 1600 MHz core setting
- 1200 mV core setting
- 1550 MHz core actual average
- 1150 mV core actual average
- 215 W
- + mem settings/actual

## Auto-tuning (TO BE DEVELOPED)

Set a limit (min clock or max power usage) and let Vatu try to find the
optimal settings for your card.

Example:

- I want a 1600 MHz core average
- Vatu tries the default 1.2 Vcore and succeeds
- Vatu then tries 1.0 Vcore and gets a 1550 MHz average
- ???
- sweet-spot

Vcore is the main variable that determines core clock, ie. with a 0.95 Vcore
setting P7 to 1632 MHz will actually give a 1450 MHz core clock.
Still, if you set P7 to 1642 MHz at that point, you should get a 1460 MHz core
or just crash right away.
In order to get an optimal setup you need to play with
voltage first to get power usage around your target and then push P7 clocks to
the highest point of stability.
