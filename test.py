import asyncio
import json
from bilibili_api import user

import grpc
import grpc_pb2_grpc





u = user.User(695002047)

# async def run_async(func):
#     info = await func()
#     print(info)

async def test_a_User_get_user_info():
    info = await u.get_user_info()
    return info


 

r = asyncio.run(test_a_User_get_user_info())
rs = json.dumps(r)
print(type(rs),rs)
# print(r,'-------------------------')
# asyncio.run(test_a_User_get_user_info())
# print('111111111111111')
# asyncio.run(test_a_User_get_user_info())
# print('22222222222')