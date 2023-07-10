import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import threading
import time

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Locey Reminder")
        self.root.configure(bg='yellow')
        self.entries = []
        self.date_entries = []
        self.hour_entries = []
        self.minute_entries = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(5):
            tk.Label(self.root, text=f"Event {i+1}:", bg='yellow').grid(row=i, column=0)
            event_entry = tk.Entry(self.root)
            event_entry.grid(row=i, column=1)
            self.entries.append(event_entry)

            date_entry = DateEntry(self.root)
            date_entry.grid(row=i, column=2)
            self.date_entries.append(date_entry)

            hour_entry = tk.Entry(self.root, width=3)
            hour_entry.grid(row=i, column=3)
            self.hour_entries.append(hour_entry)

            minute_entry = tk.Entry(self.root, width=3)
            minute_entry.grid(row=i, column=4)
            self.minute_entries.append(minute_entry)

        submit_button = tk.Button(self.root, text="设置", command=self.set_reminders)
        submit_button.grid(row=6, columnspan=5)

    def set_reminders(self):
        for event_entry, date_entry, hour_entry, minute_entry in zip(self.entries, self.date_entries, self.hour_entries, self.minute_entries):
            event = event_entry.get()
            date = date_entry.get_date()
            hour = hour_entry.get()
            minute = minute_entry.get()
            if event and date and hour.isdigit() and minute.isdigit():
                date = datetime.datetime(date.year, date.month, date.day, int(hour), int(minute))
                threading.Thread(target=timer_event, args=(date.strftime("%Y-%m-%d %H:%M"), event)).start()
        self.root.destroy()

def timer_event(event_time, event_message):
    # 当前时间
    now_time = datetime.datetime.now()
    
    # 指定的时间
    future_time = datetime.datetime.strptime(event_time, "%Y-%m-%d %H:%M")
    
    # 计算时间差（秒）
    delta_seconds = (future_time - now_time).total_seconds()
    if delta_seconds <= 0:
        print("The specified time has passed.")
        return
    
    # 创建定时器
    timer = threading.Timer(delta_seconds, show_message, args=(event_message,))
    timer.start()

def show_message(event_message):
    # 创建窗口
    window = tk.Tk()
    window.title("Locey Reminder")
    window.configure(bg='yellow')
    
    # 创建消息标签
    message_label = tk.Label(window, text=event_message, font=("Arial", 20, 'bold'), fg="red", bg='yellow')
    message_label.pack()

    # 置顶窗口
    window.lift()
    window.attributes('-topmost', True)

    # 将窗口移动到屏幕中心
    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
    window.geometry("+%d+%d" % (int(x), int(y)))
    window.update_idletasks()

    # 震动窗口
    shake(window)

    # 主循环
    window.mainloop()

def shake(window):
    # 获取窗口当前位置
    x = window.winfo_x()
    y = window.winfo_y()

    # 震动的次数和距离
    shakes = 50
    distance = 10

    # 模拟震动
    for _ in range(shakes):
        for i in range(0, distance, 2):
            window.geometry("+%d+%d" % (x + i, y))
            window.update()
            time.sleep(0.01)
        for i in range(distance, -distance, -2):
            window.geometry("+%d+%d" % (x + i, y))
            window.update()
            time.sleep(0.01)
        for i in range(-distance, 0, 2):
            window.geometry("+%d+%d" % (x + i, y))
            window.update()
            time.sleep(0.01)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
