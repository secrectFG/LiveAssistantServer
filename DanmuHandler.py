from bilibili_api import login, user, live
import grpc_pb2 as pb2
import json


# class WrapData
#     {
#         public string JsonData { get; set; }
#         public MsgTypeEnum MsgType { get; set; }
#         public override string ToString()
#         {
#             return $"MsgType:{MsgType} JsonData:{JsonData}";
#         }
#     }

class MsgTypeEnum:
    Comment = 0
    GiftSend = 1
    GiftTop = 2
    Welcome = 3
    LiveStart = 4
    LiveEnd = 5
    Unknown = 6
    WelcomeGuard = 7
    GuardBuy = 8
    SuperChat = 9
    Interact = 10
    Warning = 11
    WatchedChange = 12



def HandleDanmuMsg(event:dict, router):

    data = dict(
        JsonData = json.dumps(event['data']),
        MsgType = MsgTypeEnum.Comment
    )
    
    msg = pb2.StringMsg(
        type='收到弹幕消息',
        jsonStr=json.dumps(data)
    )
    router.AppendMsg(msg)

def HandleGiftMsg(event:dict, router):
    
    data = dict(
        JsonData = json.dumps(event['data']),
        MsgType = MsgTypeEnum.GiftSend
    )
    
    msg = pb2.StringMsg(
        type='收到弹幕消息',
        jsonStr=json.dumps(data)
    )
    router.AppendMsg(msg)


def RegisterHandler(room:live.LiveDanmaku, router, debug):
    @room.on('DANMU_MSG')
    async def on_danmaku(event:dict):
        # 收到弹幕
        if debug:
            print(f'收到弹幕 ',event)
        HandleDanmuMsg(event, router)
        

    @room.on('SEND_GIFT')
    async def on_gift(event:dict):
        # 收到礼物
        if debug:
            print(f'收到礼物 ',event)
        HandleGiftMsg(event, router)
        # pass
        