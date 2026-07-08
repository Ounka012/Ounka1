import os
import yt_dlp
import time
import re
import tempfile
import uuid
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from langdetect import detect
from deep_translator import GoogleTranslator
import edge_tts

# ================== កំណត់ Token របស់ Bot ==================
BOT_TOKEN = "8623945913:AAFJMhq2azWjvSmr6pNRN_kMNNeSlTXae6E"

# សំឡេងសម្រាប់ភាសាខ្មែរ (Sreymom Neural)
KHMER_VOICE = "km-KH-SreymomNeural"
# សំឡេងសម្រាប់ភាសាអង់គ្លេស (Aria Neural) - ទុកបម្រុង បើមិនត្រូវការកុំប្រើ
ENGLISH_VOICE = "en-US-AriaNeural"

# ================== មុខងារជំនួយ ==================
def is_url(text: str) -> bool:
    """ពិនិត្យថាតើអត្ថបទជា URL រឺអត់"""
    url_pattern = re.compile(
        r'^(https?://)?'                     # http:// or https://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})' # domain
        r'(:\d+)?(/.*)?$'                    # optional port & path
    )
    return bool(url_pattern.match(text))

async def text_to_speech(text: str, voice: str = KHMER_VOICE) -> str:
    """
    បម្លែងអត្ថបទទៅជាឯកសារ MP3 បណ្ដោះអាសន្ន
    ប្រើ Microsoft Edge TTS (edge-tts)
    ត្រឡប់ផ្លូវឯកសារ .mp3
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(tmp_file.name)
    return tmp_file.name

# ================== Handler សំខាន់ ==================
async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # -------- បើជា URL → ទាញយក MP3 --------
    if is_url(text):
        await update.message.reply_text("⏳ កំពុងទាញយក MP3...")

        # ឈ្មោះឯកសារមានលក្ខណៈចៃដន្យដើម្បីជៀសវាងការប៉ះទង្គិច
        filename = f"audio_{int(time.time())}_{uuid.uuid4().hex[:6]}"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": filename + ".%(ext)s",
            "socket_timeout": 60,
            "retries": 5,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(text, download=True)

            mp3_file = filename + ".mp3"
            if not os.path.exists(mp3_file):
                await update.message.reply_text("❌ មិនអាចរកឃើញឯកសារ MP3")
                return

            # ផ្ញើឯកសារជាសំឡេង
            with open(mp3_file, "rb") as audio:
                await update.message.reply_audio(audio=audio)

            # លុបឯកសារចោលក្រោយផ្ញើ
            os.remove(mp3_file)

        except Exception as e:
            await update.message.reply_text(f"❌ មានបញ្ហា៖ {e}")
        return  # ចប់ URL handler

    # -------- បើមិនមែន URL → Text‑to‑Speech --------
    await update.message.reply_text("🔊 កំពុងបម្លែងអត្ថបទទៅជាសំឡេង...")

    try:
        # ស្គាល់ភាសារបស់អត្ថបទ
        detected_lang = detect(text)
        final_text = text
        voice = KHMER_VOICE

        # បើជាភាសាអង់គ្លេស → បកប្រែទៅខ្មែរ
        if detected_lang == 'en':
            translated = GoogleTranslator(source='auto', target='km').translate(text)
            final_text = translated
            voice = KHMER_VOICE
        # បើជាភាសាខ្មែរ (ឬភាសាផ្សេង) → និយាយដោយផ្ទាល់ជាមួយសំឡេងខ្មែរ
        # (អ្នកអាចផ្លាស់ប្ដូរជា voice = ENGLISH_VOICE បើចង់អានអង់គ្លេសផ្ទាល់)

        # បង្កើតឯកសារសំឡេង
        mp3_path = await text_to_speech(final_text, voice)

        # ផ្ញើឯកសារសំឡេង
        with open(mp3_path, "rb") as audio:
            await update.message.reply_audio(audio=audio)

        # លុបឯកសារបណ្ដោះអាសន្ន
        os.remove(mp3_path)

    except Exception as e:
        await update.message.reply_text(f"❌ មិនអាចបម្លែងជាសំឡេងបានទេ៖ {e}")

# ================== ចាប់ផ្ដើម Bot ==================
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    # Handler សម្រាប់អត្ថបទមិនមែនពាក្យបញ្ជា (/command)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_mp3))

    print("🤖 Bot បានចាប់ផ្ដើម... (URL Download + TTS Khmer)")
    app.run_polling()
