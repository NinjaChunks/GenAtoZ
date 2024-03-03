
def get_message(key: str, lang: str = "en_US"):

    return TELEGRAM_MESSAGES[key]


TELEGRAM_MESSAGES = {
    "start": "Hey! I am GenAtoZ Bot. Send my Text/Photo/File and I will give you a link for it which you can open anywhere easily.",
    
    "sent": "{} sent a Pastebin:\n\n📝 {}",
    "paste_empty": "Error",
    "maintenance": "I'm sorry, but I'm under maintenance right now due to the high demand."
}
