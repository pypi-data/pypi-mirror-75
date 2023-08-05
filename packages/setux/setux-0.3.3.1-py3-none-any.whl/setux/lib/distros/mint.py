from setux.lib.distros.debian import debian_10
from setux.lib.managers.service import SystemD


class Mint_20(debian_10):
    Service = SystemD
    svcmap = dict(
    )

    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        if did=='LinuxMint':
            did='Mint'
        ver = infos['DISTRIB_RELEASE']
        return f'{did}_{ver}'
