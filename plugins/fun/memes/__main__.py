""" enjoy memes """

# Copyright (C) 2020-2021 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from urllib import parse
from random import choice,  randint  
import aiohttp

from pyrogram import enums
import requests
from userge import userge, Message


@userge.on_cmd("bakk", about={'header': "Check yourself ;)"})
async def bakk_(message: Message):
    await message.edit("Zek Will Be Back after few hours For More Bakchodi")

@userge.on_cmd("pat", about={
    'header': "Give head Pat xD",
    'flags': {'-g': "For Pat Gifs"},
    'usage': "{tr}pat [reply | username]\n{tr}pat -g [reply]"})
async def pat(message: Message):
    username = message.filtered_input_str
    reply = message.reply_to_message
    reply_id = reply.id if reply else message.id
    if not username and not reply:
        await message.edit("**Bruh** ~`Reply to a message or provide username`", del_in=3)
        return
    kwargs = {"reply_to_message_id": reply_id, "caption": username}

    if "-g" in message.flags:
        async with aiohttp.ClientSession() as session, session.get(
            "https://nekos.life/api/pat"
        ) as request:
            result = await request.json()
            link = result.get("url")
            await message.client.send_animation(
                message.chat.id, animation=link, **kwargs
            )
    else:
        async with aiohttp.ClientSession() as session:
            chi_c = await session.get("https://headp.at/js/pats.json")
            uri = f"https://headp.at/pats/{parse.quote(choice(await chi_c.json()))}"
        await message.reply_photo(uri, **kwargs)

    await message.delete() 


@userge.on_cmd("slap", about={
    'header': "reply to slap them with random objects !!",
    'usage': "{tr}slap [input | reply to msg]"}, allow_channels=False)
async def slap_(message: Message):
    """slap"""
    u_id = message.input_str
    if message.reply_to_message:
        u_id = message.reply_to_message.from_user.id
    if not u_id:
        await message.err("no input found!")
        return
    info_dict = await message.client.get_user_dict(u_id)
    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)
    where = choice(WHERE)
    caption = "..." + temp.format(victim=info_dict['mention'],
                                  item=item, hits=hit,
                                  throws=throw, where=where)
    if message.from_user.is_self:
        await message.edit(caption)
    elif message.reply_to_message:
        await message.reply_to_message.reply(caption)
    else:
        await message.reply(caption)


@userge.on_cmd("insult$", about={'header': "Check yourself ;)"})
async def insult_(message: Message):
    """insult"""
    await check_and_send(message, choice(INSULT_STRINGS), parse_mode=enums.ParseMode.HTML)


@userge.on_cmd("mock", about={
    'header': "Do it and find the real fun",
    'usage': "{tr}mock [input | reply to msg]"})
async def mock_(message: Message):
    """mock"""
    input_str = message.input_or_reply_str
    if not input_str:
        await message.err("`gIvE sOMEtHInG tO MoCk!`")
        return
    reply_text = []
    for charac in input_str:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)
    await message.edit("".join(reply_text))


@userge.on_cmd("lfy", about={
    'header': "Let me Google that for you real quick !!",
    'usage': "{tr}lfy [query | reply to msg]"})
async def lfy_(message: Message):
    """lfy_"""
    query = message.input_or_reply_str
    if not query:
        await message.err("`gIvE sOMEtHInG tO lFy!`")
        return
    query_encoded = query.replace(" ", "+")
    lfy_url = f"https://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {'format': 'json', 'url': lfy_url}
    r = requests.get('https://is.gd/create.php', params=payload)
    await message.edit(f"Here you are, help yourself.\n[{query}]({r.json()['shorturl']})")


@userge.on_cmd("hi", about={
    'header': "Greet everyone!",
    'usage': "{tr}hi\n{tr}hi [emoji | character]\n{tr}hi [emoji | character] [emoji | character]"})
async def hi_(message: Message):
    """hi"""
    input_str = message.input_str
    if not input_str:
        await message.edit(choice(HELLOSTR), parse_mode=enums.ParseMode.HTML)
    else:
        args = input_str.split()
        if len(args) == 2:
            paytext, filler = args
        else:
            paytext = args[0]
            filler = choice(EMOJIS)
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 4,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 4,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 8 + filler * 2 + paytext * 2,
            paytext * 8 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2,
            paytext * 2 + filler * 4 + paytext * 2 + filler * 2 + paytext * 2)
        await message.edit(pay)


@userge.on_cmd("belo", about={
    'header': "Get a Logical Quote",
    'usage': "{tr}belo"}, allow_via_bot=False)
async def being_logical(message: Message):
    raw_list = [msg async for msg in userge.get_chat_history("@BeingLogical")]
    raw_message = choice(raw_list)
    await message.edit(raw_message.text)


@userge.on_cmd("tips", about={
    'header': "Get a Pro Tip",
    'usage': "{tr}tips"}, allow_via_bot=False)
async def pro_tips(message: Message):
    raw_list = [msg async for msg in userge.get_chat_history("Knowledge_Facts_Quotes_Reddit")]
    try:
        raw_message = choice(raw_list)
        pru_text = raw_message.text
        while "Pro Tip" not in pru_text:
            raw_message = choice(raw_list)
            pru_text = raw_message.text
        await message.edit(pru_text)
    # None Type Error 😴🙃
    except Exception:
        await message.edit("I Ran Out of Tips.")


HELLOSTR = (
    "Hi !", "‘Ello, gov'nor!", "What’s crackin’?", "‘Sup, homeslice?", "Howdy, howdy ,howdy!",
    "Hello, who's there, I'm talking.", "You know who this is.", "Yo!", "Whaddup.",
    "Greetings and salutations!", "Hello, sunshine!", "Hey, howdy, hi!",
    "What’s kickin’, little chicken?", "Peek-a-boo!", "Howdy-doody!",
    "Hey there, freshman!", "I come in peace!", "Ahoy, matey!", "Hiya!")

ITEMS = (
    "cast iron skillet", "large trout", "baseball bat", "cricket bat", "wooden cane", "nail",
    "printer", "shovel", "pair of trousers", "CRT monitor", "diamond sword", "baguette",
    "physics textbook", "toaster", "portrait of Richard Stallman", "television", "mau5head",
    "five ton truck", "roll of duct tape", "book", "laptop", "old television",
    "sack of rocks", "rainbow trout", "cobblestone block", "lava bucket", "rubber chicken",
    "spiked bat", "gold block", "fire extinguisher", "heavy rock", "chunk of dirt",
    "beehive", "piece of rotten meat", "bear", "ton of bricks")

RUNS_STR = (
    "Runs to Thanos..",
    "Runs far, far away from earth..",
    "Running faster than Bolt coz i'mma userbot !!",
    "Runs to Marie..",
    "This Group is too cancerous to deal with.",
    "Cya bois",
    "Kys",
    "I go away",
    "I am just walking off, coz me is too fat.",
    "I Fugged off!",
    "Will run for chocolate.",
    "I run because I really like food.",
    "Running...\nbecause dieting is not an option.",
    "Wicked fast runnah",
    "If you wanna catch me, you got to be fast...\nIf you wanna stay with me, "
    "you got to be good...\nBut if you wanna pass me...\nYou've got to be kidding.",
    "Anyone can run a hundred meters, it's the next forty-two thousand and two hundred that count.",
    "Why are all these people following me?",
    "Are the kids still chasing me?",
    "Running a marathon...there's an app for that.")

SLAP_TEMPLATES = (
    "{hits} {victim} with a {item}.",
    "{hits} {victim} in the face with a {item}.",
    "{hits} {victim} around a bit with a {item}.",
    "{throws} a {item} at {victim}.",
    "grabs a {item} and {throws} it at {victim}'s face.",
    "{hits} a {item} at {victim}.", "{throws} a few {item} at {victim}.",
    "grabs a {item} and {throws} it in {victim}'s face.",
    "launches a {item} in {victim}'s general direction.",
    "sits on {victim}'s face while slamming a {item} {where}.",
    "starts slapping {victim} silly with a {item}.",
    "pins {victim} down and repeatedly {hits} them with a {item}.",
    "grabs up a {item} and {hits} {victim} with it.",
    "starts slapping {victim} silly with a {item}.",
    "holds {victim} down and repeatedly {hits} them with a {item}.",
    "prods {victim} with a {item}.",
    "picks up a {item} and {hits} {victim} with it.",
    "ties {victim} to a chair and {throws} a {item} at them.",
    "{hits} {victim} {where} with a {item}.",
    "ties {victim} to a pole and whips them {where} with a {item}."
    "gave a friendly push to help {victim} learn to swim in lava.",
    "sent {victim} to /dev/null.", "sent {victim} down the memory hole.",
    "beheaded {victim}.", "threw {victim} off a building.",
    "replaced all of {victim}'s music with Nickelback.",
    "spammed {victim}'s email.", "made {victim} a knuckle sandwich.",
    "slapped {victim} with pure nothing.",
    "hit {victim} with a small, interstellar spaceship.",
    "quickscoped {victim}.", "put {victim} in check-mate.",
    "RSA-encrypted {victim} and deleted the private key.",
    "put {victim} in the friendzone.",
    "slaps {victim} with a DMCA takedown request!")


INSULT_STRINGS = (
    "Owww ... Such a stupid idiot.",
    "Don't drink and type.",
    "I think you should go home or better a mental asylum.",
    "Command not found. Just like your brain.",
    "Do you realize you are making a fool of yourself? Apparently not.",
    "You can type better than that.",
    "Bot rule 544 section 9 prevents me from replying to stupid humans like you.",
    "Sorry, we do not sell brains.",
    "Believe me you are not normal.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
    "Zombies eat brains... you're safe.",
    "You didn't evolve from apes, they evolved from you.",
    "Come back and talk to me when your I.Q. exceeds your age.",
    "I'm not saying you're stupid, I'm just saying you've got bad luck when it comes to thinking.",
    "What language are you speaking? Cause it sounds like bullshit.",
    "Stupidity is not a crime so you are free to go.",
    "You are proof that evolution CAN go in reverse.",
    "I would ask you how old you are but I know you can't count that high.",
    "As an outsider, what do you think of the human race?",
    "Brains aren't everything. In your case they're nothing.",
    "Ordinarily people live and learn. You just live.",
    "I don't know what makes you so stupid, but it really works.",
    "Keep talking, someday you'll say something intelligent! (I doubt it though)",
    "Shock me, say something intelligent.",
    "Your IQ's lower than your shoe size.",
    "Alas! Your neurotransmitters are no more working.",
    "Are you crazy you fool.",
    "Everyone has the right to be stupid but you are abusing the privilege.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.",
    "You should try tasting cyanide.",
    "Your enzymes are meant to digest rat poison.",
    "You should try sleeping forever.",
    "Pick up a gun and shoot yourself.",
    "You could make a world record by jumping from a plane without parachute.",
    "Stop talking BS and jump in front of a running bullet train.",
    "Try bathing with Hydrochloric Acid instead of water.",
    "Try this: if you hold your breath underwater for an hour, you can then hold it forever.",
    "Go Green! Stop inhaling Oxygen.",
    "God was searching for you. You should leave to meet him.",
    "give your 100%. Now, go donate blood.",
    "Try jumping from a hundred story building but you can do it only once.",
    "You should donate your brain seeing that you never used it.",
    "Volunteer for target in an firing range.",
    "Head shots are fun. Get yourself one.",
    "You should try swimming with great white sharks.",
    "You should paint yourself red and run in a bull marathon.",
    "You can stay underwater for the rest of your life without coming back up.",
    "How about you stop breathing for like 1 day? That'll be great.",
    "Try provoking a tiger while you both are in a cage.",
    "Have you tried shooting yourself as high as 100m using a canon.",
    "You should try holding TNT in your mouth and igniting it.",
    "Try playing catch and throw with RDX its fun.",
    "I heard phogine is poisonous but i guess you wont mind inhaling it for fun.",
    "Launch yourself into outer space while forgetting oxygen on Earth.",
    "You should try playing snake and ladders, with real snakes and no ladders.",
    "Dance naked on a couple of HT wires.",
    "Active Volcano is the best swimming pool for you.",
    "You should try hot bath in a volcano.",
    "Try to spend one day in a coffin and it will be yours forever.",
    "Hit Uranium with a slow moving neutron in your presence. It will be a worthwhile experience.",
    "You can be the first person to step on sun. Have a try.")

EMOJIS = (
    "😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕",
    "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰")


async def check_and_send(message: Message, *args, **kwargs):
    replied = message.reply_to_message
    if replied:
        await asyncio.gather(
            message.delete(),
            replied.reply(*args, **kwargs)
        )
    else:
        await message.edit(*args, **kwargs)


@userge.on_cmd("run$", about={'header': "Let Me Run, run, RUNNN!"})
async def run_(message: Message):
    """run"""
    await check_and_send(message, choice(RUNS_STR), parse_mode=enums.ParseMode.HTML)


THROW = ("throws", "flings", "chucks", "hurls")

HIT = ("hits", "whacks", "slaps", "smacks", "bashes")

WHERE = ("in the chest", "on the head", "on the butt", "on the crotch")

