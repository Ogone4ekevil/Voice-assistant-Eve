import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            return r.recognize_google(audio, language='ru-RU')
        except sr.UnknownValueError:
            print("Голос не распознан")
            return None
        except sr.RequestError as e:
            print(f"Ошибка распознания речи: {e}")
            return None