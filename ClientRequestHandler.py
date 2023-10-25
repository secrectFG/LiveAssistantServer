import grpc_pb2 as pb2
import json

import asyncio
from bilibili_api import user



def Handle(jsonStr):
    jsonr = json.loads(jsonStr)
    requestType = jsonr['requestType']
    if requestType=='GetBilibiliUserInfo':
        u = user.User(jsonr['userid'])
        # print(f'GetBilibiliUserInfo userid:{jsonr["userid"]}')
        async def User_get_user_info():
            info = await u.get_user_info()
            return info
        r = asyncio.run(User_get_user_info())
        return pb2.StringMsg(jsonStr=json.dumps(r))
            
    return pb2.StringMsg() 
