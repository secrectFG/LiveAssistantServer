# import asyncio
# import json
# from bilibili_api import user

# import grpc
# import grpc_pb2_grpc
# from pathlib import Path

# s = Path(__file__).parent.parent.absolute()

# print("path:",s)
# u = user.User(695002047)

# # async def run_async(func):
# #     info = await func()
# #     print(info)

# async def test_a_User_get_user_info():
#     info = await u.get_user_info()
#     return info


 

# r = asyncio.run(test_a_User_get_user_info())
# rs = json.dumps(r)
# print(type(rs),rs)
# print(r,'-------------------------')
# asyncio.run(test_a_User_get_user_info())
# print('111111111111111')
# asyncio.run(test_a_User_get_user_info())
# print('22222222222')

	# https://i2.hdslb.com/bfs/face/ba8cff1333a078b5f7b2…jpg@240w_240h_1c_1s_!web-avatar-space-header.webp
# <img class="bili-avatar-img bili-avatar-face bili-avatar-img-radius" data-src="//i2.hdslb.com/bfs/face/ba8cff1333a078b5f7b2e087d0a80ce98874a652.jpg@240w_240h_1c_1s_!web-avatar-space-header.webp" alt="" src="//i2.hdslb.com/bfs/face/ba8cff1333a078b5f7b2e087d0a80ce98874a652.jpg@240w_240h_1c_1s_!web-avatar-space-header.webp">
from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_avatar_url_from_html(html:str):
    index = html.find('@240w_240h_1c_1s_!web-avatar-space-header.webp')
    if index==-1:
        print('get_avatar_url_from_html error')
        return ''
    index2 = html.rfind('data-src="',0,index)
    url = html[index2+len('data-src="'):index]
    return url

def get_bilibili_avatar_url(uid):
    session = HTMLSession()
    r = session.get(f'https://space.bilibili.com/{uid}')

    # 这个库支持 JavaScript 渲染，所以我们需要调用这个方法
    r.html.render(timeout=60)

    # 找到头像元素并获取它的 src 属性
    # img = r.html.find('web-avatar-space-header', first=True)
    # return img.attrs['src']

    return get_avatar_url_from_html(r.html.html)

print(get_bilibili_avatar_url(8565323))