#!/usr/bin/env python
import subprocess
import time
import generate_history
cmd = ["./setup.sh"]
subprocess.call(cmd, cwd="..")
print 'reset'
time.sleep(5)
print 'generating history'
generate_history.generate()
