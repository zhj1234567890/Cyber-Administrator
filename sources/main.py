import os
import time
from datetime import datetime
from threading import Thread
import subprocess
import random
import pystray
from PIL import Image, ImageDraw
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox


settings = {
    "shutdown_time": "23:59",
    "manage_sleep_time": "23:59",
    "manage_wake_time": "23:59",
    "noon_sleep_time": "23:59",
    "noon_wake_time": "23:59",
    "dingtalk_time": "23:59",
    "seewo_time": "23:59",
    "dingtalk_path": "D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
    "seewo_path": "C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
}


def create_image():
    color = ["black", "white", "pink", "green", "yellow", "blue"]
    width = 64
    height = 64
    color1 = random.choice(color)
    color2 = random.choice(color)
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    return image


def check_shutdown():
    while True:
        now = datetime.now()
        current_time = now.time()
        shutdown_time = datetime.strptime(settings['shutdown_time'], '%H:%M').time()

        if current_time >= shutdown_time:
            os.system('shutdown /s /t 1')
            break
        time.sleep(30)


def manage_sleep_wakeup():
    while True:
        now = datetime.now().time()
        sleep_time = datetime.strptime(settings['manage_sleep_time'], '%H:%M').time()
        wake_time = datetime.strptime(settings['manage_wake_time'], '%H:%M').time()
        if now >= sleep_time and now < wake_time:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        time.sleep(30)


def manage_sleep_wakeup_1():
    while True:
        now = datetime.now().time()
        sleep_time = datetime.strptime(settings['noon_sleep_time'], '%H:%M').time()
        wake_time = datetime.strptime(settings['noon_wake_time'], '%H:%M').time()
        if now >= sleep_time and now < wake_time:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        time.sleep(30)


def check_01():
    while True:
        now = datetime.now().time()
        open_time = datetime.strptime(settings['dingtalk_time'], '%H:%M').time()
        if now >= open_time:
            dingtalk_path = settings["dingtalk_path"]  # 动态获取路径
            subprocess.Popen(dingtalk_path)
            break
        time.sleep(30)

def check_02():
    while True:
        now = datetime.now().time()
        open_time = datetime.strptime(settings['seewo_time'], '%H:%M').time()
        if now >= open_time:
            seewo_path = settings["seewo_path"]  # 动态获取路径
            subprocess.Popen(seewo_path)
            break
        time.sleep(30)


def on_quit(icon):
    icon.stop()


# Tkinter GUI
def create_gui():
    def save_settings():
        # 更新设置值
        settings["shutdown_time"] = shutdown_var.get()
        settings["manage_sleep_time"] = manage_sleep_var.get()
        settings["manage_wake_time"] = manage_wake_var.get()
        settings["noon_sleep_time"] = noon_sleep_var.get()
        settings["noon_wake_time"] = noon_wake_var.get()
        settings["dingtalk_time"] = dingtalk_var.get()
        settings["seewo_time"] = seewo_var.get()
        settings["dingtalk_path"] = dingtalk_path_var.get()  # 保存Dingtalk路径
        settings["seewo_path"] = seewo_path_var.get()        # 保存Seewo路径
        messagebox.showinfo("Success", "Settings saved successfully!")

    root = Tk()
    root.title("System Settings")

    # 设置窗口大小
    root.geometry("330x440")

    # 创建输入字段及其标签
    Label(root, text="Shutdown Time:").grid(row=0, column=0, padx=10, pady=10)
    Label(root, text="Manage Sleep Time:").grid(row=1, column=0, padx=10, pady=10)
    Label(root, text="Manage Wake Time:").grid(row=2, column=0, padx=10, pady=10)
    Label(root, text="Noon Sleep Time:").grid(row=3, column=0, padx=10, pady=10)
    Label(root, text="Noon Wake Time:").grid(row=4, column=0, padx=10, pady=10)
    Label(root, text="DingTalk Start Time:").grid(row=5, column=0, padx=10, pady=10)
    Label(root, text="Seewo Start Time:").grid(row=6, column=0, padx=10, pady=10)
    Label(root, text="DingTalk Path:").grid(row=7, column=0, padx=10, pady=10)
    Label(root, text="Seewo Path:").grid(row=8, column=0, padx=10, pady=10)

    shutdown_var = StringVar(value=settings["shutdown_time"])
    manage_sleep_var = StringVar(value=settings["manage_sleep_time"])
    manage_wake_var = StringVar(value=settings["manage_wake_time"])
    noon_sleep_var = StringVar(value=settings["noon_sleep_time"])
    noon_wake_var = StringVar(value=settings["noon_wake_time"])
    dingtalk_var = StringVar(value=settings["dingtalk_time"])
    seewo_var = StringVar(value=settings["seewo_time"])
    dingtalk_path_var = StringVar(value=settings["dingtalk_path"])
    seewo_path_var = StringVar(value=settings["seewo_path"])

    Entry(root, textvariable=shutdown_var).grid(row=0, column=1, padx=10, pady=10)
    Entry(root, textvariable=manage_sleep_var).grid(row=1, column=1, padx=10, pady=10)
    Entry(root, textvariable=manage_wake_var).grid(row=2, column=1, padx=10, pady=10)
    Entry(root, textvariable=noon_sleep_var).grid(row=3, column=1, padx=10, pady=10)
    Entry(root, textvariable=noon_wake_var).grid(row=4, column=1, padx=10, pady=10)
    Entry(root, textvariable=dingtalk_var).grid(row=5, column=1, padx=10, pady=10)
    Entry(root, textvariable=seewo_var).grid(row=6, column=1, padx=10, pady=10)
    Entry(root, textvariable=dingtalk_path_var).grid(row=7, column=1, padx=10, pady=10)
    Entry(root, textvariable=seewo_path_var).grid(row=8, column=1, padx=10, pady=10)

    # 创建保存按钮
    Button(root, text="Save", command=save_settings).grid(row=9, column=0, columnspan=2, pady=10)

    root.mainloop()




def main():
    # 启动后台线程
    thread = Thread(target=check_shutdown)
    thread.daemon = True
    thread.start()

    thread1 = Thread(target=manage_sleep_wakeup)
    thread1.daemon = True
    thread1.start()

    thread2 = Thread(target=manage_sleep_wakeup_1)
    thread2.daemon = True
    thread2.start()

    thread3 = Thread(target=check_01)
    thread3.daemon = True
    thread3.start()

    thread4 = Thread(target=check_02)
    thread4.daemon = True
    thread4.start()

    # 设置系统托盘图标
    icon = pystray.Icon("Cyber Administrator")
    icon.icon = create_image()
    icon.title = "Cyber Administrator"
    icon.menu = pystray.Menu(pystray.MenuItem('Open Settings', lambda: create_gui()),
                             pystray.MenuItem('Quit', lambda: on_quit(icon)))

    # 运行托盘图标
    icon.run()


if __name__ == "__main__":
    main()
