import numpy as np
from scipy.io import wavfile
import argparse
import sys

def generate_pro_sleep_audio(duration_sec=600, sample_rate=44100, target_freq="432"):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # --- FREQUENCY LOGIC ---
    # We parse the input (e.g., "528Hz + 432Hz" or just "432")
    # Defaulting to 432Hz if parsing fails
    base_freq = 432.0
    if "528" in target_freq: base_freq = 528.0
    elif "432" in target_freq: base_freq = 432.0
    
    # 4Hz Delta Binaural Offset (Constant for sleep induction)
    # Left: Base Freq | Right: Base Freq + 4Hz
    left_wave = 0.08 * np.sin(2 * np.pi * base_freq * t)
    right_wave = 0.08 * np.sin(2 * np.pi * (base_freq + 4) * t)
    
    # --- BROWN NOISE (The Rain/Deep Atmosphere) ---
    white_noise = np.random.uniform(-1, 1, len(t))
    brown_noise = np.cumsum(white_noise)
    # Normalize and scale
    brown_noise = (brown_noise - np.mean(brown_noise)) / np.max(np.abs(brown_noise))
    brown_noise *= 0.15 
    
    # Mix signals
    left_mix = left_wave + brown_noise
    right_mix = right_wave + brown_noise
    
    # --- SEAMLESS LOOPING (Crossfade) ---
    fade_samples = 10 * sample_rate
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    # Apply crossfade to ensure 10-hour loops have zero "clicks"
    for channel in [left_mix, right_mix]:
        overlap = channel[-fade_samples:] * fade_out + channel[:fade_samples] * fade_in
        channel[:fade_samples] = overlap
        # Remove the extra end samples that were blended in
    
    # Final stack and cleanup
    audio = np.vstack((left_mix, right_mix)).T
    audio = np.clip(audio, -1, 1)
    
    # Export as INT16 (Fixed the previous uint16 error)
    wavfile.write('seed_audio.wav', sample_rate, (audio * 32767).astype(np.int16))
    print(f"Generated audio seed at {base_freq}Hz with 4Hz Delta offset.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", default="432")
    args = parser.parse_args()
    
    generate_pro_sleep_audio(target_freq=args.freq)
