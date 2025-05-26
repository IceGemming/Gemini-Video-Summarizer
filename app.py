from google import genai
from dotenv import load_dotenv

import moviepy.editor as mp
import speech_recognition as sr

import os

import tkinter as tk
from tkinter import filedialog

load_dotenv()

def video_extract(vid):

    video = mp.VideoFileClip(vid)
    wav_name = vid[0:vid.index('.')]+".wav"

    audio_file = video.audio
    audio_file.write_audiofile(wav_name)

    r = sr.Recognizer()

    with sr.AudioFile(wav_name) as source:
        data = r.record(source)

    text = r.recognize_google(data)

    os.remove(wav_name)

    return text


def summarize(transcript):
    API_KEY = os.getenv('API_KEY')
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[transcript, "\n\n", "Summarize the given transcript"]
    )

    return response.text


def run(vid):
    transcript = video_extract(vid)
    summary = summarize(transcript)
    T.insert(tk.END, summary)


def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    run(filename)

root = tk.Tk()
root.title('Video Summarizer')
button = tk.Button(root, text='Upload Video', command=UploadAction)
button.pack(pady=10)
root.geometry("700x580")
T = tk.Text(root, height = 40, width = 90, wrap='word')
T.pack(padx=20, pady=20)

root.mainloop()

