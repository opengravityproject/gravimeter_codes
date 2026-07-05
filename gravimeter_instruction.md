# Gravimeter Code Instructions

This repository contains utility code for the Open Gravity gravimeter setup.

## Files

- `interval_capture_2.py` - runs on the Roberto Raspberry Pi. It captures one image every 60 seconds, turns the laser on before each capture, saves the image, then turns the laser back off.

## Roberto Image Capture

Use `interval_capture_2.py` on the Roberto Raspberry Pi, where the camera and laser GPIO control are connected.

### What the Script Does

- Uses `picamera2` for still image capture.
- Uses GPIO pin `4` through `pinctrl` to control the laser.
- Turns the laser on for 5 seconds before each capture.
- Saves images into a local `data_images` directory.
- Names captures like `capture_YYYYMMDD_HHMMSS_microseconds.jpg`.
- Repeats every `60` seconds until stopped.
- On `Ctrl+C`, turns the laser off and stops the camera.

### Run on Roberto

From the Roberto device:

```bash
cd ~/camera_test
python3 interval_capture_2.py
```

Leave the process running while collecting image data. Stop it with `Ctrl+C` so the cleanup handler turns the laser off and stops the camera.

### Configuration

The main settings are at the top of `interval_capture_2.py`:

```python
PIN = 4
INTERVAL_SECONDS = 60
CAPTURE_DIR = "data_images"
```

Change `INTERVAL_SECONDS` to capture more or less frequently. Change `CAPTURE_DIR` only if the downstream image sync and processing workflow is updated to match.

## Syncing Captures for Processing

New Roberto images are normally synced into the Open Gravity processing workspace with an ignore-existing rsync pattern so only new images are copied.

Current processing destination:

```text
/mnt/wdhdd/open_gravity/captures_isobaric_0523
```

Example sync pattern:

```bash
rsync -avz --ignore-existing roberto@192.168.50.81:~/camera_test/data_images/ /mnt/wdhdd/open_gravity/captures_isobaric_0523/
```

## Processing Images

The image processing pipeline lives outside this repo in the Open Gravity workspace. The current run pattern is:

```bash
source /home/rob/torch-cu126/bin/activate
cd /mnt/wdhdd/open_gravity
python3 new_image_processing.py
```

This pipeline downloads new images, crops them, computes centroid outputs, and writes the downstream gravity analysis files used for plotting.

## GitHub Workflow

Local clone path on the node:

```text
/home/rob/repos/gravimeter_codes
```

Use the Alanclaw SSH key explicitly when pushing:

```bash
cd /home/rob/repos/gravimeter_codes
GIT_SSH_COMMAND="ssh -i ~/.ssh/Alanclaw_key -o IdentitiesOnly=yes" git push origin main
```
