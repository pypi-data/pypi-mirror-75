from .host_info import HostInfo
from .vrm_type import VrmType

class ProbeInit(object):
    """
    System job that will be encapsulated inside an UDP packet
    and broadcast to all worker hosts inside a single network segment
    by a collector host
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
