# -*- coding: utf-8 -*-
"""
 **********************************************************
 * Author        : tianshl
 * Email         : xiyuan91@126.com
 * Last modified : 2020-06-30 17:18:33
 * Filename      : wizard.py
 * Description   : XX精灵: 录制鼠标键盘操作, 回放录制的脚本
 * Document      : https://docs.python.org/zh-cn/3/library/tk.html#tkinter
                   https://pynput.readthedocs.io/en/latest
 * ********************************************************
"""
import json
import logging
import os
import threading
import time
from math import sqrt
from os import path
from tkinter import *
from tkinter import ttk, messagebox

from pynput import keyboard, mouse
from pynput.keyboard import KeyCode, Key


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger(__name__)


class Device:
    """
    外设
    """
    KEYBOARD = 'k'
    MOUSE = 'm'


class MouseOption:
    """
    鼠标 操作
    """
    MOVE = 'm'
    CLICK = 'c'
    SCROLL = 's'


class MouseButton:
    """
    鼠标 按键
    """
    LEFT = 'l'
    MIDDLE = 'm'
    RIGHT = 'r'


class Wizard(Frame):
    """
    XX精灵图形化界面
    """
    def __init__(self):
        Frame.__init__(self)

        # 当前所处文件夹
        self.cwd = path.abspath(path.dirname(__file__))
        # 记录 文件夹
        self.records_path = path.join(self.cwd, 'xx_records')
        if not path.exists(self.records_path):
            os.mkdir(self.records_path)

        # 录制 热键
        self.record_widget_hot_key = None
        self.record_hot_key = None
        # 录制 脚本名称
        self.record_widget_file_name = None
        self.record_file_name = None
        # 录制 是否记录鼠标轨迹
        self.record_widget_mouse_track = None
        self.record_mouse_track = True
        # 录制 鼠标轨迹记录最小间隔像素点, 单位: 像素
        self.record_widget_mouse_track_min_pix = None
        self.record_mouse_track_min_pix = 10
        # 录制 窗口隐藏
        self.record_widget_win_hide = None
        self.record_win_hide = True
        # 录制 录制中
        self.record_running = False
        # 录制 按钮
        self.record_button_value = StringVar(value='开始录制')
        # 录制 动作 时间戳
        self.record_timestamp = None
        # 录制 脚本 记录
        self.record_json = list()
        self.record_json_append = self.record_json.append
        # 录制 鼠标监听
        self.record_mouse_listener = None
        # 录制 键盘监听
        self.record_keyboard_listener = None
        # 录制 热键监听
        self.record_hot_key_listener = None
        # 录制 鼠标 坐标
        self.record_mouse_x = None
        self.record_mouse_y = None

        # 鼠标按键映射表
        self.MOUSE_STR2BUTTON = {
            MouseButton.LEFT: mouse.Button.left,
            MouseButton.MIDDLE: mouse.Button.middle,
            MouseButton.RIGHT: mouse.Button.right,
        }
        self.MOUSE_BUTTON2STR = {
            mouse.Button.left: MouseButton.LEFT,
            mouse.Button.middle: MouseButton.MIDDLE,
            mouse.Button.right: MouseButton.RIGHT
        }

        # 回放 热键
        self.playback_widget_hot_key = None
        self.playback_hot_key = None
        # 回放 脚本名称
        self.playback_widget_file_name = None
        self.playback_file_name = None
        # 回放 重复次数
        self.playback_widget_repeat_count = None
        self.playback_repeat_count = 0
        # 回放 每次回放间隔时间, 单位: 秒
        self.playback_widget_repeat_interval = None
        self.playback_repeat_interval = 10
        # 回放 窗口隐藏
        self.playback_widget_win_hide = None
        self.playback_win_hide = True
        # 回放 回放中
        self.playback_running = False
        # 回放 按钮
        self.playback_button_value = StringVar(value='开始回放')
        # 回放 热键监听
        self.playback_hot_key_listener = None

        # 设置基本信息
        self.render_base_info()
        # 录制窗口
        self.record_pane = None
        # 回放窗口
        self.playback_pane = None
        # 渲染窗口
        self.render_record_pane()
        self.render_playback_pane()
        # 当前窗口
        self.current_pane = 'playback'

        # 键盘控制器
        self.controller_keyboard = keyboard.Controller()
        # 鼠标控制器
        self.controller_mouse = mouse.Controller()

        # 启动热键监听
        self.hot_key_listener_thread()

        # 提示信息
        self.tool_tip = None

    def render_base_info(self):
        """
        基本信息
        """
        # 设置窗口标题
        self.master.title('XX精灵')
        # 获取屏幕分辨率
        win_w = self.winfo_screenwidth()
        win_h = self.winfo_screenheight()
        # 设置窗口尺寸/位置
        self.master.geometry('260x280+{}+{}'.format(win_w // 2 - 130, win_h // 2 - 140))
        # 设置窗口不可变
        self.master.resizable(width=False, height=False)

    def window_iconify(self):
        """
        窗口最小化
        """
        self.master.iconify()

    def window_deiconify(self):
        """
        窗口还原
        """
        self.master.deiconify()

    def render_record_pane(self):
        """
        渲染录制窗口
        """
        self.record_pane = Frame(self.master, width=260, height=280)
        self.record_pane.place(x=300, y=0)

        # 文件名称
        label_file_name = Label(self.record_pane, text='脚本名称', relief=RIDGE, padx=10)
        label_file_name.place(x=10, y=10)
        label_file_name.bind('<Enter>', lambda event: self.show_tip(event, self.record_pane, "本次录制存储的文件名, 重名覆盖"))
        label_file_name.bind('<Leave>', self.hide_tip)

        self.record_widget_file_name = Entry(self.record_pane, width=15)
        self.record_widget_file_name.insert(0, 'records_1.json')
        self.record_widget_file_name.place(x=90, y=8)

        # 鼠标轨迹
        label_mouse_track = Label(self.record_pane, text='鼠标轨迹', relief=RIDGE, padx=10)
        label_mouse_track.place(x=10, y=55)
        label_mouse_track.bind('<Enter>', lambda event: self.show_tip(event, self.record_pane, "是否记录鼠标轨迹"))
        label_mouse_track.bind('<Leave>', self.hide_tip)

        self.record_widget_mouse_track = BooleanVar(value=True)
        check_button_mouse_track = ttk.Checkbutton(
            self.record_pane, variable=self.record_widget_mouse_track,
            width=0, onvalue=True, offvalue=False
        )
        check_button_mouse_track.place(x=90, y=55)

        # 轨迹间隔
        label_mouse_track_interval = Label(self.record_pane, text='鼠标间隔', relief=RIDGE, padx=10)
        label_mouse_track_interval.place(x=10, y=100)
        label_mouse_track_interval.bind('<Enter>', lambda event: self.show_tip(
            event, self.record_pane,
            "开启轨迹后, 轨迹间隔超过x像素才会记录, 数值越小轨迹越平滑, 相应的记录文件体积也越大"
        ))
        label_mouse_track_interval.bind('<Leave>', self.hide_tip)

        self.record_widget_mouse_track_min_pix = Scale(
            self.record_pane, from_=0, to=50, orient=HORIZONTAL, sliderlength=10
        )
        self.record_widget_mouse_track_min_pix.set(self.record_mouse_track_min_pix)
        self.record_widget_mouse_track_min_pix.place(x=90, y=82)

        label_mouse_track_interval_suffix = Label(self.record_pane, text='(像素)')
        label_mouse_track_interval_suffix.place(x=190, y=100)

        # 录制热键
        label_record_stop = Label(self.record_pane, text='录制热键', relief=RIDGE, padx=10)
        label_record_stop.place(x=10, y=145)
        label_record_stop.bind('<Enter>', lambda event: self.show_tip(event, self.record_pane, "开始录制 | 停止录制, 默认'右Ctrl'"))
        label_record_stop.bind('<Leave>', self.hide_tip)

        self.record_widget_hot_key = ttk.Combobox(self.record_pane, width=13)
        self.record_widget_hot_key.bind('<<ComboboxSelected>>', self.record_hot_key_change)
        self.record_widget_hot_key.place(x=90, y=143)
        self.record_widget_hot_key['value'] = ['ctrl_r'] + ['f{}'.format(i) for i in range(1, 13)]
        self.record_widget_hot_key.current(0)

        # 窗口隐藏
        label_record_win_hide = Label(self.record_pane, text='窗口隐藏', relief=RIDGE, padx=10)
        label_record_win_hide.place(x=10, y=190)
        label_record_win_hide.bind('<Enter>', lambda event: self.show_tip(event, self.record_pane, "运行时自动隐藏窗口"))
        label_record_win_hide.bind('<Leave>', self.hide_tip)

        self.record_widget_win_hide = BooleanVar(value=True)
        check_button_win_hide = ttk.Checkbutton(
            self.record_pane, variable=self.record_widget_win_hide,
            width=0, onvalue=True, offvalue=False
        )
        check_button_win_hide.place(x=90, y=190)

        # 开始录制
        button_record_start = ttk.Button(
            self.record_pane, textvariable=self.record_button_value,
            width=21, command=self.record_status_change
        )
        button_record_start.place(x=10, y=235)

        # 右箭头
        canvas_arrow_right = Canvas(
            self.record_pane, width=20, height=280, bg='DarkGray', cursor='heart'
        )
        canvas_arrow_right.create_line(12, 100, 17, 140, fill='white')
        canvas_arrow_right.create_line(7, 100, 12, 140, fill='white')
        canvas_arrow_right.create_line(12, 140, 7, 180, fill='white')
        canvas_arrow_right.create_line(17, 140, 12, 180, fill='white')
        canvas_arrow_right.place(x=240, y=-3)
        canvas_arrow_right.bind('<ButtonRelease-1>', self.change_pane)

    def render_playback_pane(self):
        """
        渲染回放窗口
        """

        self.playback_pane = Frame(self.master, width=260, height=280)
        self.playback_pane.place(x=0, y=0)

        # 记录名称
        label_file_name = Label(self.playback_pane, text='脚本名称', relief=RIDGE, padx=10)
        label_file_name.place(x=30, y=10)
        label_file_name.bind('<Enter>', lambda event: self.show_tip(event, self.playback_pane, "要回放的脚本名称"))
        label_file_name.bind('<Leave>', self.hide_tip)

        self.playback_widget_file_name = ttk.Combobox(self.playback_pane, width=13)
        self.playback_widget_file_name.place(x=110, y=8)
        files = os.listdir(self.records_path)
        self.playback_widget_file_name['value'] = files
        if files:
            self.playback_widget_file_name.current(0)

        # 重复次数
        label_repeat_count = Label(self.playback_pane, text='重复次数', relief=RIDGE, padx=10)
        label_repeat_count.place(x=30, y=55)
        label_repeat_count.bind('<Enter>', lambda event: self.show_tip(event, self.playback_pane, "执行脚本的次数"))
        label_repeat_count.bind('<Leave>', self.hide_tip)

        self.playback_widget_repeat_count = Entry(self.playback_pane, width=11)
        self.playback_widget_repeat_count.insert(0, 0)
        self.playback_widget_repeat_count.place(x=110, y=52)

        label_repeat_count_suffix = Label(self.playback_pane, text='(次)')
        label_repeat_count_suffix.place(x=225, y=55)

        # 重复间隔
        label_repeat_interval = Label(self.playback_pane, text='重复间隔', relief=RIDGE, padx=10)
        label_repeat_interval.place(x=30, y=100)
        label_repeat_interval.bind('<Enter>', lambda event: self.show_tip(event, self.playback_pane, "执行完脚本延迟x秒后重复"))
        label_repeat_interval.bind('<Leave>', self.hide_tip)

        self.playback_widget_repeat_interval = Entry(self.playback_pane, width=11)
        self.playback_widget_repeat_interval.insert(0, 10)
        self.playback_widget_repeat_interval.place(x=110, y=97)

        label_repeat_interval_suffix = Label(self.playback_pane, text='(秒)')
        label_repeat_interval_suffix.place(x=225, y=100)

        # 回放热键
        label_playback_stop = Label(self.playback_pane, text='回放热键', relief=RIDGE, padx=10)
        label_playback_stop.place(x=30, y=145)
        label_playback_stop.bind('<Enter>', lambda event: self.show_tip(event, self.playback_pane, "开始回放 | 停止回放, 默认'右Ctrl'"))
        label_playback_stop.bind('<Leave>', self.hide_tip)

        self.playback_widget_hot_key = ttk.Combobox(self.playback_pane, width=13)
        self.playback_widget_hot_key.bind('<<ComboboxSelected>>', self.playback_hot_key_change)
        self.playback_widget_hot_key.place(x=110, y=143)
        self.playback_widget_hot_key['value'] = ['ctrl_r'] + ['f{}'.format(i) for i in range(1, 13)]
        self.playback_widget_hot_key.current(0)

        # 窗口隐藏
        label_playback_win_hide = Label(self.playback_pane, text='窗口隐藏', relief=RIDGE, padx=10)
        label_playback_win_hide.place(x=30, y=190)
        label_playback_win_hide.bind('<Enter>', lambda event: self.show_tip(event, self.playback_pane, "运行时自动隐藏窗口"))
        label_playback_win_hide.bind('<Leave>', self.hide_tip)

        self.playback_widget_win_hide = BooleanVar(value=True)
        check_button_playback_win_hide = ttk.Checkbutton(
            self.playback_pane, variable=self.playback_widget_win_hide,
            width=0, onvalue=True, offvalue=False
        )
        check_button_playback_win_hide.place(x=110, y=190)

        # 开始回放
        button_playback_start = ttk.Button(
            self.playback_pane, textvariable=self.playback_button_value,
            width=21, command=self.playback_status_change
        )
        button_playback_start.place(x=27, y=235)

        # 左箭头
        canvas_arrow_left = Canvas(
            self.playback_pane, width=20, height=280, bg='DarkGray', cursor='heart'
        )
        canvas_arrow_left.create_line(17, 100, 12, 140, fill='white')
        canvas_arrow_left.create_line(12, 100, 7, 140, fill='white')
        canvas_arrow_left.create_line(7, 140, 12, 180, fill='white')
        canvas_arrow_left.create_line(12, 140, 17, 180, fill='white')
        canvas_arrow_left.place(x=-3, y=-3)
        canvas_arrow_left.bind('<ButtonRelease-1>', self.change_pane)

    def show_tip(self, event, pane, message):
        """
        展示提示信息
        """
        if not message:
            return
        x = event.x_root - self.master.winfo_x()
        y = event.y_root - self.master.winfo_y() - 10

        self.tool_tip = Label(pane, text=message, fg='White', bg='Black', font=('', 10), wraplength=220, justify=LEFT)
        half = len(message) * 10 // 2
        x = x - half if x > half else 0
        self.tool_tip.place(x=x, y=y)

    def hide_tip(self, event):
        """
        隐藏提示信息
        """
        self.tool_tip.destroy()

    def record_hot_key_change(self, event):
        """
        录制 热键改变
        """
        self.record_hot_key = getattr(Key, self.record_widget_hot_key.get())

    def playback_hot_key_change(self, event):
        """
        回放 热键改变
        """
        self.playback_hot_key = getattr(Key, self.playback_widget_hot_key.get())

    def change_pane(self, event):
        """
        切换窗口
        """
        if self.record_running:
            log.info('录制, 正在录制, 禁止切换')
            return

        if self.playback_running:
            log.info('回放, 正在回放, 禁止切换')
            return

        if self.current_pane == 'record':
            self.current_pane = 'playback'
            self.master.title('XX精灵---回放')
            self.playback_pane.place(x=0, y=0)
            self.record_pane.place(x=300, y=0)
        else:
            self.current_pane = 'record'
            self.master.title('XX精灵---录制')
            self.record_pane.place(x=0, y=0)
            self.playback_pane.place(x=300, y=0)

    def init_run_config(self):
        """
        初始化 配置
        """
        self.record_hot_key = getattr(Key, self.record_widget_hot_key.get())
        self.playback_hot_key = getattr(Key, self.playback_widget_hot_key.get())
        if self.current_pane == 'record':
            # 获取配置
            self.record_file_name = self.record_widget_file_name.get()
            self.record_mouse_track = self.record_widget_mouse_track.get()
            self.record_mouse_track_min_pix = int(self.record_widget_mouse_track_min_pix.get())
            self.record_win_hide = self.record_widget_win_hide.get()

            log.info('录制, 配置: 热键: {}, 脚本名: {}, 鼠标轨迹: {}, 轨迹间隔: {}'.format(
                self.record_widget_hot_key.get(), self.record_file_name,
                self.record_mouse_track, self.record_mouse_track_min_pix
            ))
        elif self.current_pane == 'playback':
            # 获取配置
            self.playback_win_hide = self.playback_widget_win_hide.get()
            self.playback_file_name = self.playback_widget_file_name.get()
            try:
                self.playback_repeat_count = int(self.playback_widget_repeat_count.get())
            except Exception as e:
                log.error('重复次数有误, err: ', e)
                messagebox.showwarning('错误', '重复次数有误')
                self.playback_stop()
                return

            try:
                self.playback_repeat_interval = int(self.playback_widget_repeat_interval.get())
            except Exception as e:
                log.error('重复间隔有误, err: ', e)
                messagebox.showwarning('错误', '重复间隔有误')
                self.playback_stop()
                return

            log.info('回放, 配置: 热键: {}, 重复次数: {}, 重复间隔: {}'.format(
                self.playback_widget_hot_key.get(), self.playback_repeat_count, self.playback_repeat_interval
            ))

    def record_status_change(self):
        """
        录制状态更新
        """
        # 判断状态
        if self.playback_running:
            messagebox.showwarning('提示', '正在回放, 请稍后录制')
            return

        if self.record_running:
            self.recording_stop()
            return

        # 开始录制
        self.recording_start()

    def playback_status_change(self):
        """
        开始回放
        """
        # 判断状态
        if self.record_running:
            messagebox.showwarning('提示', '正在录制, 请稍后回放')
            return

        if self.playback_running:
            # 停止回放
            self.playback_stop()
            return

        # 开始回放
        self.playback_start()

    def record_keyboard_press(self, key):
        """
        键盘按下
        :param key: 按键
        """
        vk = False

        # 特殊按键
        if hasattr(key, 'value'):
            v = key.value.vk
            vk = True

        # 普通按键
        else:
            v = key.char

        self.record_append(Device.KEYBOARD, {
            'key': v,
            'vk': vk,
            'press': True
        })

    def record_keyboard_release(self, key):
        """
        键盘弹起
        :param key: 按键
        """
        vk = False
        # 特殊按键
        if hasattr(key, 'value'):
            v = key.value.vk
            vk = True

        # 普通按键
        else:
            v = key.char

        self.record_append(Device.KEYBOARD, {
            'key': v,
            'vk': vk,
            'press': False
        })

    def record_mouse_move(self, x, y):
        """
        鼠标移动
        :param x:   横坐标
        :param y:   纵坐标
        """
        if not self.record_mouse_track:
            return

        if not self.record_mouse_x:
            self.record_mouse_x = x

        if not self.record_mouse_y:
            self.record_mouse_y = y

        dx = x - self.record_mouse_x
        dy = y - self.record_mouse_y
        if abs(sqrt(dx ** 2 + dy ** 2)) < self.record_mouse_track_min_pix:
            return

        self.record_mouse_x = x
        self.record_mouse_y = y

        self.record_append(Device.MOUSE, {
            'op': MouseOption.MOVE,
            'x': x,
            'y': y
        })

    def record_mouse_click(self, x, y, button, pressed):
        """
        鼠标点击
        :param x:       横坐标
        :param y:       纵坐标
        :param button:  鼠标按键
        :param pressed: 鼠标按下
        """
        self.record_mouse_x = x
        self.record_mouse_y = y

        self.record_append(Device.MOUSE, {
            'op': MouseOption.CLICK,
            'button': self.MOUSE_BUTTON2STR[button],
            'x': x,
            'y': y,
            'press': pressed
        })

    def record_mouse_scroll(self, x, y, dx, dy):
        """
        鼠标滚动
        :param x:   横坐标
        :param y:   纵坐标
        :param dx:  横坐标增量
        :param dy:  纵坐标增量
        """
        self.record_mouse_x = x
        self.record_mouse_y = y

        self.record_append(Device.MOUSE, {
            'op': MouseOption.SCROLL,
            'dx': dx,
            'dy': dy
        })

    def record_append(self, _type, kwargs):
        """
        增加录制记录
        """

        timestamp = int(time.time() * 1000)
        delay = (timestamp - self.record_timestamp) / 1000
        self.record_timestamp = timestamp
        if delay < 0:
            delay = 0

        record = {
            'type': _type,
            'delay': delay,
        }

        record.update(kwargs)

        self.record_json_append(record)

    def recoding_keyboard(self):
        """
        监听键盘
        """
        with keyboard.Listener(
            on_press=self.record_keyboard_press,
            on_release=self.record_keyboard_release
        ) as self.record_keyboard_listener:
            self.record_keyboard_listener.join()

    def recoding_mouse(self):
        """
        监听鼠标
        """
        with mouse.Listener(
            on_move=self.record_mouse_move,
            on_click=self.record_mouse_click,
            on_scroll=self.record_mouse_scroll
        ) as self.record_mouse_listener:
            self.record_mouse_listener.join()

    def recording_start(self):
        """
        录制脚本
        """

        # 初始化配置
        self.init_run_config()

        # 更新状态
        self.record_running = True
        self.record_button_value.set('停止录制')

        self.record_timestamp = int(time.time() * 1000)

        # 清空记录列表
        self.record_json.clear()
        # 启动键盘监听
        log.info('录制, 启动键盘监听')
        threading.Thread(target=self.recoding_keyboard, daemon=True).start()
        # 启动鼠标监听
        log.info('录制, 启动鼠标监听')
        threading.Thread(target=self.recoding_mouse, daemon=True).start()

        # 最小化窗口
        if self.record_win_hide:
            self.window_iconify()

    def record_save(self):
        """
        存储录制记录
        """
        if not self.record_json:
            return

        # 去除脚本中的热键按下
        self.record_json.pop()

        if not self.record_file_name:
            self.record_file_name = 'records_{}'.format(self.record_timestamp)
        file_path = path.join(self.records_path, self.record_file_name)
        log.info('录制, 脚本名: {}, {}'.format(
            self.record_file_name, '文件已存在, 覆盖操作' if os.path.exists(file_path) else '文件不存在, 新建操作'
        ))
        with open(file_path, 'w+') as f:
            f.write(json.dumps(self.record_json))

        # 更新回放脚本名列表
        self.playback_widget_file_name['value'] = os.listdir(self.records_path)
        self.playback_widget_file_name.set(self.record_file_name)

    def recording_stop(self):
        """
        停止录制脚本
        """
        log.info('录制: 停止录制')
        # 停止键盘监听
        if self.record_keyboard_listener:
            self.record_keyboard_listener.stop()

        # 停止鼠标监听
        if self.record_mouse_listener:
            self.record_mouse_listener.stop()

        # 存储脚本
        self.record_save()

        # 更新状态
        self.record_running = False
        self.record_button_value.set('开始录制')

        # 恢复窗口
        self.window_deiconify()

    def playback_mouse_execute(self, option):
        """
        回放 鼠标动作
        """
        op = option.get('op')

        # 鼠标点击
        if MouseOption.CLICK == op:
            self.controller_mouse.position = (option.get('x'), option.get('y'))
            method = self.controller_mouse.press if option.get('press') else self.controller_mouse.release
            method(self.MOUSE_STR2BUTTON[option.get('button', 'l')])

        # 鼠标滚动
        elif MouseOption.SCROLL == op:
            self.controller_mouse.scroll(option.get('dx', 0), option.get('dy', 0))

        # 鼠标位移
        elif MouseOption.MOVE == op:
            self.controller_mouse.position = (option.get('x'), option.get('y'))

    def playback_keyboard_execute(self, option):
        """
        回放 键盘动作
        """
        key = option.get('key')
        press = option.get('press')
        if key is None or press is None:
            return

        vk = option.get('vk')
        if vk:
            key = KeyCode.from_vk(key)
        else:
            key = KeyCode.from_char(key)

        if press:
            self.controller_keyboard.press(key)
        else:
            self.controller_keyboard.release(key)

    def playback_execute(self):
        """
        执行回放
        """
        if not self.playback_file_name:
            messagebox.showwarning('提示', '未获取到要执行的记录')
            self.playback_stop()
            return

        file_path = path.join(self.records_path, self.playback_file_name)
        if not path.exists(file_path):
            messagebox.showwarning('提示', '未获取到要执行的记录')
            self.playback_stop()
            return

        with open(file_path, 'rb') as f:
            records = json.loads(f.read())

        if not records:
            messagebox.showwarning('提示', '未获取到要执行的记录')
            self.playback_stop()
            return

        repeat = 0
        while True:
            # < 0: 无限制重复
            if self.playback_repeat_count < 0 or repeat > self.playback_repeat_count:
                log.info('回放, 重复已达上限, 终止回放')
                self.playback_stop()
                break

            if repeat > 0:
                # 重复间隔时间
                log.info('回放, 等待{}秒后, 执行下一遍脚本'.format(self.playback_repeat_interval))
                time.sleep(self.playback_repeat_interval)

            if not self.playback_running:
                log.info('回放, 开关已关闭, 终止回放')
                break

            log.info('回放, 脚本执行开始')
            for record in records:
                if not self.playback_running:
                    log.info('回放, 开关已关闭, 终止回放')
                    break

                # 动作类型
                record_type = record.get('type', '')

                # 动作延时
                time.sleep(record.get('delay', 1))

                # 鼠标动作回放
                if Device.MOUSE == record_type:
                    self.playback_mouse_execute(record)
                # 键盘动作回放
                elif Device.KEYBOARD == record_type:
                    self.playback_keyboard_execute(record)

            log.info('回放, 脚本执行结束')

            # 重复次数 +1
            repeat += 1

    def playback_start(self):
        """
        执行回放
        """
        # 初始化配置
        self.init_run_config()

        self.playback_running = True
        self.playback_button_value.set('停止回放')

        # 执行回放
        threading.Thread(target=self.playback_execute, daemon=True).start()

        # 最小化窗口
        if self.playback_win_hide:
            self.window_iconify()

    def playback_stop(self):
        """
        停止回放
        """
        log.info('回放, 停止回放')
        # 更新状态
        self.playback_running = False
        self.playback_button_value.set('开始回放')

        # 恢复窗口
        self.window_deiconify()

    def hot_keyboard_press(self, key):
        """
        热键: 启停操作
        """
        # 录制
        if self.record_hot_key == key and self.current_pane == 'record':
            if self.record_running:
                self.recording_stop()
            else:
                self.recording_start()

        # 回放
        elif self.playback_hot_key == key and self.current_pane == 'playback':
            if self.playback_running:
                self.playback_stop()
            else:
                self.playback_start()

    def hot_key_listener(self):
        """
        热键监听
        """
        with keyboard.Listener(on_press=self.hot_keyboard_press) as keyboard_hot_key_listener:
            keyboard_hot_key_listener.join()

    def hot_key_listener_thread(self):
        """
        热键监听
        """
        # 初始化配置
        self.init_run_config()
        # 启动热键监听
        log.info('启动热键监听')
        threading.Thread(target=self.hot_key_listener, daemon=True).start()

    def run(self):
        """
        运行
        """
        self.mainloop()


if __name__ == '__main__':
    Wizard().run()
