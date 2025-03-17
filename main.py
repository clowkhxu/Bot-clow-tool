import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from utils import get_random_user, generate_cards_from_bin, COUNTRY_MAP, COUNTRY_EMOJI
from spammer import SMSSpammer

# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Lấy token bot từ biến môi trường
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# Khởi tạo bot với intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot đã đăng nhập với tên {bot.user}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Đã đồng bộ {len(synced)} lệnh slash")
    except Exception as e:
        logger.error(f"Lỗi khi đồng bộ lệnh: {e}")


# Các lệnh slash
@bot.tree.command(name="start",
                  description="Hiển thị thông tin giới thiệu về bot")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🤖 **Chào mừng bạn đến với Bot Đa Năng!**\n\n"
        "👉 Dùng `/fake` để tạo thông tin giả.\n"
        "👉 Dùng `/gen` để tạo số thẻ tín dụng.\n"
        "👉 Dùng `/spam` để spam SMS.\n\n"
        "Xem danh sách quốc gia: `/help_fake`")


@bot.tree.command(name="fake", description="Tạo thông tin người dùng giả")
@app_commands.describe(country_code="Mã quốc gia (vd: us, gb, fr)")
async def fake_command(interaction: discord.Interaction, country_code: str):
    country_code = country_code.lower()
    if country_code not in COUNTRY_MAP:
        await interaction.response.send_message(
            "Mã quốc gia không hỗ trợ. Xem `/help_fake`.")
        return

    user_data = get_random_user(country_code)
    if not user_data or "results" not in user_data or not user_data["results"]:
        await interaction.response.send_message(
            "Không thể lấy thông tin người dùng. Thử lại sau.")
        return

    user = user_data["results"][0]
    emoji = COUNTRY_EMOJI.get(country_code, "")
    response = f'👤 **THÔNG TIN CÁ NHÂN {emoji}**\n\n'
    response += f"**Họ tên**: {user['name']['title']} {user['name']['first']} {user['name']['last']}\n"
    response += f"**Đường phố**: {user['location']['street']['number']} {user['location']['street']['name']}\n"
    response += f"**Thành phố**: {user['location']['city']}\n"
    response += f"**Tiểu bang/Tỉnh**: {user['location']['state']}\n"
    response += f"**Mã bưu điện**: {user['location']['postcode']}\n"
    response += f"**Quốc gia**: {user['location']['country']}\n"

    await interaction.response.send_message(response)


@bot.tree.command(name="gen", description="Tạo số thẻ tín dụng dựa trên BIN")
@app_commands.describe(bin_code="Mã BIN (số lượng bất kỳ)",
                       count="Số lượng thẻ (tối đa 20)")
async def gen_command(interaction: discord.Interaction,
                      bin_code: str,
                      count: int = 5):
    # Kiểm tra BIN hợp lệ
    if not bin_code.isdigit():
        await interaction.response.send_message(
            'Mã BIN không hợp lệ. Vui lòng chỉ nhập số.')
        return

    # Kiểm tra BIN không dài hơn 15 số
    if len(bin_code) > 15:
        await interaction.response.send_message(
            'Mã BIN quá dài. Vui lòng nhập ít hơn 16 số.')
        return

    # Giới hạn số lượng thẻ
    count = min(int(count), 20)

    try:
        # Tạo số thẻ từ BIN
        cards = generate_cards_from_bin(bin_code, count)
        response = f"💳 **THẺ TỪ BIN {bin_code}**\n\n"
        for card in cards:
            response += f"{card['number']}|{card['expiry_month']}|{card['expiry_year']}|{card['cvv']}\n"

        await interaction.response.send_message(response)
    except Exception as e:
        await interaction.response.send_message(f'Lỗi: {str(e)}')


@bot.tree.command(name="spam", description="Thực hiện spam SMS")
@app_commands.describe(phone="Số điện thoại cần spam",
                       count="Số lần spam (tối đa 20)")
async def spam_command(interaction: discord.Interaction, phone: str,
                       count: int):
    # Kiểm tra số điện thoại hợp lệ
    if not phone.isdigit() or len(phone) < 9 or len(phone) > 11:
        await interaction.response.send_message(
            "Số điện thoại không hợp lệ! Vui lòng nhập số điện thoại đúng định dạng."
        )
        return

    # Kiểm tra số lần spam hợp lệ
    if count <= 0:
        await interaction.response.send_message(
            "Số lần spam không hợp lệ! Vui lòng nhập một số nguyên dương.")
        return

    count = min(count, 20)  # Giới hạn tối đa 20 lần spam

    # Chuẩn hóa số điện thoại
    if phone.startswith("0"):
        phone = phone[1:]

    user_name = interaction.user.display_name
    initial_message = f"┌──────⭓ Clow_Ponkey\n│ Spam: Đang thực hiện\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count}\n│ Đang Tấn Công: {phone}\n└─────────────"

    await interaction.response.send_message(initial_message)
    progress_msg = await interaction.original_response()

    try:
        spammer = SMSSpammer()
        await spammer.run_spam_async(phone, count, user_name, progress_msg)
    except Exception as e:
        await interaction.followup.send(f"❌ Lỗi: {str(e)}")


@bot.tree.command(name="help_fake",
                  description="Hiển thị danh sách các quốc gia được hỗ trợ")
async def help_fake_command(interaction: discord.Interaction):
    response = '🌎 **Quốc gia hỗ trợ:**\n\n'
    for code, name in sorted(COUNTRY_MAP.items()):
        emoji = COUNTRY_EMOJI.get(code, '')
        response += f"{emoji} `{code}` - {name}\n"

    await interaction.response.send_message(response)


@bot.tree.command(name="help", description="Hiển thị danh sách lệnh")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "/fake `country_code` - Tạo thông tin giả.\n"
        "/gen `bin_code` `count` - Tạo số thẻ tín dụng.\n"
        "/spam `phone` `count` - Spam SMS.\n\n"
        "Xem danh sách quốc gia: `/help_fake`")


# Khởi động bot
def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
