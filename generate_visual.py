import cv2
import numpy as np
import sys
import random

def create_visual(mode, duration_min=10, fps=24):
    width, height = 1920, 1080
    out = cv2.VideoWriter(f'visual_{mode}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    total_frames = duration_min * 60 * fps

    # Initialization
    stars = [{'x': random.randint(0, width), 'y': random.randint(0, height), 's': random.uniform(0.5, 2)} for _ in range(150)]
    rain_drops = [[random.randint(0, width), random.randint(0, height), random.randint(10, 20)] for _ in range(100)]

    for f in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        if mode == "stars":
            for s in stars:
                s['x'] += 0.2
                if s['x'] > width: s['x'] = 0
                cv2.circle(frame, (int(s['x']), int(s['y'])), int(s['s']), (200, 200, 200), -1)
        
        elif mode == "rain":
            for d in rain_drops:
                d[1] += d[2]
                if d[1] > height: d[1] = -20; d[0] = random.randint(0, width)
                cv2.line(frame, (d[0], d[1]), (d[0], d[1]+15), (100, 100, 100), 1)
        
        elif mode == "nebula":
            t = f / (fps * 15)
            c1 = np.array([40, 10, 20]) # Deep Purple
            c2 = np.array([20, 30, 10]) # Dark Teal
            mix = (np.sin(2 * np.pi * t) + 1) / 2
            frame[:] = (c1 * mix + c2 * (1-mix)).astype(np.uint8)

        # Text Overlay
        cv2.putText(frame, "4Hz Delta Wave // Deep Sleep", (50, 1030), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 1, cv2.LINE_AA)
        
        out.write(frame)
    out.release()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "stars"
    create_visual(mode)
