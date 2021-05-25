#!/usr/bin/env python3

import subprocess

currentRun = 1
while(True):
    print('Current run:', currentRun)
    subprocess.run('python3 Main.py', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    currentRun += 1

