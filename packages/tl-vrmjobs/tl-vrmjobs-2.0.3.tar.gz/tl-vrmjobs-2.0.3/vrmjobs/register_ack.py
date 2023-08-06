from .register_info import RegisterInfo
from .vrm_type import VrmType

class RegisterAck(object):
    """
    System job that will be encapsulated inside an UDP packet
    and send to the worker host after the collector host tried
    to initialize the metric exporters of that worker using
    provided REST-api
    """
    def __init__(self, packet_id: str, info: 'RegisterInfo' , packet_type: 'VrmType'):
        self.id = packet_id
        self.info = info
        self.type = packet_type

    def __str__(self):
        return "[{}] {} - {}".format(str(self.type), id, str(self.info))

    def __repr__(self):
        return "{}({} - {})".format(self.__class__.__name__,
                                    id,
                                    str(self.info))