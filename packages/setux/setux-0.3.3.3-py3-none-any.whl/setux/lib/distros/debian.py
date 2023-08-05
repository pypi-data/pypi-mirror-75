from setux.lib.managers.package import Apt
from setux.lib.managers.service import SystemD

from setux.core.distro import Distro


class Debian(Distro):
    Package = Apt
    Service = SystemD
    pkgmap = dict(
        pip = 'python3-pip',
    )
    svcmap = dict(
    )

    @classmethod
    def release_name(cls, infos):
        did = infos['ID'].strip()
        ver = infos['VERSION_ID'].strip('\r"')
        return f'{did}_{ver}'


class debian_9(Debian):
    pass


class debian_10(Debian):
    pass
