#!/bin/sh
#for i in `seq 1 10`
#do
  cd ~/Rescue_Project
  python record.py
  cp human_voice.wav ~/sample_voice
  cp human_voice_filtered.wav ~/sample_voice
  cd ~/sample_voice
  julius -C ~/julius-kits/dictation-kit-v4.4/word.jconf -outfile -input rawfile
#  cd ~/Navio2/Python
#  python modGPS.py
#  cat ~/Navio2/Python/src/test.csv ~/Software/julius/test_wav/sample.out > ~/Rescue_Project/victim_data.csv
#done
