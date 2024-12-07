# Image Downloader from CSV with IPv4 Enforcement

This Python script downloads images from URLs listed in a CSV file and saves them to a specified folder. It forces the use of IPv4 for network connections, making it ideal for environments where IPv6 may cause issues.

## Features

- Reads a CSV file to find image URLs.
- Automatically identifies the column containing image links.
- Saves downloaded images to a specified folder.
- Skips downloading if the image already exists.
- Forces IPv4 for all network requests.
- Handles errors gracefully, including network timeouts and invalid URLs.

## Requirements

- Python 3.6 or higher
- Required Python libraries:
  - `pandas`
  - `requests`

## Usage 

- name,image_url
- Photo1,https://example.com/image1.png
- Photo2,https://example.com/image2.png

## Run the Script

python image_downloader.py

## Customize Input and Output

- file.csv as the default input file.
- Output/ as the default folder for saving images.

Modify the csv_file and output_folder variables in the script to change the input file and destination folder.