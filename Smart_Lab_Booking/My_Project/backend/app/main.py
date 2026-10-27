from fastapi import FastAPI
from app.models.user import User
from app.database import Base, engine
from app.api import api


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

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
