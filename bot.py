from telethon import TelegramClient, events
import os

# 使用你的 API ID 和 API Hash
api_id = 你的ID
api_hash = '你的 API Hash'

# 创建一个新的 Telegram 客户端
client = TelegramClient('session_name', api_id, api_hash)

# 定义一个函数读取文本文件内容
def read_text_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return "文件不存在。"

# 定义触发关键词列表
keywords = ['拍照','摄影','车辆','收款码','商铺','店铺','赚钱','在家','已上压','就有钱','灵活','自由安排','二维码','拍','商家','收款','在家','80元','100元','暴力','商机','八十/','一百/','一张','一对一','盈利','定制服务']

# 定义白名单用户 ID 列表
whitelist = [162726000, 1668444000, 5902192000]   # 替换为实际的用户 ID 获取方式 网页 web.telegram.org 登录你的TG，然后要给谁白名单就点击他头像到跟他聊天的界面，注意看上面网址的变化，后面的数据就是ID，群组频道ID则是 -100xxxxx

# 登录
async def main():
    # 首次运行时需要输入电话号码和验证码
    await client.start()

    async def send_file_with_fallback(chat_id, file_path, caption, event=None):
        try:
            await client.send_file(chat_id, file_path, caption=caption, reply_to=event.id if event else None)
        except Exception as e:
            print(f"Failed to send file: {e}")
            await client.send_message(chat_id, caption, reply_to=event.id if event else None)

    @client.on(events.NewMessage)
    async def handler(event):
        # 检查用户是否在白名单中
        sender = await event.get_sender()
        if sender.id in whitelist:
            return

        # 预处理消息文本，去除多余的空格和特殊字符
        message_text = event.raw_text.replace(' ', '').replace('\n', '').replace('\r', '')

        # 检查消息中是否包含任意一个关键词
        if any(keyword.replace(' ', '').replace('\n', '').replace('\r', '') in message_text for keyword in keywords):
            # 读取 pianzi.txt 文件内容
            file_content = read_text_file('pianzi.txt')

            if event.is_group or event.is_channel:
                # 如果是在群组或频道中，回复消息
                await send_file_with_fallback(event.chat_id, 'zp.png', file_content, event)
            else:
                # 如果是私聊，直接发送消息
                await send_file_with_fallback(event.chat_id, 'zp.png', file_content)

        # 检查消息是否为 "你好"
        if '你好' in message_text:
            # 读取 pianzi.txt 文件内容
            file_content = read_text_file('pianzi.txt')

            # 私发 zp.png 缩图和 pianzi.txt 的内容给发送者
            await send_file_with_fallback(sender.id, 'zp.png', file_content)

    @client.on(events.ChatAction)
    async def user_joined(event):
        # 检查用户是否在白名单中
        if event.user_id in whitelist:
            return

        if event.user_added or event.user_joined:
            # 读取 pianzi.txt 文件内容
            file_content = read_text_file('pianzi.txt')

            # 私发 zp.png 缩图和 pianzi.txt 的内容给新用户
            await send_file_with_fallback(event.user_id, 'zp.png', file_content)

    print("Listening for messages and user actions...")
    await client.run_until_disconnected()

# 运行客户端
with client:
    client.loop.run_until_complete(main())
