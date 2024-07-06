from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..invoke_method import invokellm
from ..recipe_load import file_load
from pydantic import BaseModel

class QuestionBase(BaseModel):
    question: str
    question_type: int




Cocktail = APIRouter(prefix="/cocktail", tags=["user"])

@Cocktail.post("/test", status_code=200)
async def Test()->JSONResponse:
    return JSONResponse({"ok":True})

@Cocktail.post("/file_reload", status_code=200)
async def file_reload():
    file_load()

@Cocktail.post("/question", status_code=200)
async def ask_question(request:QuestionBase)->str:
    question=request.question
    # TODO: 이거는 질문 종류에 따라 분리
    template = """
    Please provide most correct answer from the following context. 
    Think step by step and look the html tags and table values carefully to provide the most correct answer.
    If the answer is not present in the context, please write "The information is not present in the context."
    ---
    Question: {question}
    ---
    Context: {context}
    """
    match request.question_type:
        case 0:
            # 칵테일 추천
            ""
        case 1:
            #  
            ""
        case _:
            raise

    response = invokellm(question=question, template=template)

    # TODO: 이건 출력값
    return response