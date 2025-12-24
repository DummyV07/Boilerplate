import uvicorn

if __name__ == "__main__":
    # 这里的 app.main:app 指的是：app文件夹 -> main.py文件 -> app对象(FastAPI实例)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)