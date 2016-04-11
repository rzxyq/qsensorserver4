#! /bin/bash
rm screenlog.0
python qsensorpost.py &
screen -L /dev/tty.AffectivaQ-v2-2072-SPP 1000

