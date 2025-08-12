# Audio Split & Filter Tool

A Python utility to **split long audio files into clean, distinct, 5-second chunks** for machine learning datasets.  
Perfect for sound classification projects where you need to remove duplicates, silence, and low-quality samples.

---

## Features
- **Automatic splitting** into 5-second WAV snippets  
- **Silence removal** based on RMS energy  
- **Minimum duration filtering** (default: 2s)  
- **Duplicate similarity filtering** using Mel spectrogram fingerprints  
- **File renaming** with underscores for clean dataset naming  
- **Dependency auto-installation** — just run and go!  

---

## Installation & Setup

1. **Clone the repository**  
   git clone https://github.com/haanhtuandev/audio-split-tool.git
   cd audio-split-tool

2. **Create a virtual environment**  
   Creating a virtual environment ensures that your dependencies are isolated from your global Python installation.  
   python -m venv .venv

3. **Activate the virtual environment**  
   - **macOS/Linux**:  
     source .venv/bin/activate  
   - **Windows (PowerShell)**:  
     .venv\Scripts\activate

4. **Prepare your directories**  
   Create the input and output folders:  
   mkdir -p raw_wavs split_wavs

---

## Usage

1. **Add audio files**  
   Place your `.wav`, `.mp3`, or `.flac` files in the `raw_wavs/` folder.

2. **Run the tool**  
   The script will:
   - Split each audio into 5-second chunks
   - Remove silence and too-short segments
   - Filter out near-duplicate clips
   - Save results in `split_wavs/`  
   python converter.py

3. **Review output**  
   Processed files will be saved in `split_wavs/` with standardized filenames:  
   example_audio_part1.wav  
   example_audio_part2.wav

---

## Example

**Input** (`raw_wavs/`):  
chainsaw_recording.wav  
leaf_blower.mp3

**Output** (`split_wavs/`):  
chainsaw_recording_part1.wav  
chainsaw_recording_part2.wav  
leaf_blower_part1.wav  
leaf_blower_part2.wav

*(silent, too-short, or duplicate clips are automatically removed)*

---

## Requirements
- Python 3.8+  
- Supported formats: `.wav`, `.mp3`, `.flac`  
- No manual dependency installation needed — the script will auto-install what it needs.

---

## Notes
- To reprocess from scratch, you can safely delete `split_wavs/` and rerun the script.
- For best results, start with **clean, high-quality source audio**.
