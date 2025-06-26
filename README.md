# Alexa Voice Assistant (Python)

A simple voice-controlled virtual assistant built with Python. This project allows you to interact with your computer using voice commands, similar to Amazon Alexa. It can play YouTube songs, tell the current time, fetch Wikipedia summaries, tell jokes, and more.

## Features
- **Voice Recognition:** Listens for your commands using your microphone.
- **Text-to-Speech:** Responds with spoken feedback.
- **Play Songs:** Plays requested songs on YouTube.
- **Time Query:** Tells the current time.
- **Wikipedia Search:** Answers "Who is ..." questions with a summary from Wikipedia.
- **Jokes:** Tells random jokes.
- **Greetings:** Responds to greetings and simple conversational phrases.

## Requirements
- Python 3.7+
- Microphone (for voice input)

## Dependencies
Install the following Python packages:

- `speechrecognition`
- `pyttsx3`
- `pywhatkit`
- `datetime` (standard library)
- `wikipedia`
- `pyjokes`

You can install the required packages using pip:

```bash
pip install SpeechRecognition pyttsx3 pywhatkit wikipedia pyjokes
```

## Usage
1. Clone this repository or download the source code.
2. Ensure your microphone is connected and working.
3. Run the main script:

```bash
python main.py
```

4. Say "Alexa" followed by your command. Example commands:
   - "Alexa play Shape of You"
   - "Alexa what is the time"
   - "Alexa who is Albert Einstein"
   - "Alexa tell me a joke"
   - "Alexa hello"

## Example Commands
- **Play a song:**
  - "Alexa play [song name]"
- **Get the time:**
  - "Alexa what is the time"
- **Wikipedia summary:**
  - "Alexa who is [person]"
- **Tell a joke:**
  - "Alexa tell me a joke"
- **Greetings:**
  - "Alexa hello"

## Notes
- The assistant listens for the keyword "Alexa" before processing commands.
- Make sure your microphone is not muted and has the necessary permissions.
- For best results, speak clearly and wait for the "listening..." prompt.

## License
This project is for educational purposes and is not affiliated with Amazon or the Alexa product line.
