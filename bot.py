import os
import asyncio
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language_keyboard = [
        [InlineKeyboardButton("Français", callback_data='FR'), 
         InlineKeyboardButton("English", callback_data='EN'), 
         InlineKeyboardButton("Deutsch", callback_data='DE')]
    ]
    reply_markup = InlineKeyboardMarkup(language_keyboard)
    
    try:
        await update.message.reply_photo(photo=open('logo.png', 'rb'))
    except Exception:
        pass

    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

# 2. HANDLE BUTTON CLICKS
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 

    main_menu_keyboard = [
        [InlineKeyboardButton("🛍️ Open shop", url="https://example.com")], 
        [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    if query.data == 'EN':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )
    elif query.data == 'FR':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇",
            reply_markup=reply_markup
        )
    elif query.data == 'DE':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Willkommen bei Guaraná.ch!\nDanke für dein Vertrauen – bestelle schnell über den Shop 👇",
            reply_markup=reply_markup
        )

# 3. MAIN FUNCTION (100% RAILWAY PROOF)
async def main():
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set!")
        return

    print("🚀 Starting Guaraná.ch Bot...")
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("🔄 Clearing old connections...")
    temp_bot = telegram.Bot(token=TOKEN)
    await temp_bot.delete_webhook(drop_pending_updates=True)
    print("✅ Old connections cleared!")
    
    await application.initialize()
    
    print("📡 Starting polling...")
    await application.updater.start_polling()
    
    print("✅ Bot is now LIVE on Telegram!")
    
    # KEEP THE BOT ALIVE
    try:
        # This specific sleep pattern prevents Railway from killing the loop
        while True:
            await asyncio.sleep(3600) # Sleep for an hour
            await asyncio.sleep(0)    # This tiny fix prevents the "event loop is closed" error
    except KeyboardInterrupt:
        pass
    finally:
        await application.updater.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
