from enum import Enum

class MsgTypeEnum(Enum):
    """消息类型枚举"""

    Comment = "弹幕"
    GiftSend = "礼物"
    GiftTop = "礼物排名"
    Welcome = "欢迎老爷"
    LiveStart = "直播开始"
    LiveEnd = "直播结束"
    Unknown = "其他"
    WelcomeGuard = "欢迎船员"
    GuardBuy = "购买船票（上船）"
    SuperChat = "SC"
    Interact = "观众互动信息"
    Warning = "超管警告"
    WatchedChange = "观看人数, 可能是人次?"

# 使用枚举
print(MsgTypeEnum.Comment)
print(MsgTypeEnum.Comment.value)