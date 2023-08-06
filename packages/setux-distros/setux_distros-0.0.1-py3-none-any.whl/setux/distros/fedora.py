from setux.core.distro import Distro
from setux.managers.system.package import Dnf
from setux.managers.system.service import SystemD


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
