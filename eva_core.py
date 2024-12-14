import threading
import speech_recognition as sr
import pyttsx3
from queue import Queue, Empty
import json
import os
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def load_commands():
    if os.path.exists("commands.json"):
      with open("commands.json", "r", encoding="utf-8") as f:
        return json.load(f)
    else:
      return {}

def save_commands(commands):
    with open("commands.json", "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=4, ensure_ascii=False)

def listen_and_process(output_queue, commands):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                print("Слушаю...")
                audio = r.listen(source)
                command = r.recognize_google(audio, language='ru-RU')
                print(f"Вы сказали: {command}")

                if "Ева" in command:
                    speak("Привет!")
                    command = command.replace("Ева", "").strip()
                    if command:
                        processed = False
                        for key, action in commands.items():
                            if key in command:
                                output_queue.put((key, command.replace(key,"").strip()))
                                processed = True
                                break
                        if not processed:
                            output_queue.put(("непонятная комманда", command))
                    else:
                        output_queue.put(("нет ввода",))
                else:
                    print("Ожидаю активацию по голосу...")

            except sr.UnknownValueError:
                output_queue.put(("не распознано",))
            except sr.RequestError as e:
                output_queue.put(("ошибка", str(e)))
            except Exception as e:
                print(f"Произошла ошибка: {e}")

def execute_command(command, params, commands, main_window):
    if command == "выключи себя":
        main_window.destroy()
    elif command == "поиск":
        url = f"https://www.google.com/search?q={params}"
        print(f"Выполняю поиск: {params}")
        speak(f"Ищу {params}...")
        webbrowser.open(url)
    elif command == "непонятная комманда":
        print(f"Непонятная команда: {params}")
        speak(f"Непонятная команда: {params}.")
    elif command == "нет ввода":
        print("Нет ввода")
    else:
        if command in commands:
            os.system(commands[command])
            print(f"Выполняю: {command}")