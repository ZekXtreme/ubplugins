""" get system info """

# Copyright (C) 2020-2022 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

from datetime import datetime

import psutil
from psutil._common import bytes2human

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from requests import get
from pyrogram.enums import ParseMode
from userge import userge, Message
from userge.utils import runcmd


async def generate_sysinfo(workdir):
    # uptime
    info = {
        'BOOT': (datetime.fromtimestamp(psutil.boot_time())
                 .strftime("%Y-%m-%d %H:%M:%S"))
    }
    # CPU
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    info['CPU'] = (
        f"{psutil.cpu_percent(interval=1)}% "
        f"({psutil.cpu_count()}) "
        f"{cpu_freq}"
    )
    # Memory
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    info['RAM'] = (f"{bytes2human(vm.total)}, "
                   f"{bytes2human(vm.available)} available")
    info['SWAP'] = f"{bytes2human(sm.total)}, {sm.percent}%"
    # Disks
    du = psutil.disk_usage(workdir)
    dio = psutil.disk_io_counters()
    info['DISK'] = (f"{bytes2human(du.used)} / {bytes2human(du.total)} "
                    f"({du.percent}%)")
    if dio:
        info['DISK I/O'] = (
            f"R {bytes2human(dio.read_bytes)} | W {bytes2human(dio.write_bytes)}")
    # Network
    nio = psutil.net_io_counters()
    info['NET I/O'] = (
        f"TX {bytes2human(nio.bytes_sent)} | RX {bytes2human(nio.bytes_recv)}")
    # Sensors
    sensors_temperatures = psutil.sensors_temperatures()
    if sensors_temperatures:
        temperatures_list = [
            x.current
            for x in sensors_temperatures['coretemp']
        ]
        temperatures = sum(temperatures_list) / len(temperatures_list)
        info['TEMP'] = f"{temperatures}\u00b0C"
    info = {f"{key}:": value for (key, value) in info.items()}
    max_len = max(len(x) for x in info)
    return ("```\n" + "\n".join([f"{x:<{max_len}} {y}" for x, y in info.items()]) + "```\n")


@userge.on_cmd("sysinfo", about="Get system info of your host machine.")
async def get_sysinfo(message: Message):
    await message.edit("Getting system information ...")
    response = await generate_sysinfo(userge.workdir)
    await message.edit("<u>**System Information**</u>:\n" + response)


@userge.on_cmd(
    "neofetch",
    about={
        "header": "Neofetch is a command-line system information tool",
        "description": "displays information about your operating system, software and hardware in an aesthetic and visually pleasing way.", # noqa
        "usage": " {tr}neofetch",
        "flags": {"-img": "To Get output as Image"},
        "examples": ["{tr}neofetch", "{tr}neofetch -img"],
    },
)
async def neofetch_(message: Message):
    await message.edit("Getting System Info ...")
    reply = message.reply_to_message
    reply_id = reply.message_id if reply else None
    if "-img" in message.flags:
        await message.delete()
        await message.client.send_photo(
            message.chat.id, await neo_image(), reply_to_message_id=reply_id
        )
    else:
        await message.edit(f'<code>{(await runcmd("neofetch --stdout"))[0]}</code>',
                           parse_mode=ParseMode.HTML)


async def neo_image():
    neofetch = (await runcmd("neofetch --stdout"))[0]
    font_color = (255, 42, 38)  # Red
    white = (255, 255, 255)
    if "Debian" in neofetch:
        base_pic = "https://telegra.ph/file/1f62cbef3fe8e24afc6f7.jpg"
    elif "Kali" in neofetch:
        base_pic = "https://i.imgur.com/iBJxExq.jpg"
        font_color = (87, 157, 255)  # Blue
    else:
        base_pic = "https://telegra.ph/file/f3191b7ecdf13867788c2.jpg"
    font_url = (
        "https://raw.githubusercontent.com/code-rgb/AmongUs/master/FiraCode-Regular.ttf"
    )
    photo = Image.open(BytesIO(get(base_pic).content))
    drawing = ImageDraw.Draw(photo)
    font = ImageFont.truetype(BytesIO(get(font_url).content), 14)
    x = 0
    y = 0
    for u_text in neofetch.splitlines():
        if ":" in u_text:
            ms = u_text.split(":", 1)
            drawing.text(xy=(315, 45 + x), text=f"{ms[0]}:", font=font, fill=font_color)
            drawing.text(
                xy=((8.5 * len(ms[0])) + 315, 45 + x), text=ms[1], font=font, fill=white
            )
        else:
            color = font_color if y == 0 else white
            drawing.text(xy=(315, 53 + y), text=u_text, font=font, fill=color)
        x += 20
        y += 13
    new_pic = BytesIO()
    photo = photo.resize(photo.size, Image.ANTIALIAS)
    photo.save(new_pic, format="JPEG")
    new_pic.name = "NeoFetch.jpg"
    return new_pic
