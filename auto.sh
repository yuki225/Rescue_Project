#!/bin/sh
cd ~/Rescue_Project
python rec_filter.py
cp human_voice.wav ~/sample_voice
cp human_voice_filtered.wav ~/sample_voice
cd ~/sample_voice
julius -C ~/julius-kits/dictation-kit-v4.4/word.jconf -outfile -input rawfile

===================こっから下はお試し=========================================

cd ~/Navio2/Python
python GPS_test.py

