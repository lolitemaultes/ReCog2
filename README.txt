# reCog2 - Powerful Audio Transcription & Segmentation Tool

**reCog2** is an intuitive and efficient desktop application designed for audio transcription and segmentation. Built with Python and leveraging OpenAI's Whisper AI model, reCog2 enables users to transcribe audio files and automatically extract specific audio clips based on transcribed text. Whether you're a music producer, video editor, podcaster, or content creator, this tool can save you hours of manual editing by breaking down long speeches, dialogues, or audio recordings into manageable, meaningful segments.

## 🚀 Key Features

- **Precise Transcription**: Automatically transcribe your audio files into text using Whisper AI, which delivers highly accurate transcriptions, even for noisy or complex recordings.
- **Segmented Audio Clips**: Extract specific audio clips based on transcribed text, ideal for isolating quotes, soundbites, or key moments from a longer recording.
- **Custom File Naming**: Automatically generate filenames based on the transcription text, ensuring that your audio clips and transcriptions are neatly organized.
- **Progress Tracking**: Real-time feedback with a progress bar to monitor transcription status.
- **Debug Panel**: Easily troubleshoot and monitor the transcription process with a dedicated debug panel for detailed logging.
- **Multi-Purpose Use**: Perfect for **music producers** isolating specific samples, **video editors** cutting dialogue or soundbites, **podcasters** transcribing interviews, and **all-around creatives** working with audio.

## 🎯 Who Can Use reCog2?

- **Music Producers**: Effortlessly grab specific clips or samples from longer audio tracks for remixing, sound design, or sampling.
- **Video Editors**: Extract dialogue, soundbites, or key audio moments to sync with visuals.
- **Podcasters**: Quickly transcribe long podcasts or interviews and extract specific segments for highlights, social media clips, or show notes.
- **Content Creators**: Split large audio recordings into useful, shareable clips, whether for YouTube, TikTok, or other platforms.

## 🛠️ Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `tkinter` (GUI framework)
  - `soundfile` (audio file handling)
  - `whisper` (AI transcription)
  - `numpy` (for audio processing)
  - `ttkthemes` (for modern-themed UI)
  - `re`, `os`, `sys`, `io` (for text processing and file handling)

To install the necessary dependencies, run:

```bash
pip install soundfile whisper numpy ttkthemes
