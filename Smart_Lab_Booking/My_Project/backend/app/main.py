from app.models.user import User
from app.database import Base, engine
from app.api import api
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
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
