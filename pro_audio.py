import numpy as np
from scipy.io import wavfile

def generate_pro_sleep_audio(duration_sec=600, sample_rate=44100):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # 4Hz Delta Wave (200Hz vs 204Hz)
    left_wave = 0.1 * np.sin(2 * np.pi * 200 * t)
    right_wave = 0.1 * np.sin(2 * np.pi * 204 * t)
    
    # Brown Noise (Random Walk)
    white_noise = np.random.uniform(-1, 1, len(t))
    brown_noise = np.cumsum(white_noise)
    brown_noise /= np.max(np.abs(brown_noise))
    brown_noise *= 0.2  # Keep it subtle
    
    # Mix
    left_mix = left_wave + brown_noise
    right_mix = right_wave + brown_noise
    
    # 10-second Crossfade to prevent looping clicks
    fade_samples = 10 * sample_rate
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    
    for channel in [left_mix, right_mix]:
        end_part = channel[-fade_samples:] * fade_out
        start_part = channel[:fade_samples] * fade_in
        channel[:fade_samples] = start_part + end_part

    audio = np.vstack((left_mix, right_mix)).T
    audio = np.clip(audio, -1, 1)
    wavfile.write('pro_sleep_seed.wav', sample_rate, (audio * 32767).astype(np.uint16))

if __name__ == "__main__":
    generate_pro_sleep_audio()
