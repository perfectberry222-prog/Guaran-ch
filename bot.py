import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. START COMMAND (French first)
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
    except Exception as e:
        print(f"Image error: {e}")

    # Send French text
    await update.message.reply_text(
        "👋 Bienvenue sur Guaraná.ch\nChoisis ta langue pour accéder au catalogue :",
        reply_markup=reply_markup
    )

# 2. HANDLE LANGUAGE BUTTON CLICKS
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Important: This clears the "loading" state on the button

    # The 2 buttons we want to show after picking a language
    main_menu_keyboard = [
        [InlineKeyboardButton("🛍️ Open shop", url="PUT_YOUR_SHOP_LINK_HERE")], 
        [InlineKeyboardButton("📞 Contact us", url="https://t.me/FavelaTerpsPackz")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    # --- ENGLISH ---
    if query.data == 'EN':
        # Send the LOGO again (to match your screenshot exactly)
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception as e:
            print(f"Image error: {e}")

        # Send the ENGLISH MENU as a NEW message
        await query.message.reply_text(
            text="🤗 Welcome to Guaraná.ch!\nThanks for your trust – order quickly via the shop 👇",
            reply_markup=reply_markup
        )

    # --- FRENCH ---
    elif query.data == 'FR':
        # Send the LOGO again
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception as e:
            print(f"Image error: {e}")

        # Send the FRENCH MENU as a NEW message
        await query.message.reply_text(
            text="🤗 Bienvenue sur Guaraná.ch!\nMerci de votre confiance – commandez rapidement via la boutique 👇",
            reply_markup=reply_markup
        )

    # --- GERMAN ---
    elif query.data == 'DE':
        # Send the LOGO again
        try:
            await query.message.reply_photo(photo=open('logo.png', 'rb'))
        except Exception as e:
            print(f"Image error: {e}")

        # Send the GERMAN MENU as a NEW message
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
