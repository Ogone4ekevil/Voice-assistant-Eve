def process_command(text):
    text = text.lower()
    if "поиск" in text:
        query = text.split("поиск", 1)[1].strip()
        return "поиск", query
    elif "музыка" in text:
        artist_song = text.split("музыка", 1)[1].strip()
        return "музыка", artist_song
    elif "выключи себя" in text:
        return "выключи себя", None
    else:
        return None, None