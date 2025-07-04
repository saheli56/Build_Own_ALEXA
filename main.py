import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import re
import subprocess

listener = sr.Recognizer()
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Hello, I am Alexa, how can I help you?")
    engine.runAndWait()
except Exception as e:
    print(f"Warning: Text-to-speech initialization failed: {e}")
    engine = None

def talk(text):
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            print(f"Alexa: {text}")
    else:
        print(f"Alexa: {text}")


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
        # Remove filler words and punctuation (keep dots for domains)
        for filler in [',', '?', '!', 'please', 'alexa,', 'alexa']:
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

    app_map = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
        'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
        'paint': 'mspaint.exe',
        'cmd': 'cmd.exe',
        'powershell': 'powershell.exe',
        'explorer': 'explorer.exe',
        'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        'control panel': 'control.exe',
        'cursor': r'C:\Users\sahel\AppData\Local\Programs\Cursor\Cursor.exe',
    }
    known_sites = {
        'facebook': 'https://www.facebook.com',
        'google': 'https://www.google.com',
        'linkedin': 'https://www.linkedin.com',
        'youtube': 'https://www.youtube.com',
        'github': 'https://www.github.com',
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
    tlds = ['.com', '.in', '.ai', '.org', '.net', '.co', '.us', '.gov', '.edu', '.io', '.me', '.info', '.xyz', '.sbi', '.dev', '.app']

    # NLP: Extract target after 'open'
    target = ''
    if 'open' in command:
        match = re.search(r'open\s+([\w\s\.\-]+)', command)
        if match:
            target = match.group(1).strip().lower()
            # Remove common filler words
            target = re.sub(r'\b(app|application|desktop|please|the|website|site)\b', '', target).strip()

    # Prefer app if both app and website exist
    if target:
        # Check for app match (exact or partial)
        for app in app_map:
            if app == target or app in target:
                talk(f'Opening {app}')
                try:
                    subprocess.Popen(app_map[app])
                except Exception as e:
                    talk(f'Sorry, I could not open {app}.')
                    print(f'Error opening {app}:', e)
                return
        # Check for website match (by name or TLD)
        for site in known_sites:
            if site == target or site in target:
                url = known_sites[site]
                talk(f'Opening {site}')
                print(f'Opening URL: {url}')
                webbrowser.open(url)
                return
        # Check for TLD in target (e.g., google.com)
        if any(tld in target for tld in tlds):
            url = target if target.startswith('http') else f'https://{target}'
            talk(f'Opening {target.split(".")[0].capitalize()}')
            print(f'Opening URL: {url}')
            webbrowser.open(url)
            return
        # Fallback: try as .com website
        if target:
            url = f'https://www.{target}.com'
            talk(f'Opening {target.capitalize()}')
            print(f'Opening URL: {url}')
            webbrowser.open(url)
            return
        talk('Sorry, I could not understand which app or website to open.')
        return

    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The current time is ' + time)
        print(time)
        return
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
        return
    elif 'joke' in command:
        talk(pyjokes.get_joke())
        return
    elif 'hello' in command:
        talk('Hi!')
        return
    elif 'how are you doing' in command or 'how are you' in command:
        talk('I am doing good! Thanks for asking!')
        return
    elif 'bye' in command:
        quit()
    else:
        talk('Sorry, I did not understand. Please say the command again.')
        return


if __name__ == "__main__":
    while True:
        run_alexa()
        user_choice = input("Press Enter to continue or type 'exit' to quit: ").strip().lower()
        if user_choice == 'exit':
            print("Exiting Alexa. Goodbye!")
            break