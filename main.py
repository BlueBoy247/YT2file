#功能匯入
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube, exceptions
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import threading

#事件處理
def info():
    messagebox.showinfo("程式資訊","YT2file\n\nAuthor: BlueBoy\nVersion: 1.1 (2024.05.19)")

def get_resolution():
    global resolution
    resolution = type_var.get()

def click_download():
    global resolution
    if url.get() == "":
        messagebox.showwarning("警告","網址欄尚未輸入!")
        return
    pathdir = filedialog.askdirectory(title="選擇下載位置",initialdir="download")
    if pathdir == "":
        return
    
    def show_progress_window():
        progress_window.deiconify()
        progress_window.lift(main_window)

    def download_video():
        try:
            yt = YouTube(url.get())
            dlcheck = tk.messagebox.askquestion("確認下載資訊",f"下載YT影片名稱:\n{yt.title}\n\n確定下載?")
            if dlcheck == "yes":
                threading.Thread(target=show_progress_window).start()

                name_temp = download_name.get() if download_name.get() else yt.title
                file_name = ''.join([' ' if f in ['\\', '/', ':', '*', '?', '"', '<', '>', '|'] else f for f in name_temp])
                
                if resolution in ["1080p", "2160p"]:
                    yt.streams.filter(subtype="mp4", res=resolution, progressive=False).first().download(output_path=pathdir, filename="video_temp.mp4")
                    yt.streams.filter(subtype="mp4", type="audio", progressive=False).last().download(output_path=pathdir, filename="audio_temp.mp4")
                    mix(pathdir,file_name)
                elif resolution == "music":
                    yt.streams.filter(subtype="mp4", type="audio", progressive=False).last().download(output_path=pathdir, filename=f"{file_name}.mp3")
                else:
                    yt.streams.filter(subtype="mp4", res=resolution, progressive=True).first().download(output_path=pathdir, filename=f"{file_name}.mp4")
            else:
                return
        except exceptions.AgeRestrictedError:
            messagebox.showerror("影片無法下載", "此影片有年齡限制，需要登入才能下載。\n（登入下載功能尚未實現）")
        except exceptions.RegexMatchError:
            messagebox.showerror("找不到影片", "請確認網址是否正確、該影片是否存在，並重新試一次")
        except AttributeError:
            messagebox.showerror("找不到格式", f"請確認選取之格式({resolution})是否存在，並重新試一次")
        except Exception as e:
            messagebox.showerror("下載失敗", f"錯誤訊息: {e}")
        else:
            os.startfile(pathdir)
            messagebox.showinfo("下載成功", "影片下載完成！")
        finally:
            if progress_window.winfo_exists():
                progress_window.withdraw()
    
    threading.Thread(target=download_video).start()

def mix(pathdir,file_name):
    try:
        os.chdir(pathdir)
        video = VideoFileClip("video_temp.mp4")
        audio = AudioFileClip("audio_temp.mp4")
        output = video.set_audio(audio)
        output.write_videofile(
            f"{file_name}.mp4",
            temp_audiofile="temp_audiofile.mp4",
            remove_temp=True,
        )
        os.remove("video_temp.mp4")
        os.remove("audio_temp.mp4")
    except Exception as e:
        for temp_file in ["video_temp.mp4", "audio_temp.mp4", "temp_audiofile.mp4"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        raise e

#創建下載資料夾
if not os.path.isdir("download"):
    os.makedirs("download")

#主視窗設定
main_window = tk.Tk()
main_window.geometry("430x250")
main_window.resizable(0, 0)
main_window.title("YT2file")
main_window.iconbitmap("icon.ico")
main_window["bg"] = "#e0ff2c"

#全域變數
resolution = "720p"
type_var = tk.StringVar()
url = tk.StringVar()
download_name = tk.StringVar()

#網址列
label_url = tk.Label(main_window, text="Youtube網址：", bg="#e0ff2c")
label_url.place(x=10, y=20)

entry_url = tk.Entry(main_window, textvariable=url)
entry_url.config(width=45)
entry_url.place(x=100, y=20)

#檔案名稱列
label_filename = tk.Label(main_window, text="檔案名稱：", bg="#e0ff2c")
label_filename.place(x=34, y=50)

entry_filename = tk.Entry(main_window, textvariable=download_name)
entry_filename.config(width=45)
entry_filename.place(x=100, y=50)

#下載按鈕
download_button = tk.Button(main_window, text="下載", command=click_download)
download_button.place(x=240,y=200)

#類型選擇區
label_type = tk.Label(main_window, text="類型選擇：", bg="#e0ff2c")
label_type.place(x=34,y=80)

type_music = tk.Radiobutton(main_window, text=("音訊, mp3"), variable=type_var, value="music", command=get_resolution, bg="#e0ff2c")
type_music.place(x=100,y=80)

type_360p = tk.Radiobutton(main_window, text=("360p, mp4"), variable=type_var, value="360p", command=get_resolution, bg="#e0ff2c")
type_360p.place(x=200,y=80)

type_480p = tk.Radiobutton(main_window, text=("480p, mp4"), variable=type_var, value="480p", command=get_resolution, bg="#e0ff2c")
type_480p.place(x=300,y=80)

type_720p = tk.Radiobutton(main_window, text=("720p, mp4"), variable=type_var, value="720p", command=get_resolution, bg="#e0ff2c")
type_720p.place(x=100,y=105)
type_720p.select()

type_1080p = tk.Radiobutton(main_window, text=("1080p, mp4"), variable=type_var, value="1080p", command=get_resolution, bg="#e0ff2c")
type_1080p.place(x=200,y=105)

type_2160p = tk.Radiobutton(main_window, text=("2160p, mp4"), variable=type_var, value="2160p", command=get_resolution, bg="#e0ff2c")
type_2160p.place(x=300,y=105)

#程式資訊
info_button = tk.Button(main_window, text="程式資訊", command=info)
info_button.place(x=150,y=200)

#注意事項
label_notice = tk.Label(main_window, text="注意事項：", fg="#ff0000", bg="#e0ff2c")
label_notice.place(x=34, y=135)

notice_content = tk.Message(
    main_window,
    text="1.務必確認該影片支援選取之類型。\n2.影片下載需時較長(尤其1080p與2160p)，請耐心等候！\n3.檔案名稱非必填，預設為原影片於YT之名稱。",
    justify="left",
    width=310,
    anchor="w",
    fg="#ff0000",
    bg="#e0ff2c"
)
notice_content.place(x=95, y=135)

# 下載中視窗
progress_window = tk.Toplevel(main_window)
progress_window.iconbitmap("icon.ico")
progress_window.geometry("300x100")
progress_window.resizable(0, 0)
progress_window.withdraw()
label_downloading = tk.Label(progress_window, text="影片下載中，請稍後...")
label_downloading.place(x=95, y=30)

main_window.mainloop()
