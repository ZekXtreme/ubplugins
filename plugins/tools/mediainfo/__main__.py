# Copyright (C) 2020-Present by zekxtreme@Github, <https://github.com/ZEKXTRME>.
# All rights reserved.
# PLUGIN BY ZEK

import re
# import aiofiles
import requests
import mimetypes
from urllib.parse import unquote_plus
import subprocess
from pyrogram import enums
# from .telegraph_helper import telegraph
from userge import userge, Message


logger = userge.getLogger(__name__)

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


@userge.on_cmd("minfo", about={
    'header': "Get media info",
    'usage': "{tr}minfo direct link ",
    'examples': ['{tr}minfo']}, check_downpath=True)
async def media_info(message: Message):
    """ get media info """

    # reply = message.reply_to_message
    # reply_id = reply.message_id if reply else None
    sent_link = message.filtered_input_str
    if not sent_link:
        return await message.err("Send a link along with command")
    url_regex = re.compile(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])") # noqa

    try:
        link = url_regex.search(sent_link)
    except Exception:
        await message.edit("Not a valid URL")
    __response = requests.head(link, stream=True)
    await message.edit("Getting MediaInfo")

    if "-r" in message.flags:
        await message.edit("Pending")
        # try:
        #     await message.edit("Getting Raw MediaInfo")
        #     file_size = get_readable_file_size(
        #         int(__response.headers["Content-Length"].strip()))
        #     file_name = unquote_plus(link).rsplit('/', 1)[-1]
        #     mime_type = __response.headers.get(
        #         "Content-Type", mimetypes.guess_type(file_name)).rsplit(";", 1)[0]
        #     result = subprocess.check_output(['mediainfo', link]).decode("utf-8")
        #     lines = result.splitlines()
        #     for i in range(len(lines)):
        #         if 'Complete name' in lines[i]:
        #             lines[i] = re.sub(r": .+", ': '+file_name, lines[i])
        #             break
        #     with open(f'{file_name}.txt', 'w') as f:
        #         f.write('\n'.join(lines))
        #     await message.delete()
        #     cap = f"<b>File Name:</b> <code>{file_name}</code>\n"
        #     f"<b>File Size:</b> <code>{file_size}</code>\n"
        #     f"<b>Mime Type:</b> <code>{mime_type}</code>\n\n"
        #     await message.client.send_document(
        #        f"{file_name}.txt", message.chat.id, reply_to_message_id=reply_id, caption=cap
        #     )
        #     await aiofiles.os.remove(f"{file_name}.txt")
        # except Exception:
        #     await message.edit("Error Occured")
    else:
        try:
            file_size = get_readable_file_size(
                int(__response.headers["Content-Length"].strip()))
            file_name = unquote_plus(link).rsplit('/', 1)[-1]
            mime_type = __response.headers.get(
                "Content-Type", mimetypes.guess_type(file_name)).rsplit(";", 1)[0]
            result = subprocess.run(f'mediainfo "{link}"', capture_output=True, shell=True)
            stderr = result.stderr.decode('utf-8')  # noqa
            stdout = result.stdout.decode('utf-8')
            metadata = stdout.replace("\r", "").replace(link, file_name)
            head = f"Mediainfo of {file_name}"
            html = f'''<pre>{metadata}</pre>'''
            post_url = "https://minfo.deta.dev/api"
            data_json = {"content": html, "heading": head}
            resp = requests.post(post_url, json=data_json)
            metaurl = "https://minfo.deta.dev/" + resp.json()['key']
            # DPASTE_DE_API = 'https://dpaste.org/api/'
            # resp = requests.post(DPASTE_DE_API,
            #                     data={
            #                        'content': html,
            #                         'format': "url",
            #                         "lexer": "_markdown",
            #                         'expires': 604800})
            # metaurl = resp.text
            # page = telegraph.create_page(
            # title="Minfo Results",
            # content=html.format(file_name, metadata)
            # )
            await message.edit(
                f"<b>File Name:</b> <code>{file_name}</code>\n"
                f"<b>File Size:</b> <code>{file_size}</code>\n"
                f"<b>Mime Type:</b> <code>{mime_type}</code>\n\n"
                f"<b>Metadata of your video:</b>\n"
                f"{metaurl}",
                parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
            )
        except KeyError:
            await message.edit("**Not a valid direct downloadable video!**")
        except Exception as err:
            await message.edit(f"<b>Error:</b> <code>{err}</code>", parse_mode=enums.ParseMode.HTML,
                               disable_web_page_preview=True)
