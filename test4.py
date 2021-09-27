from subprocess import Popen, PIPE


def update():
    sudo_password = '112233'
    command1 = 'apt-get update'.split()
    command2 = 'apt-get upgrade'.split()
    p = Popen(['sudo', '-S'] + command1, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    p.communicate(sudo_password + '\n')
    p1 = Popen(['sudo', '-S'] + command2, stdin=PIPE, stderr=PIPE, universal_newlines=True)
    p1.communicate('y\n')

update()
