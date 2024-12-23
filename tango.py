from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import transmission_rpc

# Telegram Bot Token
BOT_TOKEN = ""

# Allowed Telegram User IDs
ALLOWED_USER_IDS = []

# Configure Transmission RPC
TRANSMISSION_HOST = "localhost"
TRANSMISSION_PORT = 9091
TRANSMISSION_USER = ""
TRANSMISSION_PASS = ""

client = transmission_rpc.Client(
    host=TRANSMISSION_HOST,
    port=TRANSMISSION_PORT,
    username=TRANSMISSION_USER,
    password=TRANSMISSION_PASS,
)


def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS


async def add_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("Unauthorized user.")
        return

    if context.args:
        torrent_path = " ".join(context.args)
        try:
            client.add_torrent(torrent_path)
            await update.message.reply_text(f"Torrent added: {torrent_path}")
        except Exception as e:
            await update.message.reply_text(f"Error adding torrent: {e}")
    else:
        await update.message.reply_text("Usage: /add <torrent_file_or_url>")


async def list_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("Unauthorized user.")
        return

    try:
        torrents = client.get_torrents()
        if not torrents:
            await update.message.reply_text("No active torrents.")
            return

        response = "\n".join(
            [
                f"ID: {t.id}, Hash: {t.hashString}, Name: {t.name}, Progress: {t.progress:.2f}%"
                for t in torrents
            ]
        )
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error listing torrents: {e}")


async def remove_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("Unauthorized user.")
        return

    if context.args:
        torrent_id = context.args[0]
        try:
            client.remove_torrent(torrent_id, delete_data=False)
            await update.message.reply_text(f"Removed torrent with ID: {torrent_id}")
        except Exception as e:
            await update.message.reply_text(f"Error removing torrent: {e}")
    else:
        await update.message.reply_text("Usage: /remove <torrent_id>")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("add", add_torrent))
    application.add_handler(CommandHandler("list", list_torrents))
    application.add_handler(CommandHandler("remove", remove_torrent))

    application.run_polling()


if __name__ == "__main__":
    main()
