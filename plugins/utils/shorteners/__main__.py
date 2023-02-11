""" Url shortener """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import requests
import gdshortener

from userge import userge, Message


@userge.on_cmd("nocry", about={
    'header': "Shorten Any Url using nocry.me",
    'usage': "{tr}nocry [link or reply]"})
async def nocry(msg: Message):
    link = msg.input_or_reply_str
    if not link:
        await msg.err("need url to shorten")
        return
    try:
        short = requests.get(f'https://nocry.me/api/create?url={link}').text
        await msg.edit(f"`{short}`", disable_web_page_preview=True)
    except Exception:
        await msg.err("API is down")


@userge.on_cmd("isgd", about={
    'header': "Shorten Any Url using is.gd",
    'usage': "{tr}isgd [link or reply]"})
async def is_gd(msg: Message):
    url = msg.input_or_reply_str
    if not url:
        await msg.err("need url to shorten")
        return
    s = gdshortener.ISGDShortener()
    try:
        s_url, stats = s.shorten(url, log_stat=True)
    except Exception as er:
        await msg.err(str(er))
    else:
        await msg.edit(
            f"**Shortened URL:**\n`{s_url}`\n\n**Stats:** `{stats}`",
            disable_web_page_preview=True
        )


@userge.on_cmd("statsisgd", about={
    'header': "Convert is.gd url into original URl.",
    'usage': "{tr}statsisgd [link or reply]"})
async def stats_is_gd(msg: Message):
    url = msg.input_or_reply_str
    if not url:
        await msg.err("need url to check stats")
        return
    s = gdshortener.ISGDShortener()
    try:
        original_url = s.lookup(url)
    except Exception as er:
        await msg.err(str(er))
    else:
        await msg.edit(
            f"**URL:** `{original_url}`",
            disable_web_page_preview=True
        )
