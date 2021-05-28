
import subprocess

N_RUNS = 25

for agent in ['dc']:
    for i in range(N_RUNS):
        print('Current run:', agent, i+1)

        subprocess.run(['python3', 'Main.py', agent, agent], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

print('Done!')
