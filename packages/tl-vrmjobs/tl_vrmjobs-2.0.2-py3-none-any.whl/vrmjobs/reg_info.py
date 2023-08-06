from typing import List, Dict

class RegisterInfo(object):
    """
    Define structure of the information of registering metric exports that
    will be exchanged via reg_ack job
    """
    def __init__(self, status: bool, message: str, max_retries: int):
        self.status = status
        self.message = message,
        self.max_retries = max_retries

    def __repr__(self):
        return "{} - {} - max remaining retries: {}".format(self.status,
                                                            self.message,
                                                            self.max_retries)

    def __str__(self):
        return "{} - {} - max remaining retries: {}".format(self.status,
                                                            self.message,
                                                            self.max_retries)