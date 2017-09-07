#-*- cording: utf-8 -*-

import subprocess

subprocess.call("vlc -I rc --play-and-stop human_voice.wav", shell=True)
