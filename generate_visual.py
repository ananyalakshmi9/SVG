import cv2
import numpy as np
import sys
import random
import argparse

def create_visual(mode, topic, frequency, duration_min=10, fps=24):
    width, height = 1920, 1080
    # Dynamic Filename for the Makefile to find
    filename = f'seed_video.mp4'
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    total_frames = duration_min * 60 * fps

    # Initialization
    stars = [{'x': random.randint(0, width), 'y': random.randint(0, height), 's': random.uniform(0.5, 2)} for _ in range(150)]
    rain_drops = [[random.randint(0, width), random.randint(0, height), random.randint(10, 20)] for _ in range(120)]

    for f in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        if mode == "stars":
            for s in stars:
                s['x'] += 0.15 # Slow, calming movement
                if s['x'] > width: s['x'] = 0
                cv2.circle(frame, (int(s['x']), int(s['y'])), int(s['s']), (180, 180, 180), -1)
        
        elif mode == "rain":
            for d in rain_drops:
                d[1] += d[2]
                if d[1] > height: 
                    d[1] = -20
                    d[0] = random.randint(0, width)
                # Thinner, more elegant rain lines
                cv2.line(frame, (d[0], d[1]), (d[0], d[1]+12), (90, 90, 90), 1)
        
        elif mode == "nebula":
            # Pulsing "Aura" effect
            t = f / (fps * 20)
            c1 = np.array([30, 10, 25]) # Deep Indigo
            c2 = np.array([15, 15, 35]) # Midnight Purple
            mix = (np.sin(2 * np.pi * t) + 1) / 2
            frame[:] = (c1 * mix + c2 * (1-mix)).astype(np.uint8)

        # --- AURA LABS BRANDING OVERLAY ---
        # Subtle watermark for trust
        brand_text = f"AURA LABS // {frequency} // {topic}"
        cv2.putText(frame, brand_text, (60, 1020), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (60, 60, 60), 1, cv2.LINE_AA)
        
        # Simple "Progress Bar" at the bottom (very subtle)
        progress_w = int((f / total_frames) * width)
        cv2.line(frame, (0, 1079), (progress_w, 1079), (40, 40, 40), 2)
        
        out.write(frame)
        
    out.release()
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="stars")
    parser.add_argument("--topic", default="Deep Sleep")
    parser.add_argument("--freq", default="432Hz")
    args = parser.parse_args()

    # Trigger visual generation
    create_visual(mode=args.mode, topic=args.topic, frequency=args.freq)
