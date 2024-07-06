from langchain_upstage import UpstageEmbeddings
from langchain_upstage import UpstageLayoutAnalysisLoader
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
import time
import os

from .database import conn23c
from .config import get_setting

settings = get_setting()

def sub_file_load(file_path, table_name):
    layzer = UpstageLayoutAnalysisLoader(file_path, split="page", api_key=settings.UPSTAGE_API_KEY)

    # For improved memory efficiency, consider using the lazy_load method to load documents page by page.
    docs = layzer.load()  # or layzer.lazy_load()

    text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=1500, chunk_overlap=200, language=Language.HTML
    )
    docs = text_splitter.split_documents(docs)

    for doc in docs:
        doc.metadata['title']=table_name

    upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large")
        
    # Configure the vector store with the model, table name, and using the indicated distance strategy for the similarity search and vectorize the chunks
    s1time = time.time()

    knowledge_base = OracleVS.from_documents(docs, upstage_embeddings, client=conn23c, 
    table_name=table_name, 
    distance_strategy=DistanceStrategy.DOT_PRODUCT)

    s2time =  time.time()      
    print( f"Vectorizing and inserting chunks duration: {round(s2time - s1time, 1)} sec.")


def file_load():

    relative_path = "./cocktail_recipe.pdf"
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, relative_path)

    sub_file_load(file_path, "cocktail_recipes_test")
    # sub_file_load(file_path, "cocktail_recipes")
    
    relative_path = "./cocktail_ing.pdf"
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, relative_path)

    sub_file_load(file_path, "cocktail_ingredients_test")
    # sub_file_load(file_path, "cocktail_ingredients")

    