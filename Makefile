# Variables passed from GitHub Actions
FLAVOR ?= rain
HOURS ?= 10
TOPIC ?= Healing
SEED_MINS = 10
REPEATS = $(shell echo $$(($(HOURS) * 60 / $(SEED_MINS))))

# File Names
AUDIO_SEED = seed_audio.wav
VIDEO_SEED = seed_video.mp4
CONCAT_LIST = inputs.txt
FINAL_NAME = "Aura_Labs_$(FLAVOR)_$(HOURS)hr_$(TOPIC).mp4"

all: clean generate_seeds loop finalize

generate_seeds:
	@echo "Step 1: Generating 10-minute seeds..."
	python pro_audio.py
	python generate_visual.py --flavor $(FLAVOR)

loop:
	@echo "Step 2: Creating concat list for $(REPEATS) repeats..."
	@for i in $$(seq 1 $(REPEATS)); do echo "file '$(VIDEO_SEED)'" >> $(CONCAT_LIST); done
	@echo "Step 3: Stitched 10-hour render (Stream Copying)..."
	ffmpeg -f concat -safe 0 -i $(CONCAT_LIST) -i $(AUDIO_SEED) -c copy -map 0:v:0 -map 1:a:0 output_full.mp4

finalize:
	@echo "Step 4: Renaming for SEO..."
	mv output_full.mp4 $(FINAL_NAME)
	@echo "Build Complete: $(FINAL_NAME)"

clean:
	rm -f *.mp4 *.wav *.txt
