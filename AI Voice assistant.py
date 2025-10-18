import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  # This should be your own file with music links

# Initialize engine globally (don't reinitialize every time)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index if needed
engine.setProperty('rate', 150)  # Optional: adjust speaking speed

# Speak function (stable)
def speak(text):
    print(f"[Speaking]: {text}")
    engine.say(text)
    engine.runAndWait()

# Command processing
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com/")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif "open chatgpt" in c:
        webbrowser.open("https://chatgpt.com")
    elif c.startswith("play"):
        song = " ".join(c.split(" ")[1:])
        print(f"Looking for song: {song}")
        try:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        except KeyError:
            speak("Sorry, I couldn't find that song.")
    else:
        speak("Sorry, I didn't understand the command.")

# Main assistant loop
if __name__ == "__main__":
    speak("Initializing Murtaza Assistant...")
    speak("Microphone is working perfectly, Murtaza!")

    while True:
        try:
            with sr.Microphone(device_index=1) as source:
                print("Listening for wake word...")
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)
            print(f"You said: {word}")

            if "murtaza" in word.lower() or "jarvis" in word.lower():
                print("Wake word detected.")
                speak("Yes")

                print("Listening for your command...")
                with sr.Microphone(device_index=1) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)

                try:
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
                except Exception as e:
                    print(f"Command error: {e}")
                    speak("There was an error processing your command.")
            else:
                print("Wake word not detected.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Error: {e}")


