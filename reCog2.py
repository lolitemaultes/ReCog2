import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import soundfile as sf
import whisper
import numpy as np
import os
import re
from ttkthemes import ThemedTk
from tkinter.scrolledtext import ScrolledText
import sys
import io

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("reCog2")
        self.root.geometry("800x500")
        
        # Define variables
        self.audio_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        
        # Apply theme
        self.style = ttk.Style()
        self.style.configure('TButton', background='lightblue', font=('Helvetica', 12))
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TProgressbar', thickness=25)
        
        # Create and place widgets
        self.create_widgets()
        
        # Redirect stdout and stderr to debug panel
        self.redirect_output()

    def create_widgets(self):
        # Audio file selection
        tk.Label(self.root, text="Audio File:", anchor="e").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.root, textvariable=self.audio_path, width=50, font=('Helvetica', 12)).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Browse", command=self.browse_audio).grid(row=0, column=2, padx=10, pady=10)
        
        # Output folder selection
        tk.Label(self.root, text="Output Folder:", anchor="e").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(self.root, textvariable=self.output_folder, width=50, font=('Helvetica', 12)).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, padx=10, pady=10)
        
        # Transcription button
        ttk.Button(self.root, text="Start Transcription", command=self.start_transcription).grid(row=2, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="indeterminate")
        self.progress.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        # Status area
        self.status_label = tk.Label(self.root, text="", wraplength=700, font=('Helvetica', 12))
        self.status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        
        # Debug panel
        self.debug_panel = ScrolledText(self.root, wrap=tk.WORD, width=80, height=10, font=('Courier', 10))
        self.debug_panel.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        
    def browse_audio(self):
        self.audio_path.set(filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")]))
    
    def browse_output_folder(self):
        self.output_folder.set(filedialog.askdirectory())
    
    def start_transcription(self):
        audio_path = self.audio_path.get()
        output_folder = self.output_folder.get()
        
        if not audio_path or not output_folder:
            messagebox.showerror("Input Error", "Please select both an audio file and an output folder.")
            return
        
        self.progress.start()
        self.root.update_idletasks()
        
        try:
            self.transcribe_audio(audio_path, output_folder)
            messagebox.showinfo("Success", "Transcription completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.progress.stop()
    
    def transcribe_audio(self, path, output_folder):
        self.debug("Loading Whisper model...")
        # Load the Whisper model
        model = whisper.load_model("base")
        
        self.debug("Transcribing audio...")
        # Transcribe the entire audio file
        result = model.transcribe(path, verbose=True, word_timestamps=True)
        
        # Create output folder if it doesn't exist
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        
        # Read the audio file
        data, sample_rate = sf.read(path)
        
        # Process each sentence
        for segment in result['segments']:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text'].strip()
            
            if text:
                buffer_duration = 0.2  # 200 milliseconds buffer
                start_index = int(start_time * sample_rate)
                end_index = min(int((end_time + buffer_duration) * sample_rate), len(data))
                
                # Extract chunk data
                chunk_data = data[start_index:end_index]

                # Sanitize text to use as filenames
                sanitized_text = self.sanitize_text(text)
                
                # Save the chunk as WAV file and transcription text
                chunk_file = os.path.join(output_folder, f"{sanitized_text}_chunk.wav")
                text_file = os.path.join(output_folder, f"{sanitized_text}_transcription.txt")

                # Save the chunk audio file
                sf.write(chunk_file, chunk_data, sample_rate)
                
                # Save the transcription text
                with open(text_file, "w") as f:
                    f.write(text)
        
        self.debug("Transcription complete.")

    def sanitize_text(self, text):
        """Sanitize the transcription text to be used in filenames and folder names."""
        return re.sub(r'[\/:*?"<>|]', '', text).replace(" ", "_").replace("\\", "_")

    def redirect_output(self):
        """Redirect stdout and stderr to the debug panel."""
        class StdoutRedirector(io.StringIO):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def write(self, s):
                if s.strip():  # Avoid writing empty lines
                    self.text_widget.insert(tk.END, s)
                    self.text_widget.yview(tk.END)

        # Redirect stdout and stderr
        sys.stdout = StdoutRedirector(self.debug_panel)
        sys.stderr = StdoutRedirector(self.debug_panel)
    
    def debug(self, message):
        """Custom debug method for logging messages to the debug panel."""
        print(message)

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Use a themed window for a modern look
    app = TranscriptionApp(root)
    root.mainloop()