import readline
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

from cmd import Cmd

from setux import banner
from .helps import helps
from . import commands


def safe(cmd, target):
    def wrapper(arg):
        try:
            cmd(target, arg)
        except Exception as x:
            print(type(x).__name__, x)
    return wrapper


def prompt(target):
    user = 'sudo' if target.sudo else target.distro.Login.name
    return f'{user}@{target.name} > '


class Repl(Cmd):
    def __init__(self, target):
        self.prompt = prompt(target)
        for name, cmd in commands.items():
            setattr(self, f'do_{name}', safe(cmd, target))
        super().__init__()

    def do_help(self, cmd):
        if cmd:
            hlp = helps.get(cmd)
            if hlp:
                print(cmd)
                print('-'*len(cmd))
                print(hlp)
            else:
                print(f'unkown command "{cmd}"')
        else:
            print('commands')
            print('--------')
            for cmd, hlp in helps.items():
                first = hlp.split('\n')[0]
                print(f'\t{cmd} : {first}')

    def preloop(self):
        print(banner)
        self.onecmd('infos')
        print()

    def default(self, line):
        self.onecmd(f'run {line}')

    def do_EOF(self, arg):
        return True


def repl(target):
    Repl(target).cmdloop()
