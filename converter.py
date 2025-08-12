import os
import importlib
import subprocess
import sys
import shutil

# ---------- Auto-install Helper ----------
def ensure_package(pkg_name):
    try:
        importlib.import_module(pkg_name)
    except ImportError:
        print(f"📦 Installing missing package: {pkg_name} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        print(f"✅ Installed {pkg_name}.")

# Ensure all dependencies
for pkg in ["numpy", "librosa", "pydub", "soundfile"]:
    ensure_package(pkg)

# Now safe to import
import numpy as np
import librosa
from pydub import AudioSegment

# ---------- Audio Checks ----------
def audio_fingerprint(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=64)
    log_mel = librosa.power_to_db(mel)
    norm = np.linalg.norm(log_mel)
    return log_mel.flatten() / norm if norm != 0 else log_mel.flatten()

def is_similar(f1, f2, threshold=0.90):
    try:
        fp1 = audio_fingerprint(f1)
        fp2 = audio_fingerprint(f2)
        similarity = np.dot(fp1, fp2)
        return similarity > threshold
    except Exception as e:
        print(f"[WARN] Similarity check failed: {e}")
        return False

def is_silent_or_quiet(path, silence_rms=0.001):
    try:
        y, _ = librosa.load(path, sr=None, mono=True)
        rms = np.mean(librosa.feature.rms(y=y))
        return rms < silence_rms
    except Exception as e:
        print(f"[WARN] Silence check failed for {path}: {e}")
        return False

def is_too_short(path, min_duration=2.0):
    try:
        y, sr = librosa.load(path, sr=None, mono=True)
        duration = librosa.get_duration(y=y, sr=sr)
        return duration < min_duration
    except Exception as e:
        print(f"[WARN] Duration check failed for {path}: {e}")
        return True

# ---------- Splitting & Filtering ----------
def split_and_filter(file_path, output_folder, threshold=0.90, min_duration=2.0, silence_rms=0.001):
    audio = AudioSegment.from_file(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    base_name = base_name.replace(" ", "_")
    chunk_length_ms = 5000

    temp_folder = "_temp_chunks"
    os.makedirs(temp_folder, exist_ok=True)

    chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    chunk_paths = []

    for i, chunk in enumerate(chunks):
        out_path = os.path.join(temp_folder, f"{base_name}_part{i+1}.wav")
        chunk.export(out_path, format="wav")
        chunk_paths.append(out_path)

    chunk_paths = [
        p for p in chunk_paths
        if not is_silent_or_quiet(p, silence_rms) and not is_too_short(p, min_duration)
    ]

    unique_chunks = []
    for cp in chunk_paths:
        if not any(is_similar(cp, uc, threshold) for uc in unique_chunks):
            unique_chunks.append(cp)
        else:
            print(f"[SKIP] {os.path.basename(cp)} is too similar to another chunk.")

    for idx, cp in enumerate(unique_chunks):
        final_path = os.path.join(output_folder, f"{base_name}_unique{idx+1}.wav")
        shutil.move(cp, final_path)

    shutil.rmtree(temp_folder, ignore_errors=True)
    print(f"[OK] {file_path} → {len(unique_chunks)} distinct, valid chunks.")

# ---------- Main Processing ----------
def process_all(input_folder, output_folder, threshold=0.90, min_duration=2.0, silence_rms=0.001):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    all_files = [os.path.join(input_folder, f)
                 for f in os.listdir(input_folder)
                 if f.lower().endswith((".wav", ".mp3", ".flac"))]

    print(f"[INFO] Found {len(all_files)} files in {input_folder}")
    for f in all_files:
        split_and_filter(f, output_folder, threshold, min_duration, silence_rms)

    final_count = len([f for f in os.listdir(output_folder) if f.endswith(".wav")])
    print(f"\n✅ Processing complete — {final_count} files saved in '{output_folder}'.")

if __name__ == "__main__":
    process_all("raw_wavs", "split_wavs", threshold=0.90, min_duration=2.0, silence_rms=0.001)
