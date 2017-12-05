#!/bin/sh

cd ~/Rescue_Project/
python GPS_new.py
cat ~/Software/julius/test_wav/sample.out ~/Navio2/Python/test.txt > ~/Rescue_Project/victim_data.txt
