from __future__ import annotations

import time
from typing import Optional

import discord
from discord.ext import commands


class Ping(commands.Cog):
    """Simple ping command implemented as a Cog.

    This provides a hybrid command usable as both a prefix command and a
    slash (application) command.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Show bot latency")
    async def ping(self, ctx: commands.Context[commands.Bot]) -> None:
        """Respond with websocket latency and a measured round-trip time.

        The command sends a short placeholder message and edits it with
        measured timings so the displayed RTT reflects the bot's response time.
        """
        start = time.perf_counter()

        # Send a short placeholder. Using `reply` works for both message and
        # interaction contexts; when invoked as a slash command this will create
        # an interaction response or follow-up as appropriate.
        try:
            msg = await ctx.reply("Pinging...")
        except Exception:
            # Fallback to send if reply fails for some reason
            msg = await ctx.send("Pinging...")

        end = time.perf_counter()

        rtt_ms = int((end - start) * 1000)
        ws_ms = int(self.bot.latency * 1000)

        content = f"Pong! RTT: {rtt_ms}ms | WS: {ws_ms}ms"

        # Edit the placeholder message with final timings.
        try:
            await msg.edit(content=content)
        except Exception:
            # If editing isn't allowed (rare), just send a new message.
            await ctx.send(content)


async def setup(bot: commands.Bot) -> None:
    """Extension setup for `bot.load_extension`.

    This is the async setup signature expected by discord.py v2's
    `load_extension` when used with `await bot.load_extension(...)`.
    """
    await bot.add_cog(Ping(bot))
