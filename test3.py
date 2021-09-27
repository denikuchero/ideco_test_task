# #!/usr/bin/env python
# from subprocess import Popen, PIPE
#
# sudo_password = '112233'
# command = 'systemctl stop nginx'.split()
#
# p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE,
#           universal_newlines=True)
# sudo_prompt = p.communicate(sudo_password + '\n')

import os, sys
print(sys.argv)
print(os.execvp())