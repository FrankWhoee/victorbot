import discord


async def disconnect_from_guild(client: discord.Client, message: discord.Message) -> None:
    for voice_client in client.voice_clients:
        if voice_client.guild == message.guild:
            await voice_client.disconnect(force=True)
            break