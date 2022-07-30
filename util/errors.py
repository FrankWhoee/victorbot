class WrongChannelTypeError(Exception):
    pass

class CommandError(Exception):
    def __init__(self, message):
        self.message = message