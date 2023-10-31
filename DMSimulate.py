
import DanmuHandler

DANMU_MSGDict = {
    'room_display_id': '13039015', 
    'room_real_id': 13039015, 
    'type': 'DANMU_MSG', 
    'data': {
        'cmd': 'DANMU_MSG', 
        'info': [
            [0, 1, 25, 16777215, 1698723702908, 0, 0, '244e31d5', 0, 9, 0, '', 0, '{}', '{}', 
                {
                    'mode': 0, 
                    'show_player_type': 0, 
                    'extra': '{"send_from_me":false,"mode":0,"color":16777215,"dm_type":0,"font_size":25,"player_mode":1,"show_player_type":0,"content":"加入黄方","user_hash":"609104341","emoticon_unique":"","bulge_display":0,"recommend_score":9,"main_state_dm_color":"","objective_state_dm_color":"","direction":0,"pk_direction":0,"quartet_direction":0,"anniversary_crowd":0,"yeah_space_type":"","yeah_space_url":"","jump_to_url":"","space_type":"","space_url":"","animation":{},"emots":null,"is_audited":false,"id_str":"3981230e624a3ead6be3cdc13665407755","icon":null,"show_reply":true,"reply_mid":0,"reply_uname":"","reply_uname_color":""}'
                }, 
                {
                    'activity_identity': '', 
                    'activity_source': 0, 
                    'not_show': 0
                }, 
            0], 
            '弹幕内容', # 弹幕内容
            [111111, # 弹幕用户ID
             'UserName', # 弹幕用户名
             0, #是否是房管
             0, #是否是VIP
             0, 10000, 1, ''], 
            [12, '头衔', '头衔所属用户', 25715293, 9272486, '', 0, 12632256, 12632256, 12632256, 0, 0, 387722139], 
            [24, 0, 5805790, '>50000', 1], 
            ['', ''], 0, 0, None, {'ts': 1698723702, 'ct': '8A17657'}, 0, 0, None, None, 0, 42, [0]], 'dm_v2': ''}}


def Send(router, userid, userName, content):
    DANMU_MSGDict['data']['info'][2][0] = userid
    DANMU_MSGDict['data']['info'][2][1] = userName
    DANMU_MSGDict['data']['info'][1] = content
    DanmuHandler.HandleDanmuMsg(DANMU_MSGDict, router)