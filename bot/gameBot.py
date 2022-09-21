
import os
from dotenv import load_dotenv, find_dotenv
import discord
from discord.ext import commands
from pathlib import Path


class GameBot(commands.Bot):
    def __init__(self):
        self._cogs = [name.stem for name in Path(".").glob("*/bot/cogs/*.py")]
        # ustawienie prefixu komendy oraz przymus rozróżnienia liter
        super().__init__(command_prefix='!&', case_insensitive=True)

    def setup(self):
        print("Running setup...")
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"Loaded: {cog} cog.")
        print("Setup Complete")

    def run(self):
        self.setup()
        load_dotenv(find_dotenv('.env'))
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        print("Running bot")
        super().run(BOT_TOKEN)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("+")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
