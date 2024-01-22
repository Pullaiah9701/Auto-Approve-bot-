from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver","my_app",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    'https://telegra.ph/file/a5a2bb456bf3eecdbbb99.mp4',
    'https://telegra.ph/file/03c6e49bea9ce6c908b87.mp4',
    'https://telegra.ph/file/9ebf412f09cd7d2ceaaef.mp4',
    'https://telegra.ph/file/293cc10710e57530404f8.mp4',
    'https://telegra.ph/file/506898de518534ff68ba0.mp4',
    'https://telegra.ph/file/dae0156e5f48573f016da.mp4',
    'https://telegra.ph/file/3e2871e714f435d173b9e.mp4',
    'https://telegra.ph/file/714982b9fedfa3b4d8d2b.mp4',
    'https://telegra.ph/file/876edfcec678b64eac480.mp4',
    'https://telegra.ph/file/6b1ab5aec5fa81cf40005.mp4',
    'https://telegra.ph/file/b4834b434888de522fa49.mp4'
]


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m : Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        await app.send_video(kk.id,img, "**Hello {}!\nWelcome To {}\n\nPowerd By : @PanindiaFilmZ**".format(m.from_user.mention, m.chat.title))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ pyrogram ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Initialize your Pyrogram client

# Define the source and destination chat IDs
source_chat_id = -1001234567890  # Replace with your source chat ID
destination_chat_id = -1009876543210  # Replace with your destination chat ID

# Forward messages from any chat to the destination chat
@app.on_message(filters.chat(source_chat_id))
def forward_message(client, message):
    client.forward_messages(destination_chat_id, message.chat.id, message.message_id)

# Forward messages from multiple chats to the destination chat
@app.on_message(filters.chat([source_chat_id, -1001111111111, -1002222222222]))  # Add additional chat IDs as needed
def forward_message(client, message):
    client.forward_messages(destination_chat_id, message.chat.id, message.message_id)

# Filter messages based on type or keywords
@app.on_message(filters.chat(source_chat_id) & (filters.photo | filters.document | filters.voice))
def filter_messages(client, message):
    # Add your filtering logic here
    # For example, you can check if the message contains a specific keyword
    if "keyword" in message.text:
        client.forward_messages(destination_chat_id, message.chat.id, message.message_id)

# Clone chats from source to destination
@app.on_message(filters.chat(source_chat_id))
def clone_chat(client, message):
    # Add your cloning logic here
    # For example, you can forward the entire chat history to the destination chat
    client.forward_messages(destination_chat_id, message.chat.id, message.message_id)

# Enable message duplicate filtering
@app.on_message(filters.chat(source_chat_id))
def filter_duplicates(client, message):
    # Add your duplicate filtering logic here
    # For example, you can keep track of message IDs and ignore duplicates
    if message.message_id not in processed_message_ids:
        client.forward_messages(destination_chat_id, message.chat.id, message.message_id)
        processed_message_ids.append(message.message_id)
        
# Start the Pyrogram client
app.run()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/PanindiaFilmZ"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/PIFDeals")
                    ],[
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/AutoAcceptRequest32_bot?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo("https://graph.org/file/18091323ff1c954bb5c97.jpg", caption="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\nPowerd By : @PanindiaFilmZ**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)
    
        elif m.chat.type == enums.ChatType.GROUP or enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/AutoAcceptRequest32_bot?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("**🦊 Hello {}!\nwrite me private for more details**".format(m.from_user.first_name), reply_markup=keyboar)
        print(m.from_user.first_name +" Is started Your Bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", "chk")
                ]
            ]
        )
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join @{} to use me.If you joined click check again button to confirm.**".format(cfg.FSUB), reply_markup=key)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/PanindiaFilmZ"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/PIFDeals")
                    ],[
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/AutoAcceptRequest32_bot?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\nPowerd By : @PanindiaFilmZ**".format(cb.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name +" Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Join Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("PanindiaFilmZ"))
async def PanindiaFilmZ_command(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = [
                [
                    InlineKeyboardButton("🍁 ᴛᴀᴍɪʟ - ᴋᴀɴɴᴀᴅᴀ 🎖️", url="https://t.me/+mGplIsWLBsNmMzdl")
                ],
                [
                    InlineKeyboardButton("🧞‍♀️ ʜɪɴᴅɪ - ᴍᴀʟᴀʏᴀʟᴀᴍ 🧐", url="https://t.me/+Oc2rrg_Kl0hiN2Jl"),
                    InlineKeyboardButton("🔔 ᴘᴀɴɪɴᴅɪᴀꜰɪʟᴍᴢ 🤖", url="https://t.me/PanindiaFilmZ")
                ],
                [
                    InlineKeyboardButton("🛒 ᴅᴇᴀʟꜱ 🦾", url="https://t.me/PIFDeals"),
                    InlineKeyboardButton("🥵 ʀᴀʀᴇ ʜɪᴅᴅᴇɴ ᴍᴏᴠɪᴇꜱ ♥️", url="https://t.me/PIFRareHiddenMovies")
                ],
                [
                    InlineKeyboardButton("🔗 ʙᴏᴛᴢ ᴀʀᴇᴀ", url="https://t.me/BoTzUpdates0"),
                    InlineKeyboardButton("⚙ ᴍᴏᴠɪᴇꜱ ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/PIFOficial")
                ],
                [
                    InlineKeyboardButton("⪦ ᴍᴏᴠɪᴇs ʀᴇǫᴜᴇsᴛ ɢʀᴏᴜᴘ ⪧", url="https://t.me/+37-TDCcQqltlOTRl")
                ]
            ]
 
            reply_markup = InlineKeyboardMarkup(keyboard)
            await m.reply("""**🙃 __Welcome To My PanindiaFilmZ Community!! Cheak Our Channels & Groups List Below!!**__

__**Hi.. PanindiaFilmZ Admin, I Can Provide My Channels Invite links** __

__**🌟 #PANINDIAFILMZ #OURMENIA 3D~EXP🔥 **__

**__✨  PIF Deals 24/7 :- 
@PIFDeals__**

**__✨ Rare Hidden Adult Movies 2.0 
@Telugu_Adults_Rare_Hidden_Movies__**

**__✨ PIF Fitter Bot :-
 @PanindiaFilmz_bot__**

**__✨ BoTz Updates :-
 @BoTzUpdates0__**

**__✨ File's Added Updates :- 
 @PIFOficial__**

__**© ᴀʟʟ ᴄᴏᴘʏʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ ᴛᴏ ᴍᴏᴠɪᴇ ᴏᴡɴᴇʀꜱ ᴏɴʟʏ !!**__

__**ᴀʟʟ ʟᴀɴɢᴜᴀɢᴇ ɴᴇᴡ ᴍᴏᴠɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ | தமிழ் | తెలుగు | हिंदी | മലയാളം | ಕನ್ |**__

__**Target - Reaching ur Self 🎯**__

__**For Any Queries - @PanIndia_Flimz_Admin_bot**__

__**@PanindiaFilmZ 🔥**__""", reply_markup=reply_markup)
 
    except Exception as e:
        print(f"Error: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

@app.on_message(filters.chat(-1001947425388))
async def forward_channel_post(_, message):
    # Get the chat ID of the bot
    bot_chat = await app.get_chat(chat_id=message.chat.id)
    
    # Forward the message from the channel to the bot
    await app.copy_message(chat_id=bot_chat.id, from_chat_id=message.chat.id, message_id=message.message_id.message_id)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
