from setux.lib.managers.package import Pacman
from setux.lib.managers.service import SystemD

from setux.core.distro import Distro


class manjaro(Distro):
    Package = Pacman
    Service = SystemD
    pkgmap = dict(
        pip = 'python-pip',
    )
    svcmap = dict(
        ssh = 'sshd',
    )

    @classmethod
    def release_name(cls, infos):
        return infos['ID'].strip()
