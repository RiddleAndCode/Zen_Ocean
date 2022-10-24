from fastapi import FastAPI
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
