from setux.core.distro import Distro
from setux.managers.system.package import Pacman
from setux.managers.system.service import SystemD


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
