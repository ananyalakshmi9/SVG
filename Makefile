# 1. ADD THIS LINE so the Python script gets the frequency
FREQ ?= 432Hz
FLAVOR ?= rain
HOURS ?= 10
TOPIC ?= Healing
SEED_MINS = 10
REPEATS = $(shell echo $$(($(HOURS) * 60 / $(SEED_MINS))))

# File Names
VIDEO_SEED = seed_video.mp4
AUDIO_SEED = seed_audio.wav
CONCAT_LIST = inputs.txt

all: clean generate_seeds loop finalize

generate_seeds:
	@echo "Step 1: Generating dynamic seeds for $(FREQ)..."
	python pro_audio.py --freq "$(FREQ)"
	python generate_visual.py --mode $(FLAVOR) --topic "$(TOPIC)" --freq "$(FREQ)"

loop:
	@echo "Step 2: Creating concat list..."
	@for i in $$(seq 1 $(REPEATS)); do echo "file '$(VIDEO_SEED)'" >> $(CONCAT_LIST); done
	@echo "Step 3: Stitched render..."
	ffmpeg -f concat -safe 0 -i $(CONCAT_LIST) -i $(AUDIO_SEED) -c copy -map 0:v:0 -map 1:a:0 output_full.mp4

finalize:
	@echo "Step 4: Renaming for SEO..."
	# 2. UPDATED THIS LINE: Simplified filename to avoid space errors
	mv output_full.mp4 "Aura_Labs_$(FLAVOR)_$(HOURS)hr.mp4"

clean:
	rm -f *.mp4 *.wav *.txt
