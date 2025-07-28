import pyttsx3
import datetime
import wikipedia
import pyjokes
import speech_recognition as sr

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. How can I help you today?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return ""
    except sr.RequestError:
        speak("Network error. Please try again.")
        return ""

def run_jarvis():
    wish_user()
    while True:
        query = take_command()
        if not query:
            continue  # Retry on empty input

        # Time
        elif "time" in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        # Joke
        elif "joke" in query:
            speak(pyjokes.get_joke())

        # Wikipedia question
        elif "who is" in query or "what is" in query or "tell me about" in query:
            try:
                topic = query.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except:
                speak("Sorry, I couldn't find anything about that.")

        # Exit
        elif "exit" in query or "stop" in query or "bye" in query:
            speak("Goodbye! Have a nice day.")
            break

        # Unknown command
        else:
            speak("Sorry, I don’t know how to do that yet.")

run_jarvis()
