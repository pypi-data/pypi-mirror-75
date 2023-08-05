from .port_info import PortInfo
from typing import List, Dict

class MetricInfo(object):
    """
    Define structure of the information of the metric exporter
    running in a worker host
    """
    def __init__(self, inet_addr: str, ports: List[PortInfo]):
        self.inet_addr = inet_addr
        self.ports = ports

    def __str__(self):
        return "{} - ports: {}".format(self.inet_addr,
                                       str(self.ports))

    def __repr__(self):
        return "{}({} - ports: {})".format(self.__class__.__name__,
                                           self.inet_addr,
                                           str(self.ports))

    def metric_fqinfo(self) -> List[Dict]:
        metrics = []
        for info in self.ports:
            metrics.append({'job': info.daemon,
                            'target': "{}:{}".format(self.inet_addr, info.port)})

        return metrics