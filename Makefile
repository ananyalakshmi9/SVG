FLAVOR ?= stars
HOURS ?= 10
PYTHON = python3
FFMPEG = ffmpeg

# File names
AUDIO_SEED = pro_sleep_seed.wav
VIDEO_SEED = visual_$(FLAVOR).mp4
MODULE = seed_$(FLAVOR).mp4
FINAL = sleep_$(FLAVOR)_$(HOURS)hr.mp4
LIST = list_$(FLAVOR).txt

all: $(FINAL)

$(AUDIO_SEED): pro_audio.py
	$(PYTHON) pro_audio.py

$(VIDEO_SEED): generate_visual.py
	$(PYTHON) generate_visual.py $(FLAVOR)

$(MODULE): $(AUDIO_SEED) $(VIDEO_SEED)
	$(FFMPEG) -y -i $(VIDEO_SEED) -i $(AUDIO_SEED) -c:v libx264 -crf 23 -c:a aac -shortest $(MODULE)

$(FINAL): $(MODULE)
	@rm -f $(LIST)
	@LOOPS=$$(($(HOURS) * 6)); \
	for i in $$(seq 1 $$LOOPS); do echo "file '$(MODULE)'" >> $(LIST); done
	$(FFMPEG) -y -f concat -safe 0 -i $(LIST) -c copy $(FINAL)
	@rm $(LIST)
	@echo "Build Complete: $(FINAL)"

clean:
	rm -f *.wav *.mp4 *.txt
