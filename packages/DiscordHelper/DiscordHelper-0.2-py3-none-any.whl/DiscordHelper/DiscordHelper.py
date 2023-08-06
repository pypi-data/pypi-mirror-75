import discord
import asyncio
import ast
import datetime
import aiohttp
import random

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class DiscordHelper:
    def __init__(self):
        self.channels = []
        self.start_time = self.timeset()

    def timeset(self):
        start_time = datetime.datetime.utcnow()
        return start_time
    
    async def notice(self, Bot, lists: list = None):
        for i in Bot.guilds:
            for name in lists:
                channel = discord.utils.find(lambda v: name in v.name, i.text_channels)
                if channel is not None:
                    self.channels.append(channel)
                    break
        return self.channels
    
    async def reply(self, ctx, msg):
        await ctx.channel.send(f"{ctx.author.mention}, {msg}")

    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time
