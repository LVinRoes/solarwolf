# Adaptive music based on external observations

This code belongs to the following research paper:

**Evaluating the Benefits of External Observations for Adaptive Music Systems**
Luca Roes, Fabian Ostermann, Günter Rudolph
*Proceedings of the IEEE Conference on Games (CoG), 2026*

## Setup

Install libraries via pip: `pip install pygame scamp matplotlib`

Install this repository in edit mode: `pip install -e .` (from within the directory where this README is located)

Tested under Linux & Windows with Python 3.8, 3.9, 3.10, 3.11, and 3.12.

## Run

Start the game: `solarwolf`

Start in different music modes: `solarwolf -mode=[Obs|GS|Const]`

More usage info: `solarwolf --help`

## Test and debug adaptive music

For a closer examination of our adaptive music system without the game: `python solarwolf/test_music_controller.py`

A window opens where the intensity level can be changed manually using a slider.


