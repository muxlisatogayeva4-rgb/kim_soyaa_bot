import os
import telebot
import yt_dlp

TOKEN = "8727117906:AAGT9OZ2iKW3NZF4Nz_sS9YonwAyTMK4S4U"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Assalomu alaykum! YouTube'dan qo'shiq qidirish uchun istalgan qo'shiq"
      " nomini yozing. 🎧",
  )


@bot.message_handler(func=lambda message: True, content_types=["text"])
def search_and_send_youtube(message):
  query = message.text
  msg = bot.reply_to(
      message, "🔍 YouTube'dan qidirilmoqda, iltimos kuting..."
  )

  ydl_opts = {
      "format": "bestaudio/best",
      "postprocessors": [{
          "key": "FFmpegExtractAudio",
          "preferredcodec": "mp3",
          "preferredquality": "192",
      }],
      "outtmpl": "song.%(ext)s",
      "default_search": "ytsearch1",
      "noplaylist": True,
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(query, download=True)
      filename = "song.mp3"

      with open(filename, "rb") as audio:
        bot.send_audio(
            message.chat.id,
            audio,
            caption=f"🎵 Topildi: {info.get('titlfixe', 'Musiqa')}",
        )

      os.remove(filename)
      bot.delete_message(message.chat.id, msg.message_id)

  except Exception as e:
    bot.edit_message_text(
        "Kechirasiz, bu qo'shiqni topishda xatolik yuz berdi yoki hech narsa"
        " topilmadi.",
        message.chat.id,
        msg.message_id,
    )


bot.infinity_polling()
