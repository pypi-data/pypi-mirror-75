from sys import path, argv
from os import getcwd
from os import environ

from setux.targets import Local, SSH

from setux.repl import commands
from setux.repl.repl import repl, prompt
from .usage import usage


def get_target(name=None):
    name = name or environ.get('setux_target')
    if name:
        try:
            target = SSH(name=name, host=name)
        except:
            target = None
    else:
        target = Local()
    return target


def main():
    path.insert(0, getcwd())

    if len(argv)>1:
        name = argv[1]
        if name in ('usage', 'help', '?'): return usage()
        if name.startswith('-'): return usage()
        cmd = commands.get(name)
    else:
        cmd = None

    if cmd:
        target, args = None, argv[2:]
        if args:
            target = get_target(args[-1])
            if target:
                args = args[:-1]
        if not target:
            target = get_target()
        args = ' '.join(args)
        print(f'{prompt(target)}{args}')
        cmd(target, args)
    else:
        target = get_target(argv[1] if len(argv)>1 else None)
        repl(target)
