from fastapi import FastAPI

from zenocean import run_scenario
from zenruntime_ocean import tokenize

tags_metadata = [
    {
        "name": "Tokenizer",
        "description": "Operations to tokenizer data on Ocean Protocol.",
    },
]

app = FastAPI(
    title="Drive&Stake Tokenizer",
    description="This API is to tokenize data on Ocean Protocol.",
    version="0.2.0",
    openapi_tags=tags_metadata
)


@app.get("/tokenize", tags=["Tokenizer"])
def get_token(data_hash: str):
    token = tokenize(data_hash)
    return {"token": token}


@app.get("/tokenize/url", tags=["Tokenizer"])
def get_token(data_url: str, data_nft_name: str, data_nft_symbol: str, dt_name: str, dt_symbol: str):
    token = run_scenario(data_url, data_nft_name, data_nft_symbol, dt_name, dt_symbol)
    return {"token": token}
