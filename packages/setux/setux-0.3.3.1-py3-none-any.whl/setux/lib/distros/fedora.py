from setux.lib.managers.package import Dnf
from setux.lib.managers.service import SystemD

from setux.core.distro import Distro


class Fedora(Distro):
    Package = Dnf
    Service = SystemD
    pkgmap = dict(
        pip = 'python3-pip',
    )
    svcmap = dict(
        ssh = 'sshd',
    )


class fedora_32(Fedora):
    pass
