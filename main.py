#事件處理
def info():
    messagebox.showinfo("程式資訊","YT2file\n\nAuthor: BlueBoy\nVersion: 1.0 (2024.05.18)")

def rbVideo():
    global getvideo
    getvideo=videorb.get()

def clickDown():
    global getvideo,strftype,listradio
    if url.get()=="":
        messagebox.showwarning("警告","網址欄尚未輸入!")
        return
    pathdir=filedialog.askdirectory(title='選擇下載位置',initialdir='download')
    if pathdir=="":
        return
    success=False
    try:
        yt=YouTube(url.get())
        dlcheck=tk.messagebox.askquestion('確認下載資訊','下載YT影片名稱:\n'+yt.title+'\n\n確定下載?')
        if dlcheck=='yes':
            if DLname.get()=="":
                Tname=yt.title
            else:
                Tname=DLname.get()
            Fname=""
            for f in Tname:
                if f in ['\\','/',':','*','?','"','<','>','|']:
                    Fname+=" "
                else:
                    Fname+=f
            if getvideo=="1080p" or getvideo=="2160p":
                yt.streams.filter(subtype='mp4',res=getvideo,progressive=False).first().download(output_path=pathdir,filename='video.mp4')
                yt.streams.filter(subtype='mp4',type="audio",progressive=False).last().download(output_path=pathdir,filename='audio.mp4')
                success=True
                mix(pathdir,Fname)
            elif getvideo=="music":
                yt.streams.filter(subtype='mp4',type="audio",progressive=False).last().download(output_path=pathdir,filename=Fname+'.mp3')
            else:
                yt.streams.filter(subtype='mp4',res=getvideo,progressive=True).first().download(output_path=pathdir,filename=Fname+'.mp4')
        else:
            return
    except:
        if not success:
            time.sleep(1)
            messagebox.showerror("影片無法下載！","請確認網址是否正確、影片及選取之格式是否存在，或再重新試一次。")
        else:
            messagebox.showerror("輸出錯誤","影片影像與音訊無法整合")
    else:
        messagebox.showinfo("","下載完成！")
        os.startfile(pathdir)

def mix(pathdir,Fname):
    try:
        os.chdir(pathdir)
        vedio=VideoFileClip('video.mp4')
        audio=AudioFileClip('audio.mp4')
        output=vedio.set_audio(audio)
        output.write_videofile(Fname+'.mp4',temp_audiofile='temp_audio.mp4',remove_temp=True)
        os.remove('video.mp4')
        os.remove('audio.mp4')
    except:
        os.remove('video.mp4')
        os.remove('audio.mp4')
        os.remove('temp_audio.mp4')

#功能匯入
from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox
import os,time
from moviepy.editor import VideoFileClip, AudioFileClip
if not os.path.isdir('download'):
    os.makedirs('download')

#主視窗設定
mainw=tk.Tk()
mainw.geometry("430x250")
mainw.resizable(0,0)
mainw.title("YT2file")
mainw.iconbitmap('icon.ico')
mainw['bg']='#e0ff2c'
getvideo="720p"
videorb=tk.StringVar()
url=tk.StringVar()
DLname=tk.StringVar()

#網址列
labelUrl=tk.Label(mainw,text="Youtube網址： ",bg='#e0ff2c')
labelUrl.place(x=10,y=20)
entryUrl=tk.Entry(mainw,textvariable=url)
entryUrl.config(width=45)
entryUrl.place(x=100,y=20)

#檔案名稱列
labelName=tk.Label(mainw,text="檔案名稱： ",bg='#e0ff2c')
labelName.place(x=34,y=50)
entryName=tk.Entry(mainw,textvariable=DLname)
entryName.config(width=45)
entryName.place(x=100,y=50)

#下載按鈕
downloadbutton=tk.Button(mainw,text="下載",command=clickDown)
downloadbutton.place(x=240,y=200)

#品質選擇
labelQ=tk.Label(mainw,text="類型選擇： ",bg='#e0ff2c')
labelQ.place(x=34,y=80)
rbmusic=tk.Radiobutton(mainw,text=('音訊, mp3'),variable=videorb,value='music',command=rbVideo,bg='#e0ff2c')
rbmusic.place(x=100,y=80)
rb360=tk.Radiobutton(mainw,text=('360p, mp4'),variable=videorb,value='360p',command=rbVideo,bg='#e0ff2c')
rb360.place(x=200,y=80)
rb480=tk.Radiobutton(mainw,text=('480p, mp4'),variable=videorb,value='480p',command=rbVideo,bg='#e0ff2c')
rb480.place(x=300,y=80)
rb720=tk.Radiobutton(mainw,text=('720p, mp4'),variable=videorb,value='720p',command=rbVideo,bg='#e0ff2c')
rb720.place(x=100,y=105)
rb720.select()
rb1080=tk.Radiobutton(mainw,text=('1080p, mp4'),variable=videorb,value='1080p',command=rbVideo,bg='#e0ff2c')
rb1080.place(x=200,y=105)
rb2160=tk.Radiobutton(mainw,text=('2160p, mp4'),variable=videorb,value='2160p',command=rbVideo,bg='#e0ff2c')
rb2160.place(x=300,y=105)

#程式資訊
infobutton=tk.Button(mainw,text="程式資訊",command=info)
infobutton.place(x=150,y=200)

#注意事項
labelYT=tk.Label(mainw,text="注意事項： ",fg='#ff0000',bg='#e0ff2c')
labelYT.place(x=34,y=135)
labelYTName=tk.Message(mainw,text="1.務必確認該影片支援選取之畫質。\n2.影片下載需時較長(尤其1080p與2160p)，請耐心等候！\n3.檔案名稱非必填，預設為原影片於YT之名稱。",justify='left',width=310,anchor='w',fg='#ff0000',bg='#e0ff2c')
labelYTName.place(x=95,y=135)

mainw.mainloop()
