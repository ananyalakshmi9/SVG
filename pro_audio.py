import numpy as np
from scipy.io import wavfile
import argparse
import re

def generate_dynamic_audio(duration_sec=600, sample_rate=44100, freq_input="432"):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # --- UNIVERSAL PARSER ---
    # Finds the first number in your input string (e.g., "14hz" -> 14.0)
    match = re.search(r"(\d+\.?\d*)", freq_input)
    base_freq = float(match.group(1)) if match else 432.0
    
    print(f"ENGINEERING: Generating {base_freq}Hz base with 4Hz Delta offset.")

    # Binaural Logic: Left is Base, Right is Base + 4Hz (Delta)
    # This keeps the "Aura Labs" healing signature even for Study frequencies
    left_wave = 0.08 * np.sin(2 * np.pi * base_freq * t)
    right_wave = 0.08 * np.sin(2 * np.pi * (base_freq + 4) * t)
    
    # Brown Noise Layer
    white_noise = np.random.uniform(-1, 1, len(t))
    brown_noise = np.cumsum(white_noise)
    brown_noise = (brown_noise - np.mean(brown_noise)) / np.max(np.abs(brown_noise))
    brown_noise *= 0.12 
    
    # Mixing and Seamless Loop Crossfade
    left_mix, right_mix = left_wave + brown_noise, right_wave + brown_noise
    fade_samples = 10 * sample_rate
    fade_in, fade_out = np.linspace(0, 1, fade_samples), np.linspace(1, 0, fade_samples)
    
    for ch in [left_mix, right_mix]:
        ch[:fade_samples] = ch[-fade_samples:] * fade_out + ch[:fade_samples] * fade_in
    
    audio = np.vstack((left_mix, right_mix)).T
    audio = np.clip(audio, -1, 1)
    wavfile.write('seed_audio.wav', sample_rate, (audio * 32767).astype(np.int16))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", default="432")
    args = parser.parse_args()
    generate_dynamic_audio(freq_input=args.freq)
