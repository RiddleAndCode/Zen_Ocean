from fastapi import FastAPI

from zenocean import R3COceanTokenizer, OceanParameters

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

CONF_PATH = "https://polygon-mumbai.g.alchemy.com/v2/WM8RoyN8pAUKgTswYApVeQTcKIlXWv1l"
WALLET_PRIVATE_KEY = "b36504e44a35cff35a9fc80df9a9cee366f2058b73fe2a3fa0deab40347125f6"

r3c_tokenizer_service = R3COceanTokenizer(CONF_PATH, WALLET_PRIVATE_KEY)


@app.post("/tokenize/url", tags=["Tokenizer"], )
def create_token_with_url(params: OceanParameters):
    token = r3c_tokenizer_service.create_data_token_by_url(params)
    return {"token": token}
