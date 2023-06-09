from asyncio import sleep
import os
from nextcord.ext import commands
from nextcord import Member, FFmpegPCMAudio, ClientException, VoiceState

from Config import isJoinSound
from Utils import logger

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel == after.channel or member.id == self.bot.user.id:
            return
        if before.channel == None and isJoinSound(str(after.channel.guild.id)):
            channel = member.voice.channel
            try:
                vc = await channel.connect()
                await sleep(.5)
                vc.play(FFmpegPCMAudio(os.path.dirname(__file__)+"/../sounds/sound.mp3"))

                while vc.is_playing():
                    await sleep(.1)
                await vc.disconnect()
            except ClientException as e:
                logger.error("", e)

def setup(bot):
    bot.add_cog(Voice(bot))