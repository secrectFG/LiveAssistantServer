import asyncio

async def async_func():
    # 在这里实现你的异步函数
    print("Hello World!")
    while True:
        print("async_func")
        await asyncio.sleep(1)


async def test():
    task = asyncio.create_task(async_func())
    while True:
        # print("main")
        await asyncio.sleep(0.1)

async def main():
    # 其他异步代码...

    # 创建新的任务并在后台运行
    
    # 等待任务完成
    # await task

    # 其他异步代码...
    print("test")

    await test()



# 运行 main 函数
asyncio.run(main())