from .host_info import HostInfo
from .vrm_type import VrmType

class ProbeAck(object):
    """
    System packet that will be encapsulated inside an UDP packet
    and reply back to collector host using information provided
    in probe_init packet by worker host
    """
    def __init__(self, packet_id: str, info: 'HostInfo', packet_type: 'VrmType'):
        self.id = packet_id
        self.info = info
        self.type = packet_type

    def __str__(self):
        return "[{}] {} - {}".format(str(self.type), id, str(self.info))

    def __repr__(self):
        return "{}({} - {})".format(self.__class__.__name__,
                                    id,
                                    str(self.info))