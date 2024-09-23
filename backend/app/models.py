from pydantic import BaseModel


# 性格診断クイズのリクエストデータ
class PersonalityQuizRequest(BaseModel):
    question1: str
    question2: str


# 性格診断クイズのレスポンスデータ
class PersonalityQuizResponse(BaseModel):
    name: str
    personality: str
    url: str
