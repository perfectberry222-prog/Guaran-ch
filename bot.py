import os
import asyncio
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

# 3. START THE BOT (Fixed for Railway)
if __name__ == '__main__':
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    PORT = int(os.environ.get('PORT', 8080)) # Railway requires a PORT variable
    
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set!")
        exit(1)
        
    print("Building application...")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # --- IMPORTANT RAILWAY FIX ---
    # Start the bot using Webhooks instead of Polling (Stops the Conflict error)
    print(f"Starting webhook on port {PORT}...")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RAILWAY_STATIC_URL')}/{TOKEN}"
    )
