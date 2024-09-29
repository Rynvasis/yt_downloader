# Video Downloader

This is a simple Python video downloader that allows you to download videos from various online services like YouTube, Facebook, and more.

## Requirements

Before running the project, ensure you have the following:

- **Python 3.x** installed.
- **FFmpeg** installed and added to your system's environment path.

### Installing FFmpeg:

1. **On Windows**:
   - Download FFmpeg from [here](https://ffmpeg.org/download.html).
   - Extract the files.
   - Add FFmpeg to your environment path:
     - Open *Start*, search for **Environment Variables**, and select *Edit the system environment variables*.
     - In the *System Properties* window, click **Environment Variables**.
     - Under **System Variables**, find the **Path** variable, select it, and click **Edit**.
     - Click **New** and add the path to the `bin` folder inside the extracted FFmpeg directory.
     - Click **OK** to close all windows.

2. **On Linux/MacOS**:
   Open a terminal and run the following commands:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   
## Cloning the Repository

To get started with this project, follow these steps:

1. Open a terminal.
2. Run the following commands to clone the repository:

   ```bash
   git clone https://github.com/Rynvasis/yt_downloader.git
3. Navigate into the project directory:
   ```
   cd yt_downloader
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the program:
   ```
   python run.py
