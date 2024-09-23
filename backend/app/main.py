from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models import PersonalityQuizRequest, PersonalityQuizResponse
from app.rag import get_umamusume_result
from app.auth import authenticate_user, get_current_user, User, fake_users_db

# FastAPIアプリケーションの初期化
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Umamusume Personality Quiz is working!"}


# トークン発行のためのエンドポイント
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": user.username, "token_type": "bearer"}


# 性格診断エンドポイント
@app.post("/api/getUmamusume", response_model=PersonalityQuizResponse)
async def get_umamusume_quiz(
    request: PersonalityQuizRequest,
    current_user: User = Depends(get_current_user)
):
    # 質問内容をまとめてRAGに渡す
    input_text = f"私は{request.question1}、{request.question2}です。"
    result = get_umamusume_result(input_text)

    # 診断結果を返す
    return PersonalityQuizResponse(
        name=result.get("name", "不明"),
        personality=result.get("personality", "不明"),
        url=result.get("url", "")
    )
