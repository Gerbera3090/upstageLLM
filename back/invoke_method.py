from langchain_upstage import ChatUpstage
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import time
from langchain_upstage import UpstageEmbeddings
from .config import get_setting
settings = get_setting()
from langchain_core.pydantic_v1 import SecretStr

# from .recipe_load import upstage_embeddings
upstage_embeddings = UpstageEmbeddings(model="solar-embedding-1-large", api_key=SecretStr(settings.UPSTAGE_API_KEY))
from .database import conn23c
llm = ChatUpstage()


# vector_store_recipes = OracleVS(client=conn23c, 
#   embedding_function=upstage_embeddings, 
#   table_name="cocktail_recipes", 
#   distance_strategy=DistanceStrategy.DOT_PRODUCT)
vector_store_recipes = OracleVS(client=conn23c, 
  embedding_function=upstage_embeddings, 
  table_name="cocktail_recipes_test", 
  distance_strategy=DistanceStrategy.DOT_PRODUCT)
# vector_store_ingredients = OracleVS(client=conn23c, 
#   embedding_function=upstage_embeddings, 
#   table_name="cocktail_ingredients", 
#   distance_strategy=DistanceStrategy.DOT_PRODUCT)


def invokellm(question, template):
    prompt = PromptTemplate.from_template(template)
    retriever_recipes = vector_store_recipes.as_retriever()
    # retriever_ingredients = vector_store_ingredients.as_retriever()

    s5time = time.time()
    print("RAG 돌리는 중입니당")
    print()
    chain = (
      {"context": retriever_recipes, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    response = chain.invoke(question)

    s6time = time.time()
    print( f"답변 시간: {round(s6time - s5time, 1)} sec. (디버깅용)")
    print("")
    return response


