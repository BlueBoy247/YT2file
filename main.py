"""
導入 YT2file 應用程式所需的模組和套件，以下說明它們在程式中的用途。

模組:
    os: 用於操作文件系統，如打開下載目錄和刪除暫存文件。
    sys: 用於重新啟動應用程式以套用語言設置更改。
    webbrowser: 用於在默認瀏覽器中打開網頁，如 GitHub Repository 頁面和 PayPal 贊助頁面。
    threading: 用於創建背景執行緒，如檢查更新和下載 YouTube 影片。
    gettext: 用於應用程式的國際化和本地化，支援多語言界面。
    configparser: 用於讀取和寫入應用程式的配置文件。
    tkinter (tk): 用於建立和管理 GUI 界面。
        filedialog: 用於顯示「選擇資料夾」對話框。
        messagebox: 用於顯示訊息框，如錯誤提示和下載確認對話框。
        ttk: 用於創建和管理 Tk 主題元件。
    pytube: 用於下載 YouTube 影片。
        YouTube: 用於處理和下載 YouTube 影片。
        exceptions: 用於處理 pytube 相關的異常。
    moviepy.editor: 用於影片和音訊的處理和編輯。
        VideoFileClip: 用於處理下載的影片檔。
        AudioFileClip: 用於處理下載的音訊檔。
    requests: 用於發送 HTTP 請求，檢查應用程式更新。

Import necessary modules and packages for the YT2file application.
The following descriptions describe their usage within the program.

Modules:
    os: Used for file system operations,
        such as opening the download directory and removing temporary files.
    sys: Used to restart the application to apply language settings changes.
    webbrowser: Used to open web pages in the default browser,
        such as the GitHub repository page and the PayPal donation page.
    threading: Used to run tasks in the background,
        such as checking for updates and downloading videos.
    gettext: Used for internationalization and localization of the application,
        supporting a multi-language interface.
    configparser: Used to read and write the application's configuration file.
    tkinter (tk): Used to build the graphical user interface.
        filedialog: Used to create file/directory selection dialogs.
        messagebox: Used to display message boxes, such as error prompts and information dialogs.
        ttk: Used to create and manage themed Tk widgets.
    pytube: Used to download YouTube videos.
        YouTube: Used to handle and download YouTube videos.
        exceptions: Used to handle exceptions related to pytube.
    moviepy.editor: Used for processing and editing video and audio.
        VideoFileClip: Used to handle downloaded video files.
        AudioFileClip: Used to handle downloaded audio files.
    requests: Used to send HTTP requests to check for application updates.
"""
import os
import sys
import webbrowser
import threading
import gettext
import configparser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube, exceptions
from moviepy.editor import VideoFileClip, AudioFileClip
import requests

LOCALE_DIR = "locale" # 語言文件目錄 Language file directory
CONFIG_FILE = "config.ini" # config
ICON_FILE = "icon.ico" # icon
VIDEO_TEMP_FILE = "video_temp.mp4" # 影片暫存檔 Video temp file
AUDIO_TEMP_FILE = "audio_temp.mp4" # 音訊暫存檔 Audio temp file
VERSION = "1.0.0" # 版本 Version
RELEASE_DATE = "" # 更新日期 Release date
_ = None # 翻譯 Translation

def write_config(config_data):
    """
    將配置數據寫入配置文件。

    參數：
        config_data (configparser.ConfigParser): 
            配置數據。
    
    回傳值:
        None

    Writes the given configuration data to the specified configuration file.

    Parameters:
        config_data (configparser.ConfigParser): 
            The configuration data to be written to the file.

    Returns:
        None
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as config_file:
        config_data.write(config_file)

def open_directory():
    """
    選單路徑：檔案 > 開啟下載資料夾
    開啟下載資料夾。

    參數：
        None

    回傳值:
        None

    Menu path: File > Open Download Folder
    Opens the 'download' directory.

    Parameters:
        None

    Returns:
        None
    """
    os.startfile("download")

def exit_app():
    """
    選單路徑：檔案 > 結束
    結束應用程式。

    參數：
        None

    回傳值:
        None

    Menu path: File > Exit
    Closes the application.

    Parameters:
        None

    Returns:
        None
    """
    main_window.destroy()

def change_language():
    """
    選單路徑：說明 > 切換語言
    開啟切換語言視窗供使用者選擇語言。

    參數：
        None

    回傳:
        None

    Menu path: Help > Change Language
    Creates a new window for selecting the language.

    Parameters:
        None

    Returns:
        None
    """
    language_window = tk.Toplevel(main_window)
    language_window.title(_("語言選擇"))
    language_window.iconbitmap(ICON_FILE)
    language_window.geometry("250x100")
    language_window.resizable(0, 0)

    label_language = tk.Label(language_window, text=_("選擇語言："))
    label_language.pack()

    option_list = ["繁體中文", "English"]
    language_list = ["zh_TW", "en_US"]

    language_menu = ttk.Combobox(language_window, values=option_list)
    language_menu.pack()
    language_menu.current(language_list.index(config["SETTINGS"]["language"]))

    def save_language():
        config["SETTINGS"]["language"] = language_list[language_menu.current()]
        write_config(config)
        os.execl(sys.executable, sys.executable, *sys.argv)

    button_frame = tk.Frame(language_window)
    button_frame.pack(pady=10)
    button_save = tk.Button(button_frame, text=_("確認"), command=save_language)
    button_save.grid(column=0, row=0, padx=5)
    button_cancel = tk.Button(button_frame, text=_("取消"), command=language_window.destroy)
    button_cancel.grid(column=1, row=0, padx=5)

def open_repository():
    """
    選單路徑：說明 > GitHub Repository
    打開YT2file的GitHub Repository。

    參數：
        None

    回傳值:
        None

    Menu path: Help > GitHub Repository
    Opens the GitHub repository page for the YT2file project in the default web browser.

    Parameters:
        None

    Returns:
        None
    """
    webbrowser.open("https://github.com/BlueBoy247/YT2file")

def issue_report():
    """
    選單路徑：說明 > 問題回報
    打開問題回報之HTML文件。

    參數：
        None

    回傳值:
        None

    Menu path: Help > Report Issue
    Opens the issue report HTML file in the default web browser.

    Parameters:
        None

    Returns:
        None
    """
    webbrowser.open(f"Help\\{config['SETTINGS']['language']}\\report_issue.html")

def donate():
    """
    選單路徑：說明 > 贊助YT2file
    打開本專案的PayPal贊助頁面。

    參數：
        None

    回傳值:
        None

    Menu path: Help > Donate
    Opens the PayPal page for donation in the default web browser.

    Parameters:
        None

    Returns:
        None
    """
    webbrowser.open("https://paypal.me/blueboy2472779")

def info():
    """
    選單路徑：說明 > 關於
    顯示關於本程式的資訊訊息框。
    
    參數：
        None

    回傳值:
        None

    Menu path: Help > About
    Displays information about the program in a message box.

    Parameters:
        None

    Returns:
        None
    """
    messagebox.showinfo(
        _("程式資訊"),
        "YT2file\n\n"\
        f"{_('版本')}: {VERSION}\n"\
        f"{_('發佈時間')}: {RELEASE_DATE}\n\n"\
        "Copyright © 2024 AllenChang\nAll rights reserved."
    )

def check_update(show_message=True):
    """
    選單路徑：說明 > 檢查更新
    檢查更新。

    參數：
        show_message (bool): 
            是否在版本已經是最新時顯示訊息框。

    回傳值:
        None

    Menu path: Help > Check for Updates
    Checks for updates.

    Parameters:
        show_message (bool): 
            Whether to show a message box when the version is already up to date.

    Returns:
        None
    """
    def checking():
        new_version = requests.get(
            "https://api.github.com/repos/BlueBoy247/YT2file/releases/latest",
            timeout=5
        ).json()
        tag_name = new_version["tag_name"]
        published_at = new_version["published_at"]
        if tag_name > VERSION:
            update = messagebox.askyesno(
                _("更新"),
                f"{_('新版本已發佈，點擊「是」以更新至最新版本。')}\n\n"\
                f"{_('最新版本')}: {tag_name}\n"\
                f"{_('發佈時間')}: {published_at}"
            )
            if update:
                webbrowser.open("https://github.com/BlueBoy247/YT2file/releases/latest")
        elif show_message:
            messagebox.showinfo(_("更新"), _("已經是最新版本！"))

    threading.Thread(target=checking).start()

def show_progress_window():
    """
    顯示下載視窗。

    參數：
        None

    回傳值:
        progress_window (tk.Toplevel): 下載視窗

    Creates a progress window for displaying the download progress of a video.

    Parameters:
        None

    Returns:
        progress_window (tk.Toplevel): The progress window.
    """
    progress_window = tk.Toplevel(main_window)
    progress_window.title(_("下載中"))
    progress_window.iconbitmap(ICON_FILE)
    progress_window.geometry("300x100")
    progress_window.resizable(0, 0)
    progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

    canvas = tk.Canvas(progress_window, width=50, height=50)
    canvas.pack()

    arc = canvas.create_arc(
        (15, 15, 35, 35),
        start=0,
        extent=90,
        outline="blue",
        width=5,
        style="arc"
    )

    def animate_arc():
        while True:
            for i in range(18):
                if not canvas.winfo_exists():
                    return
                canvas.itemconfig(arc, start=(i * 20) % 360)
                canvas.update()
                canvas.after(75)

    threading.Thread(target=animate_arc).start()

    label_downloading = tk.Label(progress_window, text=_("影片下載中，請稍後..."))
    label_downloading.pack(fill="x")

    return progress_window

def click_download():
    """
    下載YouTube影片。

    參數：
        None

    回傳值:
        None

    Download a YouTube video.

    Parameters:
        None

    Returns:
        None
    """
    resolution = type_menu.get().split(", ")[0]

    if video_url.get() == "":
        messagebox.showwarning(_("警告"), _("網址欄尚未輸入!"))
        return
    pathdir = filedialog.askdirectory(title=_("選擇下載位置"), initialdir="download")
    if pathdir == "":
        return

    def download_video():
        progress_window = None
        try:
            yt = YouTube(video_url.get())
            if messagebox.askokcancel(_("確認下載資訊"), f"{_('下載YT影片名稱')}:\n{yt.title}\n\n{_('確定下載?')}"):
                progress_window = show_progress_window()

                name_temp = download_name.get() if download_name.get() else yt.title
                invalid_char = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
                file_name = "".join([" " if f in invalid_char else f for f in name_temp])

                if resolution in ["1080p", "2160p"]:
                    yt.streams.filter(
                        subtype="mp4",
                        res=resolution,
                        progressive=False
                    ).first().download(output_path=pathdir, filename=VIDEO_TEMP_FILE)
                    yt.streams.filter(
                        subtype="mp4",
                        type="audio",
                        progressive=False
                    ).last().download(output_path=pathdir, filename=AUDIO_TEMP_FILE)
                    mix(pathdir, file_name)
                elif resolution == "audio":
                    yt.streams.filter(
                        subtype="mp4",
                        type="audio",
                        progressive=False
                    ).last().download(output_path=pathdir, filename=f"{file_name}.mp3")
                else:
                    yt.streams.filter(
                        subtype="mp4",
                        res=resolution,
                        progressive=True
                    ).first().download(output_path=pathdir, filename=f"{file_name}.mp4")
            else:
                return
        except exceptions.AgeRestrictedError:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror(_("影片無法下載"), _("此影片有年齡限制，需要登入才能下載。\n（登入下載功能尚未實現）"))
        except exceptions.RegexMatchError:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror(_("找不到影片"), _("請確認網址是否正確、該影片是否存在，並重新試一次。"))
        except AttributeError:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror(_("找不到格式"), f"{_('您所選的類型')} ({resolution}) {_('不存在。')}")
        except Exception as e:
            if progress_window:
                progress_window.destroy()
            messagebox.showerror(_("下載失敗"), f"{_('錯誤訊息')}: {e}")
        else:
            if progress_window:
                progress_window.destroy()
            messagebox.showinfo(_("下載成功"), _("影片下載完成！"))
            os.startfile(pathdir)
    threading.Thread(target=download_video).start()

def mix(pathdir, file_name):
    """
    當解析度為 "1080p" 或 "2160p" 時，因pytube下載的影片檔無音訊，需以此將影片和音訊合併為一個檔案。

    參數：
        pathdir (str): 儲存暫存影片、音訊及合併完成之影片檔案的目標資料夾。
        file_name (str): 合併完成之影片檔案名稱。

    回傳值：
        None

    Merges the video and audio files when the resolution is "1080p" or "2160p".

    Parameters:
        pathdir (str): The directory path where the video and audio files are located.
        file_name (str): The name of the merged file.

    Returns:
        None
    """
    try:
        os.chdir(pathdir)
        video = VideoFileClip(VIDEO_TEMP_FILE)
        audio = AudioFileClip(AUDIO_TEMP_FILE)
        output = video.set_audio(audio)
        output.write_videofile(
            f"{file_name}.mp4",
            temp_audiofile="temp_audiofile.mp4",
            remove_temp=True,
        )
        os.remove(VIDEO_TEMP_FILE)
        os.remove(AUDIO_TEMP_FILE)
    except Exception as e:
        for temp_file in [VIDEO_TEMP_FILE, AUDIO_TEMP_FILE, "temp_audiofile.mp4"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        raise e

# 讀取配置檔 Read config
config = configparser.ConfigParser()
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)
else:
    config['SETTINGS'] = {"language": "zh_TW"}
    write_config(config)
lang_code = config["SETTINGS"]["language"]
lang = gettext.translation("messages", LOCALE_DIR, languages=[lang_code])
lang.install()
_ = lang.gettext

if not os.path.isdir("download"):
    os.makedirs("download")

# 創建主視窗 Create main window
main_window = tk.Tk()
main_window.geometry("430x250")
main_window.resizable(0, 0)
main_window.title("YT2file")
main_window["bg"] = "#e0ff2c"
if os.path.exists(ICON_FILE):
    main_window.iconbitmap(ICON_FILE)


# 檢查更新 Check for update
try:
    RELEASE_DATE = requests.get(
        f"https://api.github.com/repos/BlueBoy247/YT2file/releases/tags/{VERSION}",
        timeout=5
    ).json()["published_at"]
except requests.ConnectionError:
    if messagebox.showerror(_("連線失敗"), _("請檢查本裝置是否已連線至網路！")):
        main_window.destroy()
else:
    threading.Thread(target=lambda: check_update(show_message=False)).start()

# 主視窗輸入變數 Variables for main window
video_url = tk.StringVar()
download_name = tk.StringVar()

# 選單 Menu
menu = tk.Menu(main_window)

cascade_file = tk.Menu(menu, tearoff=0)
cascade_file.add_command(label=_("開啟下載資料夾"), command=open_directory)
cascade_file.add_separator()
cascade_file.add_command(label=_("結束"), command=exit_app)

cascade_option = tk.Menu(menu, tearoff=0)
cascade_option.add_command(label=_("切換語言"), command=change_language)
cascade_option.add_separator()
cascade_option.add_command(label=_("Github Repository"), command=open_repository)
cascade_option.add_separator()
cascade_option.add_command(label=_("問題回報"), command=issue_report)
cascade_option.add_command(label=_("贊助YT2file"), command=donate)
cascade_option.add_separator()
cascade_option.add_command(label=_("關於"), command=info)
cascade_option.add_command(label=_("檢查更新"), command=check_update)

menu.add_cascade(label=_("檔案"), menu=cascade_file)
menu.add_cascade(label=_("說明"), menu=cascade_option)
main_window.config(menu=menu)

# 網址列 URL entry
label_url = tk.Label(main_window, text=_("影片網址："), bg="#e0ff2c")
label_url.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

entry_url = tk.Entry(main_window, textvariable=video_url)
entry_url.config(width=45)
entry_url.grid(column=1, row=0, sticky=tk.W, padx=2, pady=10)

# 檔案名稱列 Filename entry
label_filename = tk.Label(main_window, text=_("檔案名稱："), bg="#e0ff2c")
label_filename.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

entry_filename = tk.Entry(main_window, textvariable=download_name)
entry_filename.config(width=45)
entry_filename.grid(column=1, row=1, sticky=tk.W, padx=2, pady=10)

# 類型選擇區 Type selection
label_type = tk.Label(main_window, text=_("類型選擇："), bg="#e0ff2c")
label_type.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

type_list = ["audio, mp3", "360p, mp4", "480p, mp4", "720p, mp4", "1080p, mp4", "2160p, mp4"]
type_menu = ttk.Combobox(main_window, values=type_list, width=42)
type_menu.set("720p, mp4")
type_menu.grid(column=1, row=2, sticky=tk.W, padx=2, pady=10)

# 注意事項 Notice
notice_content = tk.Message(
    main_window,
    text=_("1.務必確認該影片支援選取之類型。\n2.檔案名稱非必填，預設為原影片於YT之名稱。"),
    justify="left",
    width=310,
    anchor="w",
    fg="#ff0000",
    bg="#e0ff2c"
)
notice_content.grid(column=1, row=3, sticky=tk.W, padx=2, pady=10)

# 下載按鈕 Download button
download_button = tk.Button(main_window, text=_("下載"), command=click_download, width=15)
download_button.grid(column=0, row=4, columnspan=2)

main_window.mainloop()
