from sympy import im
import grpc
import grpc_pb2 as pb2
import grpc_pb2_grpc as pb2_grpc 
import time
import os
import logging
from concurrent import futures
import threading
import PySimpleGUI as sg
from psgtray import SystemTray
import ClientRequestHandler

logging.basicConfig(filename='server.log',
level=logging.DEBUG,
format="%(asctime)s:%(levelname)s:%(message)s",
datefmt='%Y-%m-%d %H:%M:%S')



def Log(s):
    logging.info(s)
    print(s)

class Handler(pb2_grpc.LiveMessagerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.lock = threading.Lock()
        self.msgDic = {}

    def HandleJsonMsg(self,request:pb2.StringMsg,context):
        # print('HandleJsonMsg',threading.get_ident())
        # Log(f"收到:{request} {context.peer()}")

        if request.type == 'ClientRequestHandle':
            return ClientRequestHandler.Handle(request.jsonStr)

        with self.lock:
            for k in self.msgDic:
                self.msgDic[k].append(request)
        
        return pb2.StringMsg()

    def JsonMsgRouter(self,request:pb2.Empty,context):

        peer = context.peer()
        msgList=[]
        self.msgDic[peer] = msgList

        def stop_stream():
            with self.lock:
                del self.msgDic[peer]

        context.add_callback(stop_stream)
        
        while True:
            with self.lock:
                if not peer in self.msgDic:
                    break
            if len(msgList)==0:
                time.sleep(0.1)
            else:
                with self.lock:
                    for msg in msgList:
                        yield msg
                    msgList.clear()

        Log(f"JsonMsgRouter. {peer} exit")
        # with self.lock:
        #     del self.msgDic[id]

file_path = os.path.dirname(os.path.realpath(__file__))
iconpath = file_path+'/icon.ico'

def runWindow(exitCallback):
    menu = ['', ['显示窗口', '隐藏窗口',  '---',  '退出']]
    title = '弹幕路由服务器'
    layout = [
        [sg.Text('----------------------------------------------------------')],
        [sg.B("隐藏"),sg.B("退出")]
    ]

    window = sg.Window(title, layout, finalize=True, enable_close_attempted_event=True,icon=iconpath,element_justification='c')
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=title,icon=iconpath)
    window.hide()
    while True:
        event, values = window.read(timeout=500)
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
        if event =='退出':
            break
        if event =='隐藏':
            window.hide()
            tray.show_icon()

    tray.close()            # optional but without a close, the icon may "linger" until moused over
    window.close()
    exitCallback()

def main():

    port = 17989
    listen_addr = f'[::]:{port}'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LiveMessagerServicer_to_server(Handler(), server)
    server.add_insecure_port(listen_addr)
    server.start()
    print("Starting server on %s", listen_addr)

    # _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    # try:
    #   while True:
    #     time.sleep(_ONE_DAY_IN_SECONDS)
    # except KeyboardInterrupt:
    #   server.stop(0)

    def exitCallback():
        server.stop(0)
        print('Server stop')


    runWindow(exitCallback)

    

if __name__ == "__main__":
    main()