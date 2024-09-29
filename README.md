# Video Downloader

This is a simple Python video downloading that can download from various online services like YouTube, Facebook, etc...

## Requirements
Before running the project, make sure you have the following:
- **Python 3.x**
- **FFmpeg**: You must download and install FFmpeg and add it to your system's environment path.

### Installing FFmpeg:
 1. On **Windows**:
   - Download FFmpeg from [here](https://ffmpeg.org/download.html).
   - Extract the files.
   - Add FFmpeg to your environment path:
   - Open *Start*, search for **Environment Variables**, and select *Edit the system environment variables*.
   - In the *System Properties* window, click **Environment Variables**.
   - Under **System Variables**, find the **Path** variable, select it, and click **Edit**.
   - Click **New** and add the path to the extracted FFmpeg folder.
   - Click **OK** to close all windows.
 2. On **Linux/MacOS**:
     ```
     sudo apt update
     ```
     ```
     sudo apt install ffmpeg
     ```
### Cloning the Repository:
To clone this repository, follow these steps:
1. Open a terminal.
2. Run the following command:
   ```
   git clone https://github.com/Rynvasis/yt_downloader.git
   ```
   ```
   cd yt_downloader
   ```
   ```
   python run.py
   ```

