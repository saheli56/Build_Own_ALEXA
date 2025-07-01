import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import re

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Hello, I am Alexa, how can I help you?")
engine.runAndWait()

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
    
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower().strip()
            # Remove filler words and punctuation
            for filler in [',', '.', '?', '!', 'please', 'alexa,', 'alexa']:
                command = command.replace(filler, '')
            print(f"DEBUG: Received command -> {command}")
            if command:
                return command
    except Exception as e:
        print(f"DEBUG: Speech recognition error: {e}")
    return ''

def get_user_command():
    user_input = input('Type your command (or press Enter to use voice): ').strip()
    if user_input:
        command = user_input.lower()
        # Remove filler words and punctuation
        for filler in [',', '.', '?', '!', 'please', 'alexa,', 'alexa']:
            command = command.replace(filler, '')
        print(f"DEBUG: Received typed command -> {command}")
        return command
    return None

def run_alexa():
    command = get_user_command()
    if not command:
        command = take_command()
    if not command:
        talk('Sorry, I did not catch that. Please say the command again.')
        return
    print(f"DEBUG: Processing command -> {command}")
    # Relaxed matching for play
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    # Relaxed matching for open website
    elif 'open' in command and 'website' in command:
        known_sites = {
            'google': 'https://www.google.com',
            'linkedin': 'https://www.linkedin.com',
            'devfolio': 'https://www.devfolio.co',
            'youtube': 'https://www.youtube.com',
            'github': 'https://www.github.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'stackoverflow': 'https://stackoverflow.com',
            'gmail': 'https://mail.google.com',
            'amazon': 'https://www.amazon.com',
            'flipkart': 'https://www.flipkart.com',
            'wikipedia': 'https://www.wikipedia.org',
            'reddit': 'https://www.reddit.com',
            'netflix': 'https://www.netflix.com',
            'whatsapp': 'https://web.whatsapp.com',
            'spotify': 'https://www.spotify.com',
            'zoom': 'https://zoom.us',
            'office': 'https://www.office.com',
            'microsoft': 'https://www.microsoft.com',
            'apple': 'https://www.apple.com',
            'bing': 'https://www.bing.com',
            'yahoo': 'https://www.yahoo.com',
            'quora': 'https://www.quora.com',
            'telegram': 'https://web.telegram.org',
            'discord': 'https://discord.com',
            'drive': 'https://drive.google.com',
            'canva': 'https://www.canva.com',
            'medium': 'https://medium.com',
            'coursera': 'https://www.coursera.org',
            'udemy': 'https://www.udemy.com',
            'kaggle': 'https://www.kaggle.com',
            'leetcode': 'https://leetcode.com',
            'ing': 'https://www.ing.com/Home.htm',
        }
        # Use a more robust extraction for the site name
        # Accepts: "open <site> website" or just "open <site>"
        match = re.search(r'open (.+?)(?: website)?$', command)
        site_name = ''
        url = ''
        if match:
            site_name = match.group(1).strip().lower()
            # Remove any extra words (e.g., 'the', 'app', 'site', 'website')
            for word in ['the', 'app', 'site', 'website']:
                site_name = site_name.replace(word, '').strip()
            # Try to match known sites (by key or by substring)
            for key in sorted(known_sites, key=len, reverse=True):
                if key == site_name or key in site_name or site_name in key:
                    url = known_sites[key]
                    site_name = key
                    break
            if not url:
                # Fallback: construct a .com URL with no spaces or special chars
                safe_site = re.sub(r'[^a-z0-9]', '', site_name)
                url = f'https://www.{safe_site}.com'
            display_name = site_name.capitalize() if site_name else 'website'
            talk(f'Opening {display_name}')
            print(f'Opening URL: {url}')
            webbrowser.open(url)
        else:
            talk('Sorry, I could not understand which website to open.')
        return
    # Relaxed matching for time
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The current time is ' + time)
        print(time)
    # Relaxed matching for who is
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    # Relaxed matching for joke
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'hello' in command:
        talk('Hi!')
    elif 'how are you doing' in command or 'how are you' in command:
        talk('I am doing good! Thanks for asking!')
    elif 'bye' in command:
        quit()
    else:
        talk('Sorry, I did not understand. Please say the command again.')
        

while True:
    run_alexa()