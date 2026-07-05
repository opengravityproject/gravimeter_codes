# Gravimeter Code Instructions

This repository contains utility code for operating a camera-based gravimeter data collection system.

## Overview

The current capture script periodically records still images from a Raspberry Pi camera while controlling an external illumination or laser output through a GPIO pin. The images are saved locally with timestamped filenames so they can be transferred later into a separate processing pipeline.

## Files

- `interval_capture_2.py` - captures still images at a fixed interval while toggling a configured GPIO output around each exposure.

## Requirements

Run the capture script on a Raspberry Pi or compatible system with:

- Python 3
- `picamera2`
- `pinctrl`
- A configured camera module
- A GPIO-connected illumination or laser control line, if that part of the setup is used

The script assumes `pinctrl` can set the configured pin high and low. If the hardware uses a different control method, update the GPIO helper functions before running it.

## Configuration

The main settings are near the top of `interval_capture_2.py`:

```python
PIN = 4
INTERVAL_SECONDS = 60
CAPTURE_DIR = "data_images"
```

- `PIN` is the GPIO pin used for illumination control.
- `INTERVAL_SECONDS` is the target time between capture starts.
- `CAPTURE_DIR` is the directory where image files are written.

Adjust these values to match the hardware and data collection plan before starting a long run.

## Running Image Capture

From the directory containing the script:

```bash
python3 interval_capture_2.py
```

The script will:

1. Create the capture directory if it does not already exist.
2. Start the camera.
3. Turn the configured GPIO output on before each image.
4. Save a timestamped JPG image.
5. Turn the GPIO output off after the capture.
6. Repeat at the configured interval.

Stop the process with `Ctrl+C`. The interrupt handler turns the GPIO output off and stops the camera.

## Output Files

Captured images are written under `CAPTURE_DIR` with names like:

```text
capture_YYYYMMDD_HHMMSS_microseconds.jpg
```

Keep the timestamped filename format if downstream processing depends on chronological ordering.

## Transferring Data

Use a transfer method that only copies new images when moving captures to a processing machine. For example:

```bash
rsync -av --ignore-existing /path/to/captures/ user@processing-host:/path/to/destination/
```

Do not delete raw capture files until the transfer and downstream processing outputs have been verified.

## Processing

Image processing is intentionally separate from this capture script. A typical processing workflow should:

1. Ingest newly captured JPG files.
2. Crop or normalize the images if required.
3. Extract the measurement feature, such as a centroid or position estimate.
4. Write timestamped analysis outputs for plotting and comparison.
5. Preserve enough metadata to trace processed results back to raw captures.

Document any site-specific processing commands in deployment notes outside this generic repository guide.
