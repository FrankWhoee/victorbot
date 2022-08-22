from util.errors import WrongChannelTypeError

def guildCommand(func):
    def wrapper(message, *args, **kwargs):
        if message.guild is not None:
            return func(message, *args, **kwargs)
        else:
            raise WrongChannelTypeError("This command can only be used in a server.")
    return wrapper

def dmCommand(func):
    def wrapper(message, *args, **kwargs):
        if message.guild is None:
            return func(message, *args, **kwargs)
        else:
            raise WrongChannelTypeError("This command can only be used in a direct message.")

    return wrapper