import os
import time
from datetime import datetime
from threading import Thread
import subprocess
import random
import pystray
from PIL import Image, ImageDraw
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
import winreg as reg  # 操作注册表
import logging  # 日志
from plyer import notification

# 初始化
now = datetime.now()
curr_time = now.time()
curr_day = now.weekday()

settings = {
    "shutdown_time": "23:59",
    "manage_sleep_time": "23:59",
    "manage_wake_time": "23:59",
    "noon_sleep_time": "23:59",
    "noon_wake_time": "23:59",
    "dingtalk_time": "23:59",
    "seewo_time": "23:59",
    "dingtalk_path": r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
    "seewo_path": r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
}

if curr_day == 0:
    settings = {
        "shutdown_time": "17:00",
        "manage_sleep_time": "10:30",
        "manage_wake_time": "10:50",
        "noon_sleep_time": "12:31",
        "noon_wake_time": "13:20",
        "dingtalk_time": "07:57",
        "seewo_time": "09:42",
        "dingtalk_path": r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
        "seewo_path": r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
    }

elif curr_day == 1:
    settings = {
        "shutdown_time": "17:00",
        "manage_sleep_time": "10:30",
        "manage_wake_time": "10:50",
        "noon_sleep_time": "12:30",
        "noon_wake_time": "13:20",
        "dingtalk_time": "10:52",
        "seewo_time": "08:47",
        "dingtalk_path": r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
        "seewo_path": r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
    }

elif curr_day == 2:
    settings = {
        "shutdown_time": "17:00",
        "manage_sleep_time": "10:30",
        "manage_wake_time": "10:50",
        "noon_sleep_time": "12:30",
        "noon_wake_time": "13:20",
        "dingtalk_time": "14:17",
        "seewo_time": "07:57",
        "dingtalk_path": r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
        "seewo_path": r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
    }

elif curr_day == 3:
    settings = {
        "shutdown_time": "16:30",
        "manage_sleep_time": "10:30",
        "manage_wake_time": "10:50",
        "noon_sleep_time": "12:30",
        "noon_wake_time": "13:20",
        "dingtalk_time": "07:57",
        "seewo_time": "11:42",
        "dingtalk_path": r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
        "seewo_path": r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
    }

elif curr_day == 4:
    settings = {
        "shutdown_time": "17:00",
        "manage_sleep_time": "10:30",
        "manage_wake_time": "10:50",
        "noon_sleep_time": "12:25",
        "noon_wake_time": "13:20",
        "dingtalk_time": "09:42",
        "seewo_time": "07:57",
        "dingtalk_path": r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe",
        "seewo_path": r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
    }

LOG_FILE = "cyber_admin.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,  # 日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 日志记录函数
def log_message(message, level=logging.INFO):
    logging.log(level, message)
    print(message)  # 在控制台输出日志信息，方便调试

# 课程表
schedule = [
    {"time": "09:00", "course": "语文"},
    {"time": "10:58", "course": "数学"},
    {"time": "11:40", "course": "英语"},
]


# 上课通知函数
def notify(course):
    if course == "数学":
        notification.notify(
            title='上课提醒',
            message=f'现在该上{course}课了',
            timeout=10
        )
        time.sleep(11)
        notification.notify(
            title='Warning',
            message=f'僵王博士即将抵达，可能存在生化武器威胁',
            timeout=10
        )
    else:
        notification.notify(
            title='上课提醒',
            message=f'现在该上{course}课了',
            timeout=10
        )


# 定时检查并提醒上课时间
def course_notification():
    while True:
        current_time = time.strftime("%H:%M")  # 获取当前时间
        for entry in schedule:
            if entry["time"] == current_time:
                log_message(f"上课通知：现在该上{entry['course']}课了", level=logging.INFO)
                notify(entry["course"])  # 如果当前时间等于课程时间，提醒
                break
        time.sleep(10)


# 日志记录函数
def log_message(message, level=logging.INFO):
    logging.log(level, message)
    print(message)


# 注册表检查函数
def check_startup_permission():
    app_name = "Cyber Administrator"  # 程序的名称
    exe_path = os.path.abspath(__file__)  # 获取当前脚本的绝对路径
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"  # 注册表键路径

    try:
        # 打开注册表的运行项
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ)
        try:
            # 尝试读取该键值
            reg_query = reg.QueryValueEx(reg_key, app_name)
            log_message(f"已存在开机启动项：{reg_query[0]}", level=logging.INFO)
        except FileNotFoundError:
            # 如果没有找到该项，则创建它
            log_message("未发现开机启动项，正在添加...", level=logging.WARNING)
            reg.CloseKey(reg_key)  # 关闭键，准备写入
            reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
            reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, exe_path)
            reg.CloseKey(reg_key)
            log_message(f"已成功添加开机启动项：{exe_path}", level=logging.INFO)
    except Exception as e:
        log_message(f"无法访问注册表：{e}", level=logging.ERROR)


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


def noon_sleep_wakeup():
    while True:
        now = datetime.now().time()
        sleep_time = datetime.strptime(settings['noon_sleep_time'], '%H:%M').time()
        wake_time = datetime.strptime(settings['noon_wake_time'], '%H:%M').time()
        if now >= sleep_time and now < wake_time:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            break
        time.sleep(30)


def check_dingtalk():
    while True:
        now = datetime.now().time()
        open_time = datetime.strptime(settings['dingtalk_time'], '%H:%M').time()
        if now >= open_time:
            dingtalk_path = r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe"
            subprocess.Popen(dingtalk_path)
            break
        time.sleep(30)


def check_seewo():
    while True:
        now = datetime.now().time()
        open_time = datetime.strptime(settings['seewo_time'], '%H:%M').time()
        if now >= open_time:
            seewo_path = r"C:\Program Files(x86)\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
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
        settings["dingtalk_path"] = dingtalk_path_var.get()
        settings["seewo_path"] = seewo_path_var.get()
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
    check_startup_permission()

    # 启动后台线程
    thread = Thread(target=check_shutdown)
    thread.daemon = True
    thread.start()

    thread1 = Thread(target=manage_sleep_wakeup)
    thread1.daemon = True
    thread1.start()

    thread2 = Thread(target=noon_sleep_wakeup)
    thread2.daemon = True
    thread2.start()

    thread3 = Thread(target=check_dingtalk)
    thread3.daemon = True
    thread3.start()

    thread4 = Thread(target=check_seewo)
    thread4.daemon = True
    thread4.start()

    thread5 = Thread(target=course_notification)
    thread5.daemon = True
    thread5.start()

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
