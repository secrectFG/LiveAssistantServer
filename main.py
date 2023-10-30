#python版本 3.10.9
import asyncio
import json
import sys
import grpc
import grpc_pb2 as pb2
import grpc_pb2_grpc as pb2_grpc 
import time
import os
import logging
from concurrent import futures
import threading

import ClientRequestHandler
import RouterWindow
import BiliBiliLiveConnect

logging.basicConfig(filename='server.log',
level=logging.DEBUG,
format="%(asctime)s:%(levelname)s:%(message)s",
datefmt='%Y-%m-%d %H:%M:%S')



def Log(s):
    logging.info(s)
    print(s)

class Router(pb2_grpc.LiveMessagerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.lock = threading.Lock()
        self.msgDic = {}

    def AppendMsg(self,request):
        # print('AppendMsg',request.type)
        with self.lock:
            for k in self.msgDic:
                self.msgDic[k].append(request)

    def HandleJsonMsg(self,request:pb2.StringMsg,context):
        # print('HandleJsonMsg',threading.get_ident())
        # Log(f"收到:{request} {context.peer()}")

        if request.type == 'ClientRequestHandle':
            try:
                return ClientRequestHandler.Handle(request.jsonStr)
            except Exception as e:
                Log(f"ClientRequestHandle error:{e}")
                return pb2.StringMsg(jsonStr='{"error":"'+str(e)+'"}')

        # with self.lock:
        #     for k in self.msgDic:
        #         self.msgDic[k].append(request)
        self.AppendMsg(request)
        
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






async def main():

    curpath = os.path.dirname(os.path.realpath(__file__))
    #判断是否是打包的程序
    if getattr(sys, 'frozen', False):
        # 打包程序
        print('打包程序')
        curpath = os.path.dirname(sys.executable)
    
    configpath = curpath+'/config.json'
    #读取配置文件
    config = {}
    if os.path.exists(configpath):
        with open(configpath,'r') as f:
            config = json.load(f)

    port = config.get('port',9798)

    listen_addr = f'[::]:{port}'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    router = Router()
    pb2_grpc.add_LiveMessagerServicer_to_server(router, server)
    server.add_insecure_port(listen_addr)
    server.start()
    print("Starting server on %s", listen_addr)



    def exitCallback():
        server.stop(0)
        print('Server stop')

    await RouterWindow.runWindow(exitCallback, port, router=router, logFunc=Log)
    print('RouterWindow exit')
    

if __name__ == "__main__":
    asyncio.run(main())