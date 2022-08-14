from tkinter import *
from tkcalendar import *
import datetime

def getMyCal(hour=0,title_Text="default"):
    # ws = Tk()
    ws = Toplevel(ws)
    ws.title("New Window")
    ws.geometry("280x380")
    Label(ws, text ="This is a new window").pack()
    # ws.title(title_Text)
    # ws.geometry("280x380")
    ws.config(bg="#cd950c")

    hour_string=StringVar(value=hour)
    min_string=StringVar()
    return_Val=IntVar(value=0, name="Epoch")
    last_value_sec = ""
    last_value = ""        
    f = ('Times', 20)

    def display_msg():
        date = cal.get_date()
        m = min_sb.get()
        h = sec_hour.get()
        s = sec.get()

        datem = datetime.datetime.strptime(date,"%m/%d/%y")
        # print(datem.year)
        # print(datem.month)
        # print(datem.day)
        getEpoch = int(datetime.datetime(datem.year,datem.month,datem.day,int(m),int(h),int(s)).timestamp())
        ws.destroy()
        return_Val.set(getEpoch)
        return return_Val.get()
        
    if last_value == "59" and min_string.get() == "0":
        hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)   
        last_value = min_string.get()

    if last_value_sec == "59" and sec_hour.get() == "0":
        min_string.set(int(min_string.get())+1 if min_string.get() !="59" else 0)
    if last_value == "59":
        hour_string.set(int(hour_string.get())+1 if hour_string.get() !="23" else 0)            
        last_value_sec = sec_hour.get()

    fone = Frame(ws)
    ftwo = Frame(ws)

    fone.pack(pady=10)
    ftwo.pack(pady=10)

    cal = Calendar(
        fone, 
        selectmode="day", 
        year=datetime.date.today().year, 
        month=datetime.date.today().month,
        day=datetime.date.today().day
        )
    cal.pack()

    min_sb = Spinbox(
        ftwo,
        from_=0,
        to=23,
        wrap=True,
        textvariable=hour_string,
        width=2,
        state="readonly",
        font=f,
        justify=CENTER
        )
    sec_hour = Spinbox(
        ftwo,
        from_=0,
        to=59,
        wrap=True,
        textvariable=min_string,
        font=f,
        width=2,
        justify=CENTER
        )

    sec = Spinbox(
        ftwo,
        from_=0,
        to=59,
        wrap=True,
        textvariable=sec_hour,
        width=2,
        font=f,
        justify=CENTER
        )

    min_sb.pack(side=LEFT, fill=X, expand=True)
    sec_hour.pack(side=LEFT, fill=X, expand=True)
    sec.pack(side=LEFT, fill=X, expand=True)

    msg = Label(
        ws, 
        text="Hour  Minute  Seconds",
        font=("Times", 12),
        bg="#cd950c"
        )
    msg.pack(side=TOP)

    actionBtn =Button(
        ws,
        text=title_Text,
        padx=10,
        pady=10,
        command=display_msg
    )
    actionBtn.pack(pady=10)

    msg_display = Label(
        ws,
        text="",
        bg="#cd950c"
    )
    msg_display.pack(pady=10)

    ws.mainloop()
    # print(return_Val.get())
    return return_Val.get()

def getMyCalTest():
    print(getMyCal())

