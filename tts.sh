#!/bin/bash

# Activate the Conda environment
source activate tts || conda activate tts

# Run the mimic3 command with the provided argument and output the audio to /workspace/output.wav
mimic3 --voice en_US/hifi-tts_low "$1" > /workspace/output.wav --length-scale 1.2

# Deactivate the Conda environment
conda deactivate
