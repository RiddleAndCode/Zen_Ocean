from fastapi import FastAPI
from pydantic import BaseModel

from os import listdir
from os.path import isfile, join

import json


tags_metadata = [
    {
        "name": "Tokenizer",
        "description": "Operations to tokenizer data on Ocean Protocol.",
    },
]

app = FastAPI()

app = FastAPI(
    title="Drive&Stake Tokenizer",
    description="This API is to tokenize data on Ocean Protocol.",
    version="0.2.0",
    openapi_tags=tags_metadata
)

    

@app.get("/configurations", tags=["Tokenizer"])
def get_token( datahash : str ):
    
    return data 

