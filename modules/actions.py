import webbrowser
import time

def search_web(query):
    webbrowser.open('https://www.google.com/search?q={query}')

def play_music(query):
    print(f'Воспроизведение музыки: {query}')
    time.sleep(2)