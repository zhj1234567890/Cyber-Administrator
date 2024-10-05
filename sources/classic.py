import os
import time
from datetime import datetime
import pystray
from PIL import Image, ImageDraw
from threading import Thread
import subprocess
import random


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
        current_day = now.weekday()  # 获取今天星期

        if current_day == 3:
            shutdown_time = datetime.strptime('16:35', '%H:%M').time()
        else:
            shutdown_time = datetime.strptime('17:05', '%H:%M').time()

        if current_time >= shutdown_time:
            os.system('shutdown /s /t 1')
            break
        time.sleep(30)  # 每分钟检查一次


def manage_sleep_wakeup():
    while True:
        now = datetime.now().time()
        sleep_time = datetime.strptime('10:30', '%H:%M').time()
        wake_time = datetime.strptime('10:50', '%H:%M').time()
        if now >= sleep_time and now < wake_time:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        time.sleep(30)


def noon_sleep_wakeup():
    while True:
        now = datetime.now().time()
        sleep_time = datetime.strptime('12:30', '%H:%M').time()
        wake_time = datetime.strptime('13:20', '%H:%M').time()
        if now >= sleep_time and now < wake_time:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        time.sleep(30)


def check_dingtalk():
    while True:
        now = datetime.now()
        current_time = now.time()
        current_day = now.weekday()

        open_time = datetime.strptime('23:59', '%H:%M').time()  # 默认时间
        if current_day == 0:
            open_time = datetime.strptime('07:55', '%H:%M').time()
        elif current_day == 1:
            open_time = datetime.strptime('10:50', '%H:%M').time()
        elif current_day == 2:
            open_time = datetime.strptime('14:15', '%H:%M').time()
        elif current_day == 3:
            open_time = datetime.strptime('07:55', '%H:%M').time()
        elif current_day == 4:
            open_time = datetime.strptime('09:40', '%H:%M').time()

        if current_time >= open_time:
            dingtalk_path = r"D:\Program Files (x86)\DingDing\DingtalkLauncher.exe"
            subprocess.Popen(dingtalk_path)
            break
        time.sleep(30)


def check_seewo():
    while True:
        now = datetime.now()
        current_time = now.time()
        current_day = now.weekday()

        open_time = datetime.strptime('23:59', '%H:%M').time()  # 默认时间
        if current_day == 0:
            open_time = datetime.strptime('09:40', '%H:%M').time()
        elif current_day == 1:
            open_time = datetime.strptime('08:45', '%H:%M').time()
        elif current_day == 2:
            open_time = datetime.strptime('07:55', '%H:%M').time()
        elif current_day == 3:
            open_time = datetime.strptime('11:40', '%H:%M').time()
        elif current_day == 4:
            open_time = datetime.strptime('07:55', '%H:%M').time()

        if current_time >= open_time:
            seewo_path = r"C:\Program Files(x86)\\Seewo\EasiNote5\swenlauncher\swenlauncher.exe"
            subprocess.Popen(seewo_path)
            break
        time.sleep(30)


def on_quit(icon):
    icon.stop()


def main():
    icon = pystray.Icon("Cyber Administrator")
    icon.icon = create_image()
    icon.title = "Cyber Administrator"
    icon.menu = pystray.Menu(pystray.MenuItem('Quit', lambda: on_quit(icon)))

    # 启动检查线程
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

    # 显示托盘图标
    icon.run()


if __name__ == "__main__":
    main()
