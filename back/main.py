from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .router.cocktail_llm import Cocktail

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "DELETE",
            "PUT",
            "OPTIONS",
            "PATCH",
        ],  # "HEAD", "OPTIONS"
        allow_headers=["*"],
        expose_headers=["errorStatus"],
    )
app.include_router(Cocktail)