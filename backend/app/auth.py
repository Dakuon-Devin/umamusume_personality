from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from dotenv import load_dotenv
from passlib.context import CryptContext

# 環境変数の読み込み
load_dotenv()

# パスワードハッシュ用
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2のエンドポイント
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 仮のユーザーデータベース
fake_users_db = {
    "test_user": {
        "username": "test_user",
        "full_name": "Test User",
        "hashed_password": pwd_context.hash("test_password"),
        "disabled": False,
    }
}


# ユーザーモデル
class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# 性格診断のリクエストモデル
class PersonalityQuizRequest(BaseModel):
    question1: str
    question2: str


# 性格診断のレスポンスモデル
class PersonalityQuizResponse(BaseModel):
    name: str
    personality: str
    url: str


# ユーザーデータベースからユーザーを取得
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# パスワード検証
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# ユーザー認証
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# 認証済みユーザーを取得
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(fake_users_db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user
