import asyncio
import time
from asyncio.subprocess import create_subprocess_shell, create_subprocess_exec

lst = []


async def main():
    for i in range(3):
        proc = await create_subprocess_exec('python ', './tmp/pe.py')
        # time.sleep(0.5)
        # ret_code = await proc.wait()
        # print(ret_code, '-----------')
        lst.append(proc)
    print(lst)
    time.sleep(5.0)

    print('sssssssssss')
    for i in range(3):
        ret_code = await lst[i].wait()
        print(ret_code, '----------')
    print('sssssssssss')
    for i in range(3):
        ret_code = await lst[i].wait()
        print(ret_code, '----------')


asyncio.run(main())
