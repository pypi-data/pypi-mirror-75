from inspect import getsource

from setux.logger import debug, error
from setux.core.package import Packager

try:
    from . import pacman_bigs
except Exception as x:
    error(x)
    raise

# pylint: disable=expression-not-assigned


class Pacman(Packager):

    def do_init(self):
        # self.do_cleanup()
        self.do_update()
        self.run(f'pacman --no-confirm -Sq yay')

    def do_installed(self):
        ret, out, err = self.run(f'pacman -Qe', report='quiet')
        for line in out:
            try:
                name, ver = line.split()
                yield name, ver
            except: pass

    def do_bigs(self):
        src = getsource(pacman_bigs)
        ret, out, err = self.target.script(src)
        for line in out:
            yield line

    def do_upgradable(self):
        ret, out, err = self.run('pacman -Qu', report='quiet')
        for line in out:
            try:
                name, ver = line.split(' ', 1)
                yield name, ver
            except Exception as x:
                debug(line)

    def do_available(self):
        ret, out, err = self.run(f'pacman -Ssq', report='quiet')
        for line in out:
            try:
                name, ver = line.split()
                yield name, ver
            except: pass

    def do_remove(self, pkg):
        self.run(f'pacman --noconfirm -Rs {pkg}')

    def do_cleanup(self):
        self.run('pacman --noconfirm -Rcsun $(pacman -Qdtq)')
        self.run('pacman --noconfirm -Scc')

    def do_update(self):
        self.run('pacman -Sy')

    def do_upgrade(self):
        self.run('pacman --noconfirm -Su')

    def do_install(self, pkg, ver=None):
        # self.run(f'pacman -S --needed --noconfirm {pkg}')
        ret, out, err = self.run(f'yay -S --needed --noconfirm {pkg}')
        if err:
            msg = '\n'.join(err)
            debug(msg) if ret==0 else error(msg)

