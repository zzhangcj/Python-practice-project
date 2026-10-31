from app.models.user import User
from app.database import Base, engine
from app.api import api
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from app.common.exceptions import (
    BusinessException,
    business_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    # 开启docs页面
    docs_url="/docs",
    # 替换成国内可访问的CDN地址
    swagger_ui_parameters={
        "swaggerJsUrl": "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.12/swagger-ui-bundle.js",
        "swaggerCssUrl": "https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.17.12/swagger-ui.css",
    },
)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端源，不要直接写 ["*"]
    allow_credentials=True,  # ✅ 关键：允许前端携带 Authorization token
    allow_methods=["*"],  # 允许所有请求方法 GET POST PUT DELETE OPTIONS
    allow_headers=["*"],  # 允许所有请求头（包含Authorization）
)

app.include_router(api)


# 注册异常处理器
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
# 全局的异常兜底，必须放在最后注册！！
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
