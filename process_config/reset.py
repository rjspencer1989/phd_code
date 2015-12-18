#!/usr/bin/env python
import subprocess
import time
import generate_history


def reset():
    cmd = ["/home/homeuser/phd_code/setup.sh"]
    subprocess.call(cmd, cwd="/home/homeuser/phd_code")
    print 'reset'
    time.sleep(5)
    print 'generating history'
    generate_history.generate()

if __name__ == "__main__":
    reset()
