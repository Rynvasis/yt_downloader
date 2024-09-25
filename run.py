
import termcolor
from customtkinter import *
from customtkinter import filedialog
import threading
from PIL import Image
import time
import yt_dlp
import subprocess

# Function to get the path to bundled resources
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        return None

    return os.path.join(base_path, relative_path)


class Spinbox(CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: int, command: callable = None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = CTkButton(self, text="-", width=height - 6, height=height - 6, command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = CTkEntry(self, width=width - (2 * height), height=height - 6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = CTkButton(self, text="+", width=height - 6, height=height - 6, command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self):
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))

def terminate_program():
    # Close the terminal window
    subprocess.Popen("taskkill /F /T /PID {}".format(os.getpid()), shell=True)



resoul = []
#====================================================================================
def get_playlist_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # This option extracts metadata without downloading videos
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if 'formats' in info_dict:
            resolutions = set()
            unique_formats = []
            for format in info_dict['formats']:
                if 'height' in format and format['height'] is not None:
                    if format['height'] not in resolutions:
                        if format['height'] not in [27,45,90,180]:
                          resolutions.add(format['height'])
                          unique_formats.append(format)
            return unique_formats
        else:
            return []
def get_video_title(url):
    ydl_opts={
        'quiet' : True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url,download=False)
        return info_dict['title']
    
def avaliable_res(playlistInfo):
    first_video_url = playlistInfo['entries'][2]['url']  # Get URL of the first video in the playlist
    available_resolutions = get_video_info(first_video_url)
    return available_resolutions


# def progress_hook(d):
#     if d['status'] == 'downloading':
#         total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
#         downloaded_bytes = d.get('downloaded_bytes')
#         if total_bytes:
#             # percentage = (downloaded_bytes / total_bytes) * 100
#             # print(f"Downloaded {downloaded_bytes / (1024 * 1024):.2f} MB of {total_bytes / (1024 * 1024):.2f} MB ({percentage:.2f}%)")
#             return f'{downloaded_bytes / (1024 * 1024):.2f} MB'

def download_videos(url, output_path='.', resolution=None, start_index=None, end_index=None,ffmpeg_path=None, ffplay_path=None, ffprobe_path=None):
    def update_progress(message):
        # Delete the last line in the textarea
        textarea.delete('end - 2 lines', 'end - 1 lines')  # Delete the last line
        
        # Insert the new progress message in the next line
        textarea.tag_config("colored_tag", foreground="#33FF7D")
        textarea.insert("end", message + "\n","colored_tag")
        # textarea.yview("end")
    
    temp = 1
    # textarea.delete('1.0',"end")
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4',
        # 'progress_hooks': [lambda d: update_progress(d)],
        'progress_hooks': [lambda d: update_progress(f"[download] {d['_percent_str'][7:-4]} of ~ {d.get('downloaded_bytes')/ (1024 * 1024):.2f}MB at {d['_speed_str'][7:-4]}")],
    }
    if resolution:
        ydl_opts['format'] = f"bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=mp4]/mp4"
    
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path
    
    if ffplay_path:
        ydl_opts['ffplay_location'] = ffplay_path
    
    if ffprobe_path:
        ydl_opts['ffprobe_location'] = ffprobe_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if 'playlist' in url:
            playlist_info = get_playlist_info(url)
            total_videos = len(playlist_info.get('entries', []))

            if start_index is None or start_index < 1:
                start_index = 1
            if end_index is None or end_index > total_videos:
                end_index = total_videos
            total_videos_to_download = int(end_index)-int(start_index) + 1
            entries_to_download = playlist_info['entries'][start_index-1:end_index]
            for i, entry in enumerate(entries_to_download, start=start_index):
              
                print(f"Downloading video {i} of {total_videos}: {entry['title']}")
                # update_progress(f"\r[download] {i}/{total_videos} - {entry['title']}")
                textarea.insert("end",f"Downloading >> {i}.{entry['title']}...\n")
                textarea.insert("end","\n")
                ydl.download(entry['url'])
                # print("Done...")
                print(termcolor.colored(">> downloaded <<\n" ,color="green"))
                textarea.tag_config("colored_tag", foreground="#33FF7D")
                textarea.delete('end - 2 lines', 'end - 1 lines')
                # update_progress(f"\r[download] {i}/{total_videos} - {entry['title']} - Done")
                textarea.insert("end",">> downloaded <<\n","colored_tag")
                textarea.yview("end")
                
                progress_value = temp/total_videos_to_download 
                progress_value_label = int(progress_value * 100)
                
                progressvar.set(progress_value)
                txt = "Downloading..."+ f"{progress_value_label}" + "%"
                progress_label.configure(text=txt)
                # file_name = f"{video.title}"
                # rename_video(download_path,file_name,count)
                temp = temp + 1
        else:
                title = get_video_title(url)
                print(f"Downloading video: {title}")
                textarea.insert("end", f"Downloading >> {title}...\n")
                textarea.insert("end","\n")
                ydl.download(url)
                print(termcolor.colored(">> downloaded <<\n", color="green"))
                textarea.tag_config("colored_tag", foreground="#33FF7D")
                textarea.delete('end - 2 lines', 'end - 1 lines')
                textarea.insert("end", ">> downloaded <<\n", "colored_tag")
                textarea.yview("end")

                progressvar.set(100)
                progress_label.configure(text="Downloading...100%")

#====================================================================================
root = CTk()
root.title("Youtube Downloader")
root.geometry("600x500")
root.resizable(False, False)
root.iconbitmap('downloader.ico')
def optionmenu_callback(choice):
    return choice[:-1]
def show_progressbar():
    global resoul
    link = ytLink.get()
    if ytLink.get() and folderLink.get() :
        if 'playlist' in link:
          if endEntry.get() and startEntry.get():
            if int(startEntry.get()) <= int(endEntry.get()):
                download.place_forget()
                progress_label.place(x=260, y=420)
                progressbar.place(x=160, y=460)
                progress_label.configure(text="Downloading...")
                progressvar.set(0)
                threading.Thread(target=yt_down).start()
        else:
            download.place_forget()
            progress_label.place(x=260, y=420)
            progressbar.place(x=160, y=460)
            progress_label.configure(text="Downloading...")
            progressvar.set(0)
            threading.Thread(target=yt_down).start()
    else:
        textarea.delete("1.0", "end")
        textarea.tag_config("error_tag", foreground="red")
        textarea.insert("end", "Please Enter Valid Number Videos !!!\n", "error_tag")

def browse():
    dirctory = filedialog.askdirectory(title="Save list")
    folderLink.delete(0, "end")
    folderLink.insert(0, dirctory)
def appear_start_end():
    startLabel.place(x=50, y=235)
    startEntry.place(x=133, y=235)
    startEntry.set(0)

    endLabel.place(x=390,y=235)
    endEntry.place(x=448,y=235)
    endEntry.set(0)
def forget_start_end():
    startLabel.place_forget()
    startEntry.place_forget()
    # startEntry.set(0)

    endLabel.place_forget()
    endEntry.place_forget()
    # endEntry.set(0)
def yt_down():
    global resoul

    link = ytLink.get()
    folder = folderLink.get()
    # count = int(startEntry.get())
    if 'playlist' in link:
      start_index = startEntry.get()
      end_index = endEntry.get()

    textarea.delete('1.0', "end")

    if 'playlist' in link:
        ffmpeg_path = resource_path("ffmpeg.exe")
        ffplay_path = resource_path("ffplay.exe")
        ffprobe_path = resource_path("ffprobe.exe")
        print(f"Path to ffmpeg: {ffmpeg_path}")
        print(f"Path to ffplay: {ffplay_path}")
        print(f"Path to ffprobe: {ffprobe_path}")
        playlist_info = get_playlist_info(link)
        total_videos = len(playlist_info.get('entries', []))
        # print(f"Total videos in the playlist: {total_videos}")

        start_index = int(start_index) or 1
        end_index = int(end_index) or total_videos

        if start_index > end_index or start_index < 1 or end_index > total_videos:
            print("Invalid range. Please check your input and try again.")
        else:
            resoul = avaliable_res(playlist_info)
            if resoul:
                # optionmenu.configure(values=[f"{res['height']}p" for res in resoul])
                choice = optionmenu_callback(optionmenu.get())
                download_videos(link, folder, choice, start_index=start_index, end_index=end_index,ffmpeg_path=ffmpeg_path, ffplay_path=ffplay_path, ffprobe_path=ffprobe_path)

    # elif 'linkedin'in link:
    #     ffmpeg_path = resource_path("ffmpeg.exe")
    #     ffplay_path = resource_path("ffplay.exe")
    #     ffprobe_path = resource_path("ffprobe.exe")
    #     print(f"Path to ffmpeg: {ffmpeg_path}")
    #     print(f"Path to ffplay: {ffplay_path}")
    #     print(f"Path to ffprobe: {ffprobe_path}")
    #     download_videos(link,folder,ffmpeg_path=ffmpeg_path, ffplay_path=ffplay_path, ffprobe_path=ffprobe_path)
    else:
        ffmpeg_path = resource_path("ffmpeg.exe")
        ffplay_path = resource_path("ffplay.exe")
        ffprobe_path = resource_path("ffprobe.exe")
        print(f"Path to ffmpeg: {ffmpeg_path}")
        print(f"Path to ffplay: {ffplay_path}")
        print(f"Path to ffprobe: {ffprobe_path}")
        available_resolutions = get_video_info(link)
        if available_resolutions:
            resoul = available_resolutions
            # optionmenu.configure(values=[f"{res['height']}p" for res in resoul])
            choice = optionmenu_callback(optionmenu.get())
            if choice:
              download_videos(link, folder, choice,ffmpeg_path=ffmpeg_path, ffplay_path=ffplay_path, ffprobe_path=ffprobe_path)
        else:
          download_videos(link,folder,ffmpeg_path=ffmpeg_path, ffplay_path=ffplay_path, ffprobe_path=ffprobe_path)

    print("\nDownload complete!")
    textarea.insert("end", "\nDownload complete!", "colored_tag")
    textarea.yview("end")

    time.sleep(1)
    progressbar.place_forget()
    progress_label.place_forget()
    download.place(x=220, y=440)

class PlaceholderEntry(CTkEntry):
    def __init__(self, master=None, placeholder=None, color='grey62', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_text_color = self.cget("text_color")
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self._add_placeholder()

    def _clear_placeholder(self, e):
        if self.get() == self.placeholder and self.cget("text_color") == self.placeholder_color:
            self.delete(0, "end")
            self.configure(text_color=self.default_text_color)

    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(text_color=self.placeholder_color)



# Define global variables
after_id = None  # Initialize after_id as None

def url_check():
    global resoul
    global after_id  # Access the global after_id variable
    link = ytLink.get()
    # print(link)
    if link == '':
            resoul.clear()
            optionmenu.configure(values=[])
            optionmenu.set("Resolution")
    else:   
      if 'https' in link:
        if 'playlist' in link:
            appear_start_end()
            playlist_info = get_playlist_info(link)
            resoul = avaliable_res(playlist_info)
        else:
            forget_start_end()
            # if link == '':
            #   resoul.clear()
            #   optionmenu.configure(values=[])
            #   optionmenu.set("Resolution")
            # else:
            resoul = get_video_info(link)

        if resoul:
            optionmenu.configure(values=[f"{res['height']}p" for res in resoul])
            optionmenu.set(f'{resoul[0]['height']}p')  # Set default selection
        else:
            optionmenu.set("Auto")
def url_check_delayed(*args):
    global after_id  # Access the global after_id variable
    
    # Cancel any previously scheduled callback
    if after_id:
        root.after_cancel(after_id)
    # Schedule a new callback after some seconds 1 sec == 1000
    after_id = root.after(1, thread_url_check)

def thread_url_check(*args):
    thread = threading.Thread(target=url_check)
    thread.start()
# Youtube link
ytLabel = CTkLabel(root, text="Playlist URL")
ytLabel.place(x=30, y=165)

ytLink_var = StringVar()
ytLink_var.trace_add("write", url_check_delayed)

ytLink = PlaceholderEntry(root, textvariable=ytLink_var, placeholder="Enter Playlist URL", width=300)
ytLink.place(x=133, y=165)

# Download Folder
folderLabel = CTkLabel(root, text="Downloader Folder")
folderLabel.place(x=18, y=198)

folderLink = CTkEntry(root, placeholder_text="Enter The Path", width=300)
folderLink.place(x=133, y=198)

# Browse Button
browse = CTkButton(root, text="Browse", command=browse)
browse.place(x=448, y=198)

# Download Button
download = CTkButton(root, text="Download", command=show_progressbar)
download.place(x=220, y=450)

# Start
startLabel = CTkLabel(root, text="Start")
# startLabel.place(x=50, y=235)

startEntry = Spinbox(root, width=100, step_size=1)
# startEntry.place(x=133, y=235)
# startEntry.set(0)

# End
endLabel= CTkLabel(root ,text="End ")
# endLabel.place(x=390,y=235)

endEntry = Spinbox(root,width=100,step_size=1)
# endEntry.place(x=448,y=235)
# endEntry.set(0)

# Option Menu
optionmenu = CTkOptionMenu(root, values=resoul or [], command=optionmenu_callback)
optionmenu.place(x=448, y=165)
optionmenu.set("Resolution")
# Text Area
frame = CTkFrame(root, width=500, height=130)
frame.place(x=50, y=290)
textarea = CTkTextbox(root, width=500, height=130)
textarea.place(x=50, y=290)

# Progress Bar
progressvar = DoubleVar()
progressbar = CTkProgressBar(root, variable=progressvar, width=300, mode="determinate")

# Progress Label
progress_label = CTkLabel(root, text="Loading...")

# Photo Logo
logo = CTkImage(dark_image=Image.open(r'downloaderLogo.png'), size=(230, 170))
yt_logo = CTkLabel(root, text="", image=logo)
yt_logo.place(relx=0.5, rely=0.15, anchor="center")
# Bind the close event to terminate_program function
root.protocol("WM_DELETE_WINDOW", terminate_program)
root.mainloop()




