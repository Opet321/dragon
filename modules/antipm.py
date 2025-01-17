#  Dragon-Userbot - telegram userbot
#  Copyright (C) 2020-present Dragon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.db import db
from utils.misc import modules_help, prefix

anti_pm_enabled = filters.create(
    lambda _, __, ___: db.get("core.antipm", "status", False)
)

in_contact_list = filters.create(lambda _, __, message: message.from_user.is_contact)

is_support = filters.create(lambda _, __, message: message.chat.is_support)



@Client.on_message(
    filters.private
    & ~filters.me
    & ~filters.bot
    & ~in_contact_list
    & ~is_support
    & anti_pm_enabled
)
async def anti_pm_handler(client: Client, message: Message):
    user_info = await client.resolve_peer(message.chat.id)
    if db.get("core.antipm", "spamrep", False):
        await client.send(functions.messages.ReportSpam(peer=user_info))
    if db.get("core.antipm", "block", False):
        await client.send(functions.contacts.Block(id=user_info))
    if db.get("core.antipm", "warn", False):
        await client.send_message(
            message.chat.id, "Harap tunggu sampai bos saya merespon atau anda akan di blokir dan di laporkan sebagai spam, tag saya di group !!"
        )
    await asyncio.sleep(10)
    await client.send(
        functions.messages.DeleteHistory(peer=user_info, max_id=0, revoke=True)
    )


@Client.on_message(filters.command(["antipm", "anti_pm"], prefix) & filters.me)
async def anti_pm(_, message: Message):
    if len(message.command) == 1:
        if db.get("core.antipm", "status", False):
            await message.edit(
                "<b>Anti-PM status: enabledn"
                f"Disable with: </b><code>{prefix}antipm disable</code>"
            )
        else:
            await message.edit(
                "<b>Anti-PM status: disabledn"
                f"Enable with: </b><code>{prefix}antipm enable</code>"
            )
    elif message.command[1] in ["enable", "on", "1", "yes", "true"]:
        db.set("core.antipm", "status", True)
        await message.edit("<b>Anti-PM enabled!</b>")
    elif message.command[1] in ["disable", "off", "0", "no", "false"]:
        db.set("core.antipm", "status", False)
        await message.edit("<b>Anti-PM disabled!</b>")
    elif message.command[1] in ["warn", "notification"]:
        db.set("core.antipm", "warn", True)
        await message.edit("<b>Anti-PM warning enabled!</b>")
    elif message.command[1] in ["nowarn", "nowarning"]:
        db.set("core.antipm", "warn", False)
        await message.edit("<b>Anti-PM warning disabled!</b>")
    else:
        await message.edit(f"<b>Usage: {prefix}antipm [enable|disable|warn|nowarn]</b>")
        







modules_help["antipm"] = {
    "antipm [enable|disable]*": "When enabled, deletes all messages from users who are not in the contact book",
    "antipm_report [enable|disable]*": "Enable spam reporting",
    "antipm_block [enable|disable]*": "Enable user blocking",
}
