import discord
import asyncio
import os
from discord import Activity, ActivityType

bots_data = []

for i in range(1, 6):
    token = os.getenv(f"TOKEN_{i}")
    channel_id = os.getenv(f"CHANNEL_ID_{i}")

    if token and channel_id:
        bots_data.append({
            "TOKEN": token,
            "CHANNEL_ID": int(channel_id)
        })


class VoiceBot(discord.Client):
    def __init__(self, channel_id):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.voice_states = True

        super().__init__(intents=intents)

        self.channel_id = channel_id
        self.voice_client = None

    async def connect_voice(self):
        channel = self.get_channel(self.channel_id)

        if not channel:
            print(f"❌ Channel {self.channel_id} not found")
            return

        try:
            if self.voice_client and self.voice_client.is_connected():
                return

            self.voice_client = await channel.connect(
                self_deaf=True,
                self_mute=True
            )

            print(f"🔊 {self.user} joined {channel.name}")

        except Exception as e:
            print(f"⚠️ {self.user} error: {e}")

    async def set_streaming_status(self):
        activity = Activity(
            type=ActivityType.streaming,
            name="24/7 Voice Bot",
            url="https://twitch.tv/discord"
        )
        await self.change_presence(activity=activity)

    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

        await self.set_streaming_status()
        await self.connect_voice()

        while True:
            await asyncio.sleep(20)

            if not self.voice_client or not self.voice_client.is_connected():
                print(f"♻️ {self.user} reconnecting...")
                await self.connect_voice()


async def start_bot(token, channel_id):
    bot = VoiceBot(channel_id)
    await bot.start(token)


async def main():
    await asyncio.gather(*[
        start_bot(bot["TOKEN"], bot["CHANNEL_ID"])
        for bot in bots_data
    ])


asyncio.run(main())
