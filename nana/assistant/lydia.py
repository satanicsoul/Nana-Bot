import time

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI
from pyrogram import Filters

from nana import setbot, AdminSettings, lydia_api

lydia_status = False
coffeehouse_api = None
lydia = None
session = None


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["lydia"]))
async def lydia_stats(client, message):
    global lydia_status, coffeehouse_api, lydia, session
    if lydia_api == "":
        await message.reply("`lydia API key is not set!\nSet your lydia API key by adding Config Vars in heroku with "
                            "name lydia_api with value your lydia key API`")
        return
    if lydia_status:
        await message.reply("Turning off lydia...")
        time.sleep(0.5)
        lydia_status = False
        await message.reply("Lydia will not reply your message")
    else:
        await message.reply("Turning on lydia...")
        try:
            coffeehouse_api = API(lydia_api)
            # Create Lydia instance
            lydia = LydiaAI(coffeehouse_api)
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
        except:
            await message.reply("Wrong lydia API key!")
            return
        lydia_status = True
        await message.reply("now Lydia will reply your message!")


@setbot.on_message(Filters.user(AdminSettings))
async def lydia(client, message):
    global lydia_status, session
    if lydia_status:
        output = session.think_thought(message.text)
        await message.reply_text("`{0}`".format(output), quote=True)
    else:
        return
