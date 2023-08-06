from setux.distros.debian import debian_10
from setux.managers.system.service import SystemV


class MX_19(debian_10):
    Service = SystemV
    svcmap = dict(
    )

    @classmethod
    def release_name(cls, infos):
        did = infos['DISTRIB_ID']
        ver = infos['DISTRIB_RELEASE'].split('.')[0]
        return f'{did}_{ver}'
