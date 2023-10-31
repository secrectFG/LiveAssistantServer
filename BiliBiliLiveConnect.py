
import asyncio
import os
from tkinter import messagebox
from bilibili_api import login, user, live
import json
import DanmuHandler
import QRCodeWIndow

room:live.LiveDanmaku = None
autoReconnect = False

def saveToJson(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4, ensure_ascii=False)
    return dict

async def stop():
    global room, autoReconnect
    if room is not None:
        autoReconnect = False
        try:
            await room.disconnect()
        except:
            pass

async def run(roomid, router, debug=False):
    global room, autoReconnect
    credential = None
    autoReconnect = True

    print('开始连接房间', roomid)

    while autoReconnect:
        try:
            jsondata = json.load(open("credential.json", 'r'))
            credential = login.Credential(
                sessdata=jsondata['sessdata'],
                bili_jct=jsondata['bili_jct'],
                buvid3=jsondata['buvid3'],
                dedeuserid=jsondata['dedeuserid'],
                ac_time_value=jsondata['ac_time_value']
            )
            credential.raise_for_no_bili_jct() # 判断是否成功
            credential.raise_for_no_sessdata() # 判断是否成功
        except:
            print("未找到credential.json，将重新登录")
            credential = None

        if credential is None:
            print("请登录：")
            # credential = login.login_with_qrcode_term() # 在终端扫描二维码登录
            # credential = login.login_with_qrcode() # 使用窗口显示二维码登录
            credential = await QRCodeWIndow.show()

            try:
                credential.raise_for_no_bili_jct() # 判断是否成功
                credential.raise_for_no_sessdata() # 判断是否成功
                data = {
                    "sessdata": credential.sessdata,
                    "bili_jct": credential.bili_jct,
                    "buvid3": credential.buvid3,
                    "dedeuserid": credential.dedeuserid,
                    "ac_time_value": credential.ac_time_value
                }
                saveToJson(data, "credential.json")
            except:
                print("登陆失败。。。")
                return

        # info = await user.get_self_info(credential)
        # print("欢迎，", info['name'], "!")

        room = live.LiveDanmaku(roomid, debug=False, credential=credential)
        
        DanmuHandler.RegisterHandler(room, router, debug=debug)

        

        await room.connect()
        print('连接断开，等待重连')

        try:
            credential.raise_for_no_bili_jct() # 判断是否成功
            credential.raise_for_no_sessdata() # 判断是否成功
        except:
            credential = None
            messagebox.showerror("错误", "登录失效，请重新登录")
