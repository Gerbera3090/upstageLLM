# %load_ext dotenv
# %dotenv
import os
from dotenv import load_dotenv

load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")



import warnings

warnings.filterwarnings("ignore")

from langchain_upstage import UpstageLayoutAnalysisLoader

from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

layzer = UpstageLayoutAnalysisLoader("칵테일 레시피.pdf", output_type="html")
# For improved memory efficiency, consider using the lazy_load method to load documents page by page.
docs = layzer.load()


from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_upstage import ChatUpstage


llm = ChatUpstage()

prompt_template = PromptTemplate.from_template(
    """
    Please provide most correct answer from the following context. 
    Think step by step and look the html tags and table values carefully to provide the most correct answer.
    If the answer is not present in the context, please write "The information is not present in the context."
    ---
    Question: {question}
    ---
    Context: {Context}
    """
)
chain = prompt_template | llm | StrOutputParser()


text_splitter = RecursiveCharacterTextSplitter.from_language(
    chunk_size=1000, chunk_overlap=100, language=Language.HTML
)
splits = text_splitter.split_documents(docs)

retriever = BM25Retriever.from_documents(splits)

backnow = retriever.invoke("깔루아")
print(backnow)

print("#" * 50)

print(chain.invoke({"question": "깔루아가 들어가는 칵테일 레시피를 추천하면? 레시피 이름과 재료 및 그 혼합비율을 말해줘", "Context": backnow}))

