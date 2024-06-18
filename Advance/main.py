import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import smtplib
import requests
import json

# Configure speech engine
engine = pyttsx3.init()


# Speech recognition setup
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
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


def send_email(to, subject, body):
    # Configure your email SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'your_email@gmail.com'  # Replace with your email address
    sender_password = 'your_password'  # Replace with your email password

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(sender_email, to, message)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Sorry, I am unable to send the email. Error: {str(e)}")

def get_weather(city):
    # Replace with your API key and API endpoint
    api_key = "0f2da766b4d61c386ec2f19799de2975"  # Replace with your OpenWeatherMap API key
    endpoint = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(endpoint)
        weather_data = json.loads(response.text)

        if weather_data['cod'] == 200:
            weather_desc = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            speak(f"The current weather in {city} is {weather_desc}. The temperature is {temp} degrees Celsius.")
        else:
            speak("Sorry, I couldn't fetch the weather information.")
    except Exception as e:
        speak(f"Sorry, I encountered an error while fetching the weather. Error: {str(e)}")

def process_command(query):
    if 'send email' in query:
        speak("To whom do you want to send the email?")
        to = listen_command()
        speak("What is the subject of the email?")
        subject = listen_command()
        speak("What should I write in the email?")
        body = listen_command()
        send_email(to, subject, body)

    elif 'weather' in query:
        speak("Sure, which city's weather do you want to know?")
        city = listen_command()
        get_weather(city)

    elif 'open website' in query:
        speak("Which website do you want me to open?")
        website = listen_command()
        url = f"https://www.{website}.com"
        webbrowser.open(url)
        speak(f"Opening {website}")

    elif 'terminate' in query:
        program_name = query.replace("terminate", "").strip()
        terminate_program(program_name)

    elif 'lock the computer' in query:
        lock_computer()

    elif 'shutdown' in query:
        shutdown_computer()

    # Add more commands for controlling smart home devices, setting reminders, etc.

def terminate_program(program_name):
    try:
        subprocess.run(["pkill", program_name], check=True)  # Linux command to terminate process by name
        speak(f"Successfully terminated {program_name}.")
    except subprocess.CalledProcessError:
        speak(f"Failed to terminate {program_name}.")

def lock_computer():
    try:
        subprocess.run(["gnome-screensaver-command", "-l"])  # Linux command to lock screen
        speak("The computer is locked.")
    except Exception as e:
        speak(f"Sorry, I encountered an error while locking the computer. Error: {str(e)}")

def shutdown_computer():
    try:
        speak("Hold on a sec! Your system is on its way to shut down.")
        subprocess.call(['shutdown', 'now'])  # Linux shutdown command
    except Exception as e:
        speak(f"Sorry, I encountered an error while shutting down the computer. Error: {str(e)}")

if __name__ == "__main__":
    speak("Welcome! How can I assist you today?")

    while True:
        query = listen_command()

        if 'exit' in query:
            speak("Goodbye!")
            break

        process_command(query)
