import os
import torch
import tkinter as tk
import torch.nn.functional as F
from tkinter import messagebox
from pydub import AudioSegment
from speechbrain.inference import EncoderClassifier
import yt_dlp
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Load the SpeechBrain model
model = EncoderClassifier.from_hparams("Jzuluaga/accent-id-commonaccent_ecapa")

# Download and convert YouTube audio to WAV
def download_and_convert_to_wav(youtube_url):
    output_filename = "audio_file"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_filename}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    mp3_file = f"{output_filename}.mp3"
    wav_file = f"{output_filename}.wav"

    if not os.path.exists(mp3_file):
        raise FileNotFoundError("MP3 file was not created.")

    audio = AudioSegment.from_file(mp3_file)
    audio.export(wav_file, format="wav")
    os.remove(mp3_file)
    return wav_file

# Classify the accent in the given WAV file
def classify_accent(wav_path):
    logits, score, index, label = model.classify_file(wav_path)
    probs = F.softmax(logits, dim=1)
    class_labels = model.hparams.label_encoder.decode_ndim(torch.arange(probs.shape[1]))

    result = "Accent probabilities:\n\n"
    for i, lbl in enumerate(class_labels):
        result += f"{lbl:15s}: {probs[0, i].item()*100:.2f}%\n"

    # Find the most probable accent
    best_index = torch.argmax(probs, dim=1).item()
    best_label = class_labels[best_index]

    return result, best_label

# GUI application
def run_app():
    def process_video():
        url = url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        try:
            status_label.config(text="Downloading and processing audio...")
            root.update()

            wav_path = download_and_convert_to_wav(url)
            result, most_probable_accent = classify_accent(wav_path)
            os.remove(wav_path)

            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, result)
            status_label.config(text=f"The most probable accent is: {most_probable_accent}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Failed.")

    # Build GUI
    root = tk.Tk()
    root.title("YouTube Accent Identifier")

    tk.Label(root, text="Enter YouTube Video URL:").pack(pady=5)
    url_entry = tk.Entry(root, width=60)
    url_entry.pack(pady=5)

    process_button = tk.Button(root, text="Analyze Accent", command=process_video)
    process_button.pack(pady=10)

    status_label = tk.Label(root, text="")
    status_label.pack()

    result_text = tk.Text(root, height=15, width=70)
    result_text.pack(pady=10)

    root.mainloop()

# Run the app
if __name__ == "__main__":
    run_app()
