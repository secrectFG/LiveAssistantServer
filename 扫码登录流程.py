
from bilibili_api import login, user, sync, live
import json

def saveToJson(dict, filename):
    with open(filename, 'w') as f:
        json.dump(dict, f, indent=4, ensure_ascii=False)
    return dict

credential = None

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
    credential = login.login_with_qrcode() # 使用窗口显示二维码登录
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
        exit()

print("欢迎，", sync(user.get_self_info(credential))['name'], "!")

room = live.LiveDanmaku(26705605, debug=False, credential=credential)

@room.on('DANMU_MSG')
async def on_danmaku(event):
    # 收到弹幕
    print(f'收到弹幕:',event)

@room.on('SEND_GIFT')
async def on_gift(event):
    # 收到礼物
    print(f'收到礼物:',event)

sync(room.connect())