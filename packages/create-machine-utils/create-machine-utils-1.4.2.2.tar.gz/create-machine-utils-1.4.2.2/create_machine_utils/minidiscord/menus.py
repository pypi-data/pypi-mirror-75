import asyncio
import functools
import inspect
import os
import warnings

import discord
import json
from .exceptions import FullError, ExistsError, NotExistsError

import typing

print(os.path.abspath(__file__))
print(os.getcwd())

with open("minidiscord/emojis.json") as emoji_file:
    emojis = json.load(emoji_file)


def iscoroutinefunction_accepting_partials(obj):
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj)


class Menu:
    def __init__(self, timeout: int = None, reactions: dict = None,
                 timeout_callback: typing.Union[typing.Callable, typing.Coroutine] = None):
        self.timeout_callback = timeout_callback

        self.timeout = timeout or 0

        self.reactions = {}

        if reactions is not None:
            for reaction in reactions.items():
                try:
                    self + reaction
                except Exception as e:
                    warnings.warn(f"Failed to add reaction {reaction} when initialising menu ({e}). Ignoring the issue")

    def __add__(self, other):
        if not type(other) == tuple \
                or not len(other) == 2 \
                or not (isinstance(other[0], discord.Emoji) or (isinstance(other[0], str) and other[0] in emojis)) \
                or not isinstance(other[1], (typing.Callable, typing.Coroutine)):
            return NotImplemented
        if other[1] in self.reactions:
            raise ExistsError("That emoji already has a callback. "
                              "Try removing it before adding another callback")
        if len(self.reactions) >= 20:
            raise FullError("There are too many callbacks already (20/20). "
                            "Try removing one before adding another callback")
        self.reactions[other[0] if isinstance(other[0], discord.Emoji) else emojis[other[0]]] = other[1]

        return self

    def add(self, reaction, callback=None):
        self + (reaction, callback)

    def __sub__(self, other):
        if not (isinstance(other, discord.Emoji) or (isinstance(other, str) and other in emojis)):
            return NotImplemented
        if other[1] not in self.reactions:
            raise NotExistsError("That emoji isn't on the menu")

        del self.reactions[other]

        return self

    def remove(self, reaction):
        self - reaction

    async def _add_reactions_to_message(self, message):
        for reaction in self.reactions:
            await message.add_reaction(reaction)

    # noinspection DuplicatedCode,PyShadowingNames
    async def __call__(self, bot, message, *responding, **_responding):
        responding = responding + tuple(_responding.values())
        if not len(responding):
            raise ValueError("You must provide at least one respondent")

        bot.loop.create_task(self._add_reactions_to_message(message))

        complete, incomplete = await asyncio.wait((
            bot.wait_for("reaction_add", check=lambda reaction, user: (
                    user == responding and
                    reaction.message == message and
                    self.reactions.get(reaction.emoji)
            ), timeout=self.timeout),
            bot.wait_for("message", check=lambda _message: (
                    _message.channel == message.channel and
                    _message.author == responding and
                    self.reactions.get(message.content)
            ), timeout=self.timeout),
        ), return_when=asyncio.FIRST_COMPLETED)

        for task in incomplete:
            task.cancel()

        try:
            complete = list(complete)[0].result()  # type: typing.Union[tuple, discord.message]
        except asyncio.TimeoutError as e:
            if self.timeout_callback:
                return (await self.timeout_callback()) \
                    if iscoroutinefunction_accepting_partials(self.timeout_callback) else \
                    self.timeout_callback()
            raise e

        if isinstance(complete, tuple):
            reaction = complete[0].emoji
        else:
            if message.guild:
                perms = message.channel.permissions_for(message.guild.me)
                # Get our permissions in the current channel
                if isinstance(message.channel, discord.abc.GuildChannel) and perms.manage_messages:
                    await complete.delete()
            reaction = complete.content

        reaction = list(emojis.keys())[list(emojis.values()).index(16)] if type(reaction) == str else reaction

        if callback := self.reactions[reaction]:
            return (await callback()) if iscoroutinefunction_accepting_partials(callback) else callback()

        return reaction
