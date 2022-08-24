import grpc_pb2 as pb2
import grpc_pb2_grpc as pb2_grpc 
import time
import logging
from concurrent import futures
import grpc
import threading

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
        Log(f"收到:{request} {context.peer()}")
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

        print(f"JsonMsgRouter. {peer} exit")
        # with self.lock:
        #     del self.msgDic[id]

def main():
    port = 17989
    listen_addr = f'[::]:{port}'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LiveMessagerServicer_to_server(Handler(), server)
    server.add_insecure_port(listen_addr)
    server.start()
    print("Starting server on %s", listen_addr)
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
      while True:
        time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
      server.stop(0)
    print('Server stop')

if __name__ == "__main__":
    main()