import os
import time
from datetime import datetime
import pystray
from PIL import Image, ImageDraw
from threading import Thread

def create_image():
    # 创建托盘图标的图像
    width = 64
    height = 64
    color1 = "black"
    color2 = "white"

    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)

    return image

def check_shutdown():
    while True:
        now = datetime.now().time()
        shutdown_time = datetime.strptime('17:05', '%H:%M').time()
        if now >= shutdown_time:
            os.system('shutdown /s /t 1')
            break
        time.sleep(60)  # 每60秒检查一次时间

def on_quit(icon):
    icon.stop()

def main():
    # 创建托盘图标
    icon = pystray.Icon("Shutdown Timer")
    icon.icon = create_image()
    icon.title = "Shutdown Timer"
    icon.menu = pystray.Menu(
        pystray.MenuItem('Quit', lambda: on_quit(icon))
    )

    # 启动检查关机时间的线程
    thread = Thread(target=check_shutdown)
    thread.daemon = True
    thread.start()

    # 运行托盘图标
    icon.run()

if __name__ == "__main__":
    main()
