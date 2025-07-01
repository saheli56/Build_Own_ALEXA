import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import os
import subprocess
import wikipedia
import pyjokes
import webbrowser
import re
import shutil

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
    # Relaxed matching for play
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    # Handle application launches
    elif 'open' in command or 'launch' in command:
        app_mapping = {
            'spotify': r'C:\Users\sahel\AppData\Roaming\Spotify\Spotify.exe',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'vscode': r'C:\Users\sahel\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'paint': 'mspaint.exe',
            'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
            'pycharm': r'C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.1\bin\pycharm64.exe',
            'control panel': 'control',
            # Add aliases for common mispronunciations
            'crome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'visual studio code': r'C:\Users\sahel\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'brav': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
        }
        app_name = re.search(r'(?:open|launch)\s+(.+?)(?:\s+app)?$', command)
        if app_name:
            target_app = app_name.group(1).strip().lower()
            print(f"DEBUG: Attempting to launch {target_app}")
            # Try all possible relaxed matches
            possible_matches = [name for name in app_mapping if name in target_app or target_app in name or name.replace(' ', '') in target_app.replace(' ', '')]
            tried = set()
            for name in possible_matches:
                app_to_try = app_mapping[name]
                if app_to_try in tried:
                    continue
                tried.add(app_to_try)
                try:
                    if os.path.isfile(app_to_try):
                        os.startfile(app_to_try)
                        talk(f'Opening {name}')
                        return
                    else:
                        # Quote path if it contains spaces
                        cmd = f'"{app_to_try}"' if ' ' in app_to_try and not app_to_try.startswith('"') else app_to_try
                        subprocess.Popen(cmd, shell=True)
                        talk(f'Opening {name}')
                        return
                except Exception as e:
                    print(f"DEBUG: Launch failed for {name} ({app_to_try}): {e}")
            # Try direct command as last resort
            try:
                if shutil.which(target_app):
                    cmd = f'"{target_app}"' if ' ' in target_app and not target_app.startswith('"') else target_app
                    subprocess.Popen(cmd, shell=True)
                    talk(f'Opening {target_app}')
                    return
            except Exception as e:
                print(f"DEBUG: Direct launch failed for {target_app}: {e}")
            talk(f"Could not find {target_app} application")
            print(f"DEBUG: No application found matching '{target_app}'. Tried: {possible_matches if possible_matches else '[no matches]'}")

    # Handle website opening
    elif 'open' in command and ('website' in command or 'dot' in command or any(tld in command for tld in ['.com', '.in', '.ai', '.org', '.net', '.co', '.us', '.gov', '.edu'])):
        known_sites = {
            'google.com': 'https://www.google.com',
            'linkedin.com': 'https://www.linkedin.com',
            'devfolio.co': 'https://www.devfolio.co',
            'onlinesbi.sbi': 'https://www.onlinesbi.sbi',
            'youtube.com': 'https://www.youtube.com',
            'github.com': 'https://www.github.com',
            'facebook.com': 'https://www.facebook.com',
            'twitter.com': 'https://www.twitter.com',
            'instagram.com': 'https://www.instagram.com',
            'stackoverflow.com': 'https://stackoverflow.com',
            'gmail.com': 'https://mail.google.com',
            'amazon.com': 'https://www.amazon.com',
            'amazon.in': 'https://www.amazon.in',
            'flipkart.com': 'https://www.flipkart.com',
            'wikipedia.org': 'https://www.wikipedia.org',
            'reddit.com': 'https://www.reddit.com',
            'netflix.com': 'https://www.netflix.com',
            'whatsapp.com': 'https://web.whatsapp.com',
            'spotify.com': 'https://www.spotify.com',
            'zoom.us': 'https://zoom.us',
            'office.com': 'https://www.office.com',
            'microsoft.com': 'https://www.microsoft.com',
            'apple.com': 'https://www.apple.com',
            'bing.com': 'https://www.bing.com',
            'yahoo.com': 'https://www.yahoo.com',
            'quora.com': 'https://www.quora.com',
            'telegram.org': 'https://web.telegram.org',
            'discord.com': 'https://discord.com',
            'drive.google.com': 'https://drive.google.com',
            'canva.com': 'https://www.canva.com',
            'medium.com': 'https://medium.com',
            'coursera.org': 'https://www.coursera.org',
            'udemy.com': 'https://www.udemy.com',
            'kaggle.com': 'https://www.kaggle.com',
            'leetcode.com': 'https://leetcode.com',
            'ing.com': 'https://www.ing.com/Home.htm',
        }
        known_sites = {
            'google.com': 'https://www.google.com',
            'linkedin.com': 'https://www.linkedin.com',
            'devfolio.co': 'https://www.devfolio.co',
            'onlinesbi.sbi': 'https://www.onlinesbi.sbi',
            'youtube.com': 'https://www.youtube.com',
            'github.com': 'https://www.github.com',
            'facebook.com': 'https://www.facebook.com',
            'twitter.com': 'https://www.twitter.com',
            'instagram.com': 'https://www.instagram.com',
            'stackoverflow.com': 'https://stackoverflow.com',
            'gmail.com': 'https://mail.google.com',
            'amazon.com': 'https://www.amazon.com',
            'amazon.in': 'https://www.amazon.in',
            'flipkart.com': 'https://www.flipkart.com',
            'wikipedia.org': 'https://www.wikipedia.org',
            'reddit.com': 'https://www.reddit.com',
            'netflix.com': 'https://www.netflix.com',
            'whatsapp.com': 'https://web.whatsapp.com',
            'spotify.com': 'https://www.spotify.com',
            'zoom.us': 'https://zoom.us',
            'office.com': 'https://www.office.com',
            'microsoft.com': 'https://www.microsoft.com',
            'apple.com': 'https://www.apple.com',
            'bing.com': 'https://www.bing.com',
            'yahoo.com': 'https://www.yahoo.com',
            'quora.com': 'https://www.quora.com',
            'telegram.org': 'https://web.telegram.org',
            'discord.com': 'https://discord.com',
            'drive.google.com': 'https://drive.google.com',
            'canva.com': 'https://www.canva.com',
            'medium.com': 'https://medium.com',
            'coursera.org': 'https://www.coursera.org',
            'udemy.com': 'https://www.udemy.com',
            'kaggle.com': 'https://www.kaggle.com',
            'leetcode.com': 'https://leetcode.com',
            'ing.com': 'https://www.ing.com/Home.htm',
        }
        # Supported TLDs
        tlds = ['.com', '.in', '.ai', '.org', '.net', '.co', '.us', '.gov', '.edu', '.io', '.me', '.info', '.xyz', '.sbi']

        # Extract the site name from the command
        match = re.search(r'open (.+?)(?: website)?$', command)
        site_name = ''
        url = ''
        if match:
            site_name = match.group(1).strip().lower()
            
            # Clean unwanted words
            for word in ['app', 'site', 'website', 'please']:
                site_name = site_name.replace(word, '').strip()
            
            # Replace spoken domain suffixes
            for tld in tlds:
                spoken = ' dot ' + tld[1:]
                site_name = site_name.replace(spoken, tld)
            
            # Check for TLDs as separate words
            parts = site_name.split()
            if len(parts) > 1:
                last_part = parts[-1]
                if f".{last_part}" in tlds:
                    site_name = ".".join(parts)
            
            # Final clean of spaces
            site_name = site_name.replace(' ', '')
            
            # Find matching known site
            url = ''
            for key in sorted(known_sites, key=len, reverse=True):
                if key == site_name or key in site_name or site_name in key:
                    url = known_sites[key]
                    site_name = key
                    break
            
            if not url:
                has_tld = any(site_name.endswith(tld) for tld in tlds)
                if has_tld:
                    url = f'https://www.{site_name}'
                else:
                    url = f'https://www.{site_name}.com'
            
            if url:
                display_name = site_name.split('.')[0].capitalize()
                talk(f'Opening {display_name}')
                webbrowser.open(url)
            else:
                talk('Sorry, I could not understand which website to open.')
            site_name = match.group(1).strip().lower()

            # Replace spoken domain suffixes like 'dot ai' with '.ai'
            # Clean unwanted words first
            for word in ['app', 'site', 'website', 'please']:  # Removed 'the' from removal list
                site_name = site_name.replace(word, '').strip()
            
            for tld in tlds:
                spoken = ' dot ' + tld[1:]
                site_name = site_name.replace(spoken, tld)
            
            # Check for TLDs as separate words without "dot"
            parts = site_name.split()
            if len(parts) > 1:
                last_part = parts[-1]
                if f".{last_part}" in tlds:
                    site_name = ".".join(parts)
            
            # Final clean of any remaining spaces not part of domain structure
            site_name = site_name.replace(' ', '')

            # Check if the site matches a known site
            for key in sorted(known_sites, key=len, reverse=True):
                if key == site_name or key in site_name or site_name in key:
                    url = known_sites[key]
                    site_name = key
                    break

            if not url:
                # Check if the site name ends with a valid TLD
                has_tld = any(site_name.endswith(tld) for tld in tlds)
                if has_tld:
                    url = f'https://www.{site_name}'
                else:
                    # Default to '.com' if no TLD is found
                    url = f'https://www.{site_name}.com'

            if url:
                display_name = site_name.split('.')[0].capitalize() if site_name else 'website'
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
    print("\nType your command (or 'exit', 'quit', or 'stop' to quit): ")
    command = get_user_command()
    if command and command.strip().lower() in ['exit', 'quit', 'stop']:
        talk('Goodbye!')
        print('Exiting Alexa. Have a great day!')
        break
    if not command:
        command = take_command()
    if command and command.strip().lower() in ['exit', 'quit', 'stop']:
        talk('Goodbye!')
        print('Exiting Alexa. Have a great day!')
        break
    if command:
        print(f"DEBUG: Processing command -> {command}")
        run_alexa()
    else:
        talk('Sorry, I did not catch that. Please say the command again.')