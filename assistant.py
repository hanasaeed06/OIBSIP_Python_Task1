import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys

# Initialize speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_day():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_index = datetime.datetime.today().weekday()
    return days[day_index]

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_text("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language='en-in')
        update_text(f"You said: {query}")
        return query.lower()
    except Exception:
        update_text("Sorry, I didn't get that. Please say it again.")
        return ""

def update_text(message):
    text_output.config(state='normal')
    text_output.insert(tk.END, message + "\n\n")
    text_output.see(tk.END)
    text_output.config(state='disabled')

def run_assistant():
    query = listen()
    if query == "":
        return

    response = ""

    if "hello" in query or "hi" in query:
        response = "Hello! How can I assist you today?"

    elif "time" in query:
        response = f"The time is {get_time()}."

    elif "date" in query:
        response = f"Today's date is {get_date()}."

    elif "day" in query:
        response = f"Today is {get_day()}."

    elif "who is" in query or "what is" in query:
        try:
            topic = query.replace("who is", "").replace("what is", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            response = summary
        except Exception:
            response = "Sorry, I couldn't find information on that topic."

    elif "joke" in query:
        response = pyjokes.get_joke()

    elif "play" in query:
        song = query.replace("play", "").strip()
        response = f"Playing {song} on YouTube."
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    elif "bye" in query or "stop" in query or "exit" in query:
        response = "Goodbye! Have a great day."
        update_text("Assistant: " + response)
        speak(response)
        root.destroy()
        sys.exit()

    else:
        response = "Sorry, I can't perform that task yet."

    update_text("Assistant: " + response)
    speak(response)

# Set up GUI
root = tk.Tk()
root.title("Simple Voice Assistant")
root.geometry("550x500")
root.configure(bg="#f0f0f0")

label_title = tk.Label(root, text="Voice Assistant", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
label_title.pack(pady=10)

text_output = scrolledtext.ScrolledText(root, height=14, width=60, wrap="word", font=("Helvetica", 12))
text_output.pack(padx=10, pady=10)
text_output.config(state='disabled')

btn_speak = tk.Button(
    root,
    text="Speak",
    font=("Helvetica", 16, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    width=12,
    command=run_assistant
)
btn_speak.pack(pady=10)

root.mainloop()
