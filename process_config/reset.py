#!/usr/bin/env python
import subprocess
import generate_history
cmd = ["./setup.sh"]
subprocess.call(cmd, cwd="..")
generate_history.generate()
