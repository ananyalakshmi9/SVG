import numpy as np
from scipy.io import wavfile
import argparse
import re
import sys

def generate_aura_audio(duration_sec=600, sample_rate=44100, freq_input="432"):
    """
    Generates a professional-grade binaural audio seed with brown noise.
    Supports single or multiple frequency layering.
    """
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # --- SMART MULTI-FREQUENCY PARSER ---
    # Finds all numbers in the input string (e.g., "14Hz + 40Hz" -> [14.0, 40.0])
    freqs = [float(f) for f in re.findall(r"(\d+\.?\d*)", freq_input)]
    
    if not freqs:
        print("WARNING: No frequency detected. Defaulting to 432Hz.")
        freqs = [432.0]
    
    print(f"AURA LABS ENGINEERING: Layering frequencies: {freqs}")

    # Initialize empty channels
    left_mix = np.zeros_like(t)
    right_mix = np.zeros_like(t)

    # Scale amplitude by number of frequencies to prevent digital clipping
    # 0.08 is the sweet spot for layering without distortion
    amp = 0.08 / len(freqs) 
    
    for base_f in freqs:
        # Generate Binaural Beats
        # Left Channel: Base Frequency
        # Right Channel: Base Frequency + 4Hz (Delta offset for brain stabilization)
        left_mix += amp * np.sin(2 * np.pi * base_f * t)
        right_mix += amp * np.sin(2 * np.pi * (base_f + 4) * t)
    
    # --- AURA SIGNATURE BROWN NOISE ---
    # Brown noise provides the 'deep' atmospheric base (like a heavy rain/rumble)
    white_noise = np.random.uniform(-1, 1, len(t))
    brown_noise = np.cumsum(white_noise)
    # Normalize brown noise to keep it in a safe range
    brown_noise = (brown_noise - np.mean(brown_noise)) / np.max(np.abs(brown_noise))
    brown_noise *= 0.12  # Subtle volume level
    
    left_mix += brown_noise
    right_mix += brown_noise

    # --- SEAMLESS LOOP CROSSFADE ---
    # Prevents 'clicks' or 'pops' when the 10-minute seed loops in the 10-hour render
    fade_samples = 10 * sample_rate
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    for ch in [left_mix, right_mix]:
        overlap = ch[-fade_samples:] * fade_out + ch[:fade_samples] * fade_in
        ch[:fade_samples] = overlap
    
    # --- EXPORT TO 16-BIT WAV ---
    # Stack channels for stereo
    audio = np.vstack((left_mix, right_mix)).T
    # Safety clip to ensure no sample exceeds 1.0 or -1.0
    audio = np.clip(audio, -1, 1)
    
   # Convert to 16-bit PCM for standard WAV compatibility
    output_file = 'seed_audio.wav'
    wavfile.write(output_file, sample_rate, (audio * 32767).astype(np.int16))
    print(f"SUCCESS: {output_file} generated at {sample_rate}Hz.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aura Labs Audio Engine")
    parser.add_argument("--freq", default="432", help="Input frequency string (e.g., '14Hz + 40Hz')")
    args = parser.parse_args()
    
    generate_aura_audio(freq_input=args.freq)
