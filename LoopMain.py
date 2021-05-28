#!/usr/bin/env python3

import subprocess

N_RUNS = 100

for agent in ['r', 'd', 'dc']:
    for i in range(N_RUNS):
        print('Current run:', agent, i+1)
        subprocess.run(f'python3 Main.py {agent} {agent}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

print('Done!')
