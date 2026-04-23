from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# FastAPI アプリケーション初期化
app = FastAPI(
    title="Hazard Information API",
    description="住所からハザード情報を自動取得し、Salesforce に自動入力するAPI",
    version="1.0.0"
)

# CORS 設定
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    os.getenv("FRONTEND_URL", "https://frontend-pink-xi-74.vercel.app"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルータをインポートして登録
from routers.hazard import router as hazard_router
app.include_router(hazard_router)

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Hazard Information API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
