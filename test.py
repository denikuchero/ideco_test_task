import asyncio


async def run(cmd):
    print('start')

    proc = await asyncio.create_subprocess_shell(
        cmd)
    print(proc)
    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(run('sudo systemctl stop nginx'))
