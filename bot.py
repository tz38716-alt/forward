import logging
import asyncio
from telethon import TelegramClient, events

# ==========================================
# ဒီနေရာမှာ သင့်ရဲ့ အချက်အလက်တွေကို အစားထိုးထည့်ပါ
# ==========================================
# my.telegram.org က ရယူထားသော api_id နှင့် api_hash ကို ထည့်ပါ
API_ID = 31809374       # ဒီမှာ_API_ID_ကို_နံပါတ်သက်သက်_ထည့်ပါ
API_HASH = "9e3026dd9f9782e4c0002c983d1d11f9"

# Channel ID (ဥပမာ- -1001234567890) သို့မဟုတ် Channel Username (ဥပမာ- @mychannel)
SOURCE_CHANNEL = -1003112957551 

# Target Group ID သို့မဟုတ် Username (ဥပမာ- @mygroup)
# Group တစ်ခုထက်ပိုလျှင် list အနေနဲ့ ထည့်နိုင်သည် (ဥပမာ- [-1001, -1002])
TARGET_GROUPS = [-1003846424175,-1002406439028,-1002671928957,-4228882675,-1002655965539,-1002591014764,-1002463316379,-1002223995771,-1001598902234,-1002570768719,-1001543457827,-1002609139187,-1002193077894,-1002654408680,-1001919577491,-1001505230054,-1003253017807,-1003408809703] 

INTERVAL = 1800  # ၃၀ မိနစ် (စက္ကန့် ၁၈၀၀)
# ==========================================

# Enable logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the client (session_name က login state ကို သိမ်းထားပေးမှာပါ)
client = TelegramClient('my_session', API_ID, API_HASH)

async def infinite_forward(event, group_id, interval):
    """၃၀ မိနစ်ခြားပြီး အကန့်အသတ်မရှိ forward လုပ်ပေးခြင်း (User Account သုံး၍)"""
    count = 1
    message_id = event.message.id
    channel_id = event.chat_id
    
    while True:
        try:
            # Message ကို forward လုပ်ခြင်း
            await client.forward_messages(group_id, message_id, channel_id)
            logger.info(f"Attempt {count}: Forwarded message {message_id} to {group_id}")
            count += 1
            # ၃၀ မိနစ် စောင့်ခြင်း
            await asyncio.sleep(interval)
        except Exception as e:
            logger.error(f"Error forwarding to {group_id}: {e}")
            # Error တက်ရင် ၁ မိနစ်ခန့်စောင့်ပြီး ပြန်ကြိုးစားခြင်း
            await asyncio.sleep(60)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    """Channel မှာ Post အသစ်တင်တာနဲ့ Loop ကို စတင်ခြင်း"""
    logger.info(f"New post detected in channel {SOURCE_CHANNEL}. Starting 30-minute forward loop...")
    
    # Target groups အားလုံးအတွက် Loop စတင်ခြင်း
    for group_id in TARGET_GROUPS:
        asyncio.create_task(infinite_forward(event, group_id, INTERVAL))

async def main():
    """Client ကို စတင်ခြင်း"""
    print("Userbot စတင်နေပါပြီ...")
    await client.start()
    print("Userbot အလုပ်လုပ်နေပါပြီ။ Channel မှာ Post တင်တာနဲ့ ၃၀ မိနစ်ခြားပြီး Forward လုပ်ပေးပါလိမ့်မယ်။")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
