# Audio Split & Filter Tool

A Python utility to **split long audio files into clean, distinct, 5-second chunks** for machine learning datasets.  
Perfect for sound classification projects where you need to remove duplicates, silence, and low-quality samples.

## Features
- **Automatic splitting** into 5-second WAV snippets  
- **Silence removal** based on RMS energy  
- **Minimum duration filtering** (default: 2s)  
- **Duplicate similarity filtering** using Mel spectrogram fingerprints  
- **File renaming** with underscores for clean dataset naming  
- **Dependency auto-installation** — just run and go!  

## Quick Start (One-Liner)
```bash
git clone <https://github.com/haanhtuandev/audio-split-tool.git> audio-tool && cd audio-tool && python -m venv .venv && source .venv/bin/activate && mkdir -p raw_wavs split_wavs && python converter.py
