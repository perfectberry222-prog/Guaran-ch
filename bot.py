import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. START COMMAND (French first)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Language selection buttons
    language_keyboard = [
        [InlineKeyboardButton("Français", callback_data='FR'), 
         InlineKeyboardButton("English", callback_data='EN'), 
         InlineKeyboardButton("Deutsch", callback_data='DE')]
    ]
    reply_markup = InlineKeyboardMarkup(language_keyboard)
    
    # Send the Guaraná.ch logo image first
    try:
        await update.message.reply_photo(photo=open('logo.png', 'rb'))
    except Exception as e:
        print(f"Image error: {e}")

    # Send the French text with the language buttons
    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

# 2. HANDLE BUTTON CLICKS
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # --- THE 2 BUTTON MENU FOR EVERY LANGUAGE ---
    main_menu_keyboard = [
        [InlineKeyboardButton("🛍️ Open shop", url="PUT_YOUR_SHOP_LINK_HERE")], 
        [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    
    # If user selects ENGLISH
    if query.data == 'EN':
        # Send a NEW message with the English text + 2 buttons
        await query.message.reply_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )
        
    # If user selects FRENCH
    elif query.data == 'FR':
        # Send a NEW message with the French text + 2 buttons
        await query.message.reply_text(
            text="🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇",
            reply_markup=reply_markup
        )

    # If user selects GERMAN
    elif query.data == 'DE':
        # Send a NEW message with the German text + 2 buttons
        await query.message.reply_text(
            text="🤗 Willkommen bei Guaraná.ch!\nDanke für dein Vertrauen – bestelle schnell über den Shop 👇",
            reply_markup=reply_markup
        )

# 3. START THE BOT
if __name__ == '__main__':
    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set!")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running and waiting for users...")
    application.run_polling()
