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
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.db import db
from utils.misc import modules_help, prefix

anti_pm_enabled = filters.create(
    lambda _, __, ___: db.get("core.antipm", "status", False)
)

in_contact_list = filters.create(lambda _, __, message: message.from_user.is_contact)

is_support = filters.create(lambda _, __, message: message.chat.is_support

@Client.on_message(
    filters.private
    & ~filters.me
    & ~filters.bot
    & ~in_contact_list
    & ~is_support
    & anti_pm_enabled
)
async def anti_pm_handler(client, message):
    user_info = message.chat.id
    if db.get("core.antipm", "spamrep", False):
        await client.report_spam(user_id=user_info)
    if db.get("core.antipm", "block", False):
        await client.block_user(user_id=user_info)
    msg = await client.send_message(
        chat_id=user_info,
        text="Apakah Anda setuju untuk menghapus riwayat chat ini? Balas dengan 'Ya' atau 'Tidak'."
    )
    response = await client.listen(message.chat.id)
    if response.text == "Ya":
        await client.delete_messages(chat_id=user_info, message_ids=msg.message_id)
        await client.send_message(chat_id=user_info, text="Riwayat chat telah dihapus.")
    elif response.text == "Tidak":
        await client.send_message(chat_id=user_info, text="Anda tidak setuju untuk menghapus riwayat chat.")



@Client.on_message(filters.command(["antipm", "anti_pm"], prefix) & filters.me)
async def anti_pm(_, message: Message):
    if len(message.command) == 1:
        if db.get("core.antipm", "status", False):
            await message.edit(
                "<b>Anti-PM status: enabled\n"
                f"Disable with: </b><code>{prefix}antipm disable</code>"
            )
        else:
            await message.edit(
                "<b>Anti-PM status: disabled\n"
                f"Enable with: </b><code>{prefix}antipm enable</code>"
            )
    elif message.command[1] in ["enable", "on", "1", "yes", "true"]:
        db.set("core.antipm", "status", True)
        await message.edit("<b>Anti-PM enabled!</b>")
    elif message.command[1] in ["disable", "off", "0", "no", "false"]:
        db.set("core.antipm", "status", False)
        await message.edit("<b>Anti-PM disabled!</b>")
    else:
        await message.edit(f"<b>Usage: {prefix}antipm [enable|disable]</b>")


@Client.on_message(filters.command(["antipm_report"], prefix) & filters.me)
async def antipm_report(_, message: Message):
    if len(message.command) == 1:
        if db.get("core.antipm", "spamrep", False):
            await message.edit(
                "<b>Spam-reporting enabled.\n"
                f"Disable with: </b><code>{prefix}antipm_report disable</code>"
            )
        else:
            await message.edit(
                "<b>Spam-reporting disabled.\n"
                f"Enable with: </b><code>{prefix}antipm_report enable</code>"
            )
    elif message.command[1] in ["enable", "on", "1", "yes", "true"]:
        db.set("core.antipm", "spamrep", True)
        await message.edit("<b>Spam-reporting enabled!</b>")
    elif message.command[1] in ["disable", "off", "0", "no", "false"]:
        db.set("core.antipm", "spamrep", False)
        await message.edit("<b>Spam-reporting disabled!</b>")
    else:
        await message.edit(f"<b>Usage: {prefix}antipm_report [enable|disable]</b>")


@Client.on_message(filters.command(["antipm_block"], prefix) & filters.me)
async def antipm_block(_, message: Message):
    if len(message.command) == 1:
        if db.get("core.antipm", "block", False):
            await message.edit(
                "<b>Blocking users enabled.\n"
                f"Disable with: </b><code>{prefix}antipm_block disable</code>"
            )
        else:
            await message.edit(
                "<b>Blocking users disabled.\n"
                f"Enable with: </b><code>{prefix}antipm_block enable</code>"
            )
    elif message.command[1] in ["enable", "on", "1", "yes", "true"]:
        db.set("core.antipm", "block", True)
        await message.edit("<b>Blocking users enabled!</b>")
    elif message.command[1] in ["disable", "off", "0", "no", "false"]:
        db.set("core.antipm", "block", False)
        await message.edit("<b>Blocking users disabled!</b>")
    else:
        await message.edit(f"<b>Usage: {prefix}antipm_block [enable|disable]</b>")


modules_help["antipm"] = {
    "antipm [enable|disable]*": "When enabled, deletes all messages from users who are not in the contact book",
    "antipm_report [enable|disable]*": "Enable spam reporting",
    "antipm_block [enable|disable]*": "Enable user blocking",
}
