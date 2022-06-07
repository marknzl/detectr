# detectr
Simple license plate detection program which uses techniques learned from CS373.

## Intro
The aim of this project was to utilize image processing techniques such as contrast stretching, thresholding, and various image morphology processes.

The program takes in a picture of a license plate like so:
![example input](readme_assets/example_input.png)

And outputs the same image with a bounding box around the license plate:
![example detection](readme_assets/example_detection.png)

## How it works

### Step 1: Conversion to greyscale
The first step is to convert the input image to greyscale. Reason being is in our context of license plate detection here, the colour information of the image is irrelevant.

### Step 2: Contrast stretching
After converting our image to greyscale, we want to **contrast stretch** the image. **Contrast stretching** is a simple process of improving the contrast within an image by stretching the range of intensity values in the image. In our case, the range is 0 - 255.

### Step 3: Standard deviation filtering
// TODO