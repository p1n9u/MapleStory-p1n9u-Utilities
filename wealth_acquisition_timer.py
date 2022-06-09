"""
타이머 없는거 화딱지 나서 만듦
귀찮아서 변수같은거 대부분 전역변수로 때려박음
갖다 쓸거면 대충짠거니 알아서 읽고 수정
"""

# Library
from tkinter import *
import time
import winsound
import os

# functions

# If not build error occur by PATH
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Live Time
def clock():
    live_T = time.strftime("%H:%M:%S")
    clock_width.config(text=live_T)
    clock_width.after(980, clock)

# Start Button Command
def start():
    global running, st, cnt
    running = True
    cnt = 0
    st = time.time()
    waTimer()

# Reset Button Command
def reset():
    global running
    running = False
    time_txt.config(text="Press Start")
    wcnt_txt.config(text="연속재획시 [2시간] 을 체크해야 카운팅이 됩니다.")        

# Timer
def waTimer():
    global st, val0, val1, val2, val3, val4, val5, val6, cnt
    if (running):
        et = int(time.time() - st) # elapsed time

        # each variable match to checkbox
        if val0.get(): #2h
            if (et%7200 == 0) and (et!=0):
                winsound.PlaySound(resource_path("lithharbor.wav"), winsound.SND_ASYNC)
                cnt += 1
        if val1.get(): #1h
            if (et%3600 == 0) and (et!=0):
                winsound.PlaySound(resource_path("orbis.wav"), winsound.SND_ASYNC)
        if val2.get(): #30m
            if (et%1800 == 0) and (et!=0):
                winsound.PlaySound(resource_path("starbubble.wav"), winsound.SND_ASYNC)
        if val3.get(): #20m
            if (et%1200 == 0) and (et!=0):
                winsound.PlaySound(resource_path("ludibrium.wav"), winsound.SND_ASYNC)
        if val4.get(): #15m
            if (et%900 == 0) and (et!=0):
               winsound.PlaySound(resource_path("spotlight.wav"), winsound.SND_ASYNC)
        if val5.get(): #10m
            if (et%600 == 0) and (et!=0):
                winsound.PlaySound(resource_path("ellinia.wav"), winsound.SND_ASYNC)
        if val6.get(): #100s
            if (et%100 == 0) and (et!=0):
                winsound.PlaySound(resource_path("henesys.wav"), winsound.SND_ASYNC)

        # et variable : second -> conver to day, hour, minute, second
        m, s = divmod(et, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        if d > 0:
            dtime = str(d) + "일 "
        else: 
            dtime = ""
        if h > 0:
            htime = str(h) + "시간 "
        else:
            htime = ""
        if m > 0:
            mtime = str(m) + "분 "
        else:
            mtime = ""
               
        # elapsed time and wealth acquistion count
        strTime = "[경과시간] : " + dtime + htime + mtime + str(s) + "초"
        strCnt = "[재획횟수] : " + str(cnt)
        time_txt.config(text=strTime)
        wcnt_txt.config(text=strCnt)
        time_txt.after(980, waTimer)

# Settings and Init
root = Tk()
root.title("니가선택한재획이다악으로깡으로넷플봐라")
root.geometry("480x540+220+220")
root.resizable(False, False)
running = False
st = time.time()
cnt = 0
root.iconbitmap(resource_path("potion.ico"))

# first line
line_lbl4 = Label(root)
line_lbl4.pack(fill="both")
line4 = Label(line_lbl4, text="-----------------------------------------------------------------------------------------------")
line4.pack(side="left")

# introduction
glbl0 = Label(root, text="제작자 : 서버-유니온, 길드-풍아, 닉네임-p1n9u, 어뜨케 직업이 12움?")
glbl0.pack()
glbl1 = Label(root, text="이 프로그램은 상업용이 아닙니다. 버그픽스안합니다.")
glbl1.pack()
glbl2 = Label(root, text="< 메소회수는 5초, 이외 10초 동안 알림 >")
glbl2.pack()

# second line
line_lbl0 = Label(root)
line_lbl0.pack(fill="both")
line0 = Label(line_lbl0, text="-----------------------------------------------------------------------------------------------")
line0.pack(side="left")

# live time
clock_lbl = Label(root)
clock_lbl.pack(fill="both")

ctxt_width=Label(clock_lbl, text="Live Time : ")
ctxt_width.pack(side="left")

clock_width = Label(clock_lbl)
clock_width.pack(side="left")
clock()

# third line
line_lbl1 = Label(root)
line_lbl1.pack(fill="both")
line1 = Label(line_lbl1, text="-----------------------------------------------------------------------------------------------")
line1.pack(side="left")

# check box
val0 = IntVar()
val1 = IntVar()
val2 = IntVar()
val3 = IntVar()
val4 = IntVar()
val5 = IntVar()
val6 = IntVar()

c0_lbl = Label(root)
c1_lbl = Label(root)
c2_lbl = Label(root)
c3_lbl = Label(root)
c4_lbl = Label(root)
c5_lbl = Label(root)
c6_lbl = Label(root)

c0_lbl.pack(fill="both")
c1_lbl.pack(fill="both")
c2_lbl.pack(fill="both")
c3_lbl.pack(fill="both")
c4_lbl.pack(fill="both")
c5_lbl.pack(fill="both")
c6_lbl.pack(fill="both")

c0 = Checkbutton(c0_lbl, text="[2시간]-리스항구 : 재획비/경축비", variable=val0)
c1 = Checkbutton(c1_lbl, text="[1시간]-오르비스 : 경험치쿠폰", variable=val1)
c2 = Checkbutton(c2_lbl, text="[30분]-스타버블 : 경쿠/경뿌/유니온쿠폰/길축/우뿌/이벤벞/작경축/익스골드", variable=val2)
c3 = Checkbutton(c3_lbl, text="[20분]-루디브리엄 : 유니온쿠폰/이유식", variable=val3)
c4 = Checkbutton(c4_lbl, text="[15분]-스포트라이트 : 경험치쿠폰/붕뿌", variable=val4)
c5 = Checkbutton(c5_lbl, text="[10분]-엘리니아 : 유니온쿠폰", variable=val5)
c6 = Checkbutton(c6_lbl, text="[100초]-헤네시스 : 메소회수", variable=val6)

c0.pack(side="left")
c1.pack(side="left")
c2.pack(side="left")
c3.pack(side="left")
c4.pack(side="left")
c5.pack(side="left")
c6.pack(side="left")

# fourth line
line_lbl2 = Label(root)
line_lbl2.pack(fill="both")
line2 = Label(line_lbl2, text="-----------------------------------------------------------------------------------------------")
line2.pack(side="left")

# checklist for preparing wealth acquisition
clist_lbl = Label(root)
clist_lbl.pack(fill="both")
clist_txt = Label(clist_lbl, text="[체크리스트] : 링크, 유니온배치, 정펜, 혈반, 농장, 쓸심, 하이퍼")
clist_txt.pack(side="left")

# fifth line
line_lbl3 = Label(root)
line_lbl3.pack(fill="both")
line3 = Label(line_lbl3, text="-----------------------------------------------------------------------------------------------")
line3.pack(side="left")

# start and reset button
btn_lbl = Label(root)
btn_lbl.pack(fill="both")
btn_s = Button(btn_lbl, text="Start", command=start)
btn_s.pack(side="left")
btn_r = Button(btn_lbl, text="Reset", command=reset)
btn_r.pack(side="right")

timer_lbl = Label(root)
timer_lbl.pack(fill="both")

time_txt = Label(timer_lbl, text="Press Start")
time_txt.pack(side="left")


wcnt_lbl = Label(root)
wcnt_lbl.pack(fill="both")
wcnt_txt = Label(wcnt_lbl, text="연속재획시 [2시간] 을 체크해야 카운팅이 됩니다.")
wcnt_txt.pack(side="left")

# sixth line
line_lbl5 = Label(root)
line_lbl5.pack(fill="both")
line5 = Label(line_lbl5, text="-----------------------------------------------------------------------------------------------")
line5.pack(side="left")

root.mainloop()
