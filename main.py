import pyttsx3
from decouple import config
from datetime import datetime
# import time
import speech_recognition as sr
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from functions.online_ops import play_on_youtube, search_on_google, find_my_ip
import webbrowser
import os
import subprocess
import wikipedia
import pywhatkit as kit
from openai import OpenAI


USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 5.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

contacts = {
    'dad': '#',
    'mom': '#',
    'sis': '#',
    'dada': '#'
    # Add more contacts as needed
}


songss = {
    'siyaram': 'D:\\Manav\\JARVIS\\songs\\siya ram.mp3',
    'shiv tandav': 'D:\\Manav\\JARVIS\\songs\\shivtandav.mp3',
    'tum prem': 'D:\\Manav\\JARVIS\\songs\\tumprem.mp3',
    'instrumental': 'D:\\Manav\\JARVIS\\songs\\Instrumental.mp3'
}

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)


def ai():
    # Initialize OpenAI client
    OPENAI_API_KEY = "#"
    client = OpenAI(api_key=OPENAI_API_KEY)
    speak("what u want to know sir!")

    try:
        user_message = {
            "role": "user",
            "content": take_user_input(),

        }
        print(user_message)
        # Generate a response using chat completion
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[user_message],
        )

        response = chat_completion.choices[0].message.content
        print(response)

    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry Sir, Can't Do It")

def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_user():
    hour = datetime.now().hour

    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USERNAME}!")
    elif 16 <= hour < 19:
        speak(f"Good Evening! {USERNAME}")
    else:
        speak(f"Good Night!{USERNAME}")

    speak(f"I am {BOTNAME}, How can i help you?")


def open_website(url):
    webbrowser.open(url)


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def open_time():
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y-%m-%d")

    speak(f"The current time is {current_time} and the date is {current_date}.")


website = {
    "google": "https://www.google.com",
    "youTube": "https://www.youtube.com",
    "twitter": "https://www.twitter.com",
    "reddit": "https://www.reddit.com",
    "gitHub": "https://www.github.com",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    # Add more websites as needed
}


def take_user_input():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording for 4 seconds...")
            recorded_audio = recognizer.listen(source, timeout=3)
            print("Done recording.")
        try:
            query = recognizer.recognize_google(recorded_audio, language="en-IN").lower()
            print(f"{USERNAME}: Said {query}")
            return query
        except:
            print(speak("You Failed Try Again"))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except Exception as ex:
        print("Error during recognition:", ex)


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input()

        if query is not None:
            if 'open whatsapp' in query:
                open_website("https://web.whatsapp.com/")
                speak("is there anything else i can do for u sir?")

            elif "hello" in query:
                speak(f"Hello {USERNAME} How are you, am i working properly?")

            elif 'time' in query:
                open_time()

            elif "open notepad" in query:
                open_notepad()

            elif 'open command prompt' in query or 'open cmd' in query:
                open_cmd()

            elif 'open camera' in query:
                open_camera()

            elif 'close notepad' in query:
                subprocess.call(["taskkill", "/F", "/IM", "notepad.exe"])

            elif 'open calculator' in query:
                open_calculator()

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "wikipedia" in query:
                speak('What information do you want, sir?')
                search_query = take_user_input()
                if search_query is not None:
                    results = search_on_wikipedia(search_query)
                    speak(f"According to Wikipedia, {results}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(results)

            elif "youtube" in query:
                speak('What do you want to play on Youtube, sir?')
                video = take_user_input()
                if video is not None:
                    play_on_youtube(video)

            elif "google" in query:
                speak('What do you want to search on Google, sir?')
                search_query = take_user_input()
                if search_query is not None:
                    search_on_google(search_query)

            elif "website" in query:
                command = take_user_input()
                if command in website:
                    url = website[command]
                    webbrowser.open_new_tab(url)
                    speak(f"Opening {command}")


            elif "send whatsapp message" in query:
                speak('whom do you want to send message sir? ')
                name = take_user_input()
                if name in contacts:
                    number = contacts.get(name)
                    speak("What is the message sir?")
                    message = take_user_input()
                    if message is not None:
                        send_whatsapp_message(number, message)
                        speak("I've sent the message sir.")

            elif "play song" in query:
                speak("Which Song Do You Want To Play")
                songg = take_user_input()
                if songg in songss:
                    son = songss.get(songg)
                    os.startfile(son)


            elif "ai" in query:
                ai()

            elif "remember that" in query:
                rememberMsg = query.replace("jarvis", "")
                rememberMsg = rememberMsg.replace("remember that", "")
                speak("You told me to remember:" + rememberMsg)
                remeber = open("D:\\Manav\\JARVIS\\remeber.txt", 'w')
                remeber.write(rememberMsg)
                remeber.close()

            elif "do you remember something" in query:
                remeber = open("D:\\Manav\\JARVIS\\remeber.txt", 'r')
                speak("Yes sir you told me to remember that:" + remeber.read())

            elif "exit" or "wait" or "good night" in query:
                speak("Okay Good Bye Sir Meet You Soon")
                exit()
