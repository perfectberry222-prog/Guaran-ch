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
    
    # Send logo
    try:
        await update.message.reply_photo(photo=open('logo.png', 'rb'))
    except Exception:
        pass # Skip error if image isn't found

    # Send French welcome
    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

# 2. HANDLE BUTTON CLICKS
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 

    # The 2 buttons
    main_menu_keyboard = [
        [InlineKeyboardButton("🛍️ Open shop", url="https://example.com")], 
        [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    # --- ENGLISH ---
    if query.data == 'EN':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )

    # --- FRENCH ---
    elif query.data == 'FR':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇",
            reply_markup=reply_markup
        )

    # --- GERMAN ---
    elif query.data == 'DE':
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception:
            pass
        await query.message.reply_text(
            text="🤗 Willkommen bei Guaraná.ch!\nDanke für dein Vertrauen – bestelle schnell über den Shop 👇",
            reply_markup=reply_markup
        )

# 3. MAIN ASYNC FUNCTION (Railway Safe)
async def main():
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set!")
        return

    print("🚀 Starting Guaraná.ch Bot...")
    
    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Kill any existing webhooks/polling sessions
    print("🔄 Clearing old connections...")
    temp_bot = telegram.Bot(token=TOKEN)
    await temp_bot.delete_webhook(drop_pending_updates=True)
    print("✅ Old connections cleared!")
    
    # Initialize the application
    await application.initialize()
    
    # Start polling manually
    print("📡 Starting polling...")
    await application.updater.start_polling()
    print("✅ Bot is running and waiting for users...")
    
    # Keep the bot running forever
    try:
        # This keeps the event loop alive
        while True:
            await asyncio.sleep(3600) # Sleep for 1 hour, repeat
    except KeyboardInterrupt:
        pass
    finally:
        # Clean shutdown
        await application.updater.stop()
        await application.shutdown()

# 4. EXECUTING THE BOT
if __name__ == '__main__':
    # Run using asyncio instead of application.run_polling()
    asyncio.run(main())
