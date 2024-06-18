import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize speech recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak out the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech from microphone
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""


def handle_query(query):
    if "hello" in query:
        speak("Hello! How can I help you?")
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        current_date = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "search" in query:
        query = query.replace("search", "").strip()
        if query:
            search_url = f"https://www.google.com/search?q={query}"
            speak(f"Searching the web for {query}")
            webbrowser.open(search_url)
        else:
            speak("What would you like me to search for?")
    elif "exit" in query or "quit" in query:
        speak("Goodbye!")
        return False
    else:
        speak("I'm sorry, I didn't quite catch that. Can you repeat?")

    return True


speak("Hello! How can I assist you today?")
while True:
    query = recognize_speech()
    if query:
        if not handle_query(query):
            break
