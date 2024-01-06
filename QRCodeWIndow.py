import asyncio
import time
import uuid

import httpx
import PySimpleGUI as sg
from bilibili_api import login

from bilibili_api.utils.utils import get_api
API = get_api("login")

headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

def update_qrcode_data() -> dict:
    api = API["qrcode"]["get_qrcode_and_token"]
    url = api["url"]


    result = httpx.get(url, follow_redirects=True, headers=headers)
    print('result=',result)
    jsondic = result.json()
    qrcode_data = jsondic["data"]
    return qrcode_data

def login_with_key(key: str) -> dict:
    params = {"qrcode_key": key, "source": "main-fe-header"}
    events_api = API["qrcode"]["get_events"]
    events = httpx.get(
        events_api["url"],
        params=params,
        headers=headers,
        cookies={"buvid3": str(uuid.uuid1()), "Domain": ".bilibili.com"},
    ).json()
    return events


async def show():

    qrcode_data = update_qrcode_data()
    login_key = qrcode_data["qrcode_key"]
    qrcode_image = login.make_qrcode(qrcode_data["url"])

    # 创建一个 PySimpleGUI 窗口，并在其中显示图片
    image_elem = sg.Image(filename=qrcode_image)
    layout = [
        [image_elem],
        [sg.Text('请使用手机扫描二维码登录', key='-Status-')],
        ]
    window = sg.Window('QR Code', layout, size=(600,700))

    retry = False
    credential = None

    starttime = time.time()

    while True:
        await asyncio.sleep(0.01)
        event, values = window.read(timeout=500)

        events = login_with_key(login_key)

        if "code" in events.keys() and events["code"] == 0:
            if events["data"]["code"] == 86101:
                #更新状态
                window['-Status-'].update('请扫描二维码↑')
            elif events["data"]["code"] == 86090:
                window['-Status-'].update('请点下确认↑')
            elif events["data"]["code"] == 86038:
                window['-Status-'].update('二维码过期，请扫新二维码！')
                retry = True
                break
            elif events["data"]["code"] == 0:
                window['-Status-'].update('成功！')
                credential = login.parse_credential_url(events)
                break

            if time.time() - starttime > 120:  # 二维码有效期为120秒
                print('二维码过期')
                qrcode_data = update_qrcode_data()
                login_key = qrcode_data["qrcode_key"]
                qrcode_image = login.make_qrcode(qrcode_data["url"])
                #更新图片
                image_elem.update(filename=qrcode_image)
                
        
        if event == sg.WINDOW_CLOSED:
            break

    window.close()

    if retry:
        await show()

    return credential


