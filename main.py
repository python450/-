import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

need_update = True

# 获取手机截图
def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screenimage.png')
    os.system('adb pull /sdcard/screenimage.png')
    return np.array(Image.open('screenimage.png'))

# 计算两点间的距离
def jump_to_next(start_point, end_point):
    x1, y1 = start_point
    x2, y2 = end_point

    # 使用勾股定理计算距离
    distance = ((x1 - x2) ** 2 + (y2 - y1) ** 2) ** 0.5

    # 进行点击
    os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distance * 1.35)))

# 鼠标点击事件
def on_click(event, coor=[]):
    global need_update
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())
    need_update = True

# 更新屏幕
def update_screen(frame):
    global need_update
    if need_update:
        time.sleep(1)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,

figure = plt.figure()
axes_image = plt.imshow(get_screen_image(), animated=True)
figure.canvas.mpl_connect('button_press_event', on_click)
animation = FuncAnimation(figure, update_screen, interval=50, blit=True)
plt.show()
