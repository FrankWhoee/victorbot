from errors import WrongChannelTypeError

def guildCommand(func):
    def wrapper(self, ctx, *args, **kwargs):
        if ctx.guild:
            return func(self, ctx, *args, **kwargs)
        else:
            raise WrongChannelTypeError("This command can only be used in a server.")
    return wrapper

def dmCommand(func):
    def wrapper(self, ctx, *args, **kwargs):
        if ctx.guild:
            raise WrongChannelTypeError("This command can only be used in a direct message.")
        else:
            return func(self, ctx, *args, **kwargs)
    return wrapper