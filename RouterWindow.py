import asyncio
import os
import sys
from tkinter import messagebox
import PySimpleGUI as sg
from psgtray import SystemTray
import BiliBiliLiveConnect
from bilibili_api import live
import DMSimulate

thisdir = os.path.dirname(os.path.realpath(__file__))

#如果是打包的程序
if getattr(sys, 'frozen', False):
    # 打包程序
    print('打包程序')
    thisdir = os.path.dirname(sys.executable)

iconpath = thisdir+'/icon.ico'
print('iconpath:',iconpath)
#判断文件是否存在
if not os.path.exists(iconpath):
    iconpath = None
    messagebox.showerror('错误','找不到icon.ico')


async def runWindow(exitCallback, port, router, logFunc):

    windowConfig = sg.user_settings_get_entry('windowConfig', default={})

    menu = ['', ['显示窗口', '隐藏窗口',  '---',  '退出']]
    title = f'弹幕路由服务器(端口:{port})'
    layout = [
        [sg.Text('未连接直播间', key='-RoomInfo-')],
        #输入框 模拟弹幕内容：_____
        [sg.Text('模拟弹幕内容：'),sg.InputText(key='-DanmuContent-', default_text=windowConfig.get('-DanmuContent-','j'))],
        #输入框 模拟弹幕ID：_____
        [sg.Text('模拟弹幕ID：'),sg.InputText(key='-DanmuID-', default_text=windowConfig.get('-DanmuID-','553256'))],
        #输入框 模拟弹幕发送者：_____
        [sg.Text('模拟弹幕发送者：'),sg.InputText(key='-DanmuSender-', default_text=windowConfig.get('-DanmuSender-','老王'))],
        #按钮 发送模拟弹幕
        [sg.Button('发送模拟弹幕',key='-SendDanmu-')],
        #输入框 直播间ID：_____
        [sg.Text('直播间ID：'),sg.InputText(key='-RoomID-', default_text=windowConfig.get('-RoomID-','26705605'))],
        #按钮 连接直播间
        [sg.Button('连接直播间',key='-ConnectRoom-'),sg.Button('断开连接',key='-DisconnectRoom-', visible=False)],
        #是否调试
        [sg.Checkbox('调试',key='-Debug-', default=windowConfig.get('-Debug-',False))],
        [sg.B("隐藏"),sg.B("退出")]
    ]

    window = sg.Window(title, layout, finalize=True, enable_close_attempted_event=True,icon=iconpath,element_justification='c')
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=title,icon=iconpath)
    # window.hide()
    values = None
    danmuTask = None
    while True:
        await asyncio.sleep(0.01)

        room:live.LiveDanmaku = BiliBiliLiveConnect.room
        if not room is None:
            status = room.get_status()
            if status == live.LiveDanmaku.STATUS_INIT:
                window['-RoomInfo-'].update('正在初始化连接')
            elif status == live.LiveDanmaku.STATUS_CONNECTING:
                window['-RoomInfo-'].update('正在连接直播间')
            elif status == live.LiveDanmaku.STATUS_ESTABLISHED:
                window['-RoomInfo-'].update(f'已连接直播间:{room.room_display_id}')
            elif status == live.LiveDanmaku.STATUS_CLOSING:
                window['-RoomInfo-'].update('正在断开连接')
            elif status == live.LiveDanmaku.STATUS_CLOSED:
                window['-RoomInfo-'].update('已断开连接')
            else:
                window['-RoomInfo-'].update('未连接直播间')

        event, values = window.read(timeout=100)
        if event =='-WINDOW CLOSE ATTEMPTED-':
            window.hide()
        if event == '-TRAY-':
            event = values[event]
            if event in ('显示窗口', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
                window.un_hide()
                window.bring_to_front()
            elif event in ('隐藏窗口', sg.WIN_CLOSE_ATTEMPTED_EVENT):
                window.hide()
                tray.show_icon()        # if hiding window, better make sure the icon is visible

        #连接直播间
        if event == '-ConnectRoom-':
            print('连接直播间')
            danmuTask = asyncio.create_task(
                BiliBiliLiveConnect.run(values['-RoomID-'], router, debug=values['-Debug-']))
            #隐藏连接按钮
            window['-ConnectRoom-'].update(visible=False)
            #显示断开连接按钮
            window['-DisconnectRoom-'].update(visible=True)

        #断开连接
        if event == '-DisconnectRoom-':
            print('断开连接')
            danmuTask.cancel()
            await BiliBiliLiveConnect.stop()
            print('danmuTask.cancel')
            #显示连接按钮
            window['-ConnectRoom-'].update(visible=True)
            #隐藏断开连接按钮
            window['-DisconnectRoom-'].update(visible=False)


        #发送模拟弹幕
        if event == '-SendDanmu-':
            print('发送模拟弹幕')
            DMSimulate.Send(router, values['-DanmuID-'], values['-DanmuSender-'], values['-DanmuContent-'])
            

        if event =='退出':
            break
        if event =='隐藏':
            window.hide()
            tray.show_icon()

        #非超时事件
        if event is not '__TIMEOUT__':
            sg.user_settings_set_entry('windowConfig', values)

    tray.close()            # optional but without a close, the icon may "linger" until moused over
    window.close()

    # for key in windowConfig:
    #     control = window[key]
    #     if control is not None:
    #         windowConfig[key] = control.get()

    #保存窗口配置
    sg.user_settings_set_entry('windowConfig', values)

    exitCallback()