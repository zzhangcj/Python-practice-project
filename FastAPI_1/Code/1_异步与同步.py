from fastapi import FastAPI
import time
import asyncio
import uvicorn

# 创建Web服务实例
app = FastAPI()

# 同步接口
@app.get("/sync")
def func_sync():
    start = time.time()
    for i in range(10):
        time.sleep(1) # 阻塞等待
    end = time.time()
    return {"time": f'{end-start:.2f}s'}

# 异步接口
@app.get("/async")
async def func_async():
    start = time.time()
    tasks = [asyncio.sleep(1) for i in range(10)]
    await asyncio.gather(*tasks)
    end = time.time()
    return {"time": f'{end-start:.2f}s'}

if __name__ == "__main__":
    # 启动服务
    uvicorn.run(app, host="127.0.0.1", port=8000)