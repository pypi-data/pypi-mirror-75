from .port_info import PortInfo
from .host_type import HostType
from typing import List, Dict

class HostInfo(object):
    """
    Define structure of the information of a host that
    will be exchanged via probe_init/probe_ack packet
    """
    def __init__(self, hostname: str, inet_addr: str, ports: List[PortInfo], host_type: 'HostType'):
        self.hostname = hostname
        self.inet_addr = inet_addr
        self.ports = ports
        self.type = host_type

    def __str__(self):
        return "{}-{}[{}] - ports: {}".format(str(self.type.name),
                                              self.hostname,
                                              self.inet_addr,
                                              str(self.ports))

    def __repr__(self):
        return "{}({}-{}[{}] - ports: {})".format(self.__class__.__name__,
                                                  self.type.name,
                                                  self.hostname,
                                                  self.inet_addr,
                                                  str(self.ports))

    def daemon_fqinfo(self) -> List[Dict]:
        daemons = []
        for info in self.ports:
            daemons.append({'daemon': info.daemon,
                            'fq_info': (self.inet_addr, info.port)})

        return daemons