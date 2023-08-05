from os import environ

from setux.lib.targets import Local, SSH


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
