from datetime import datetime

from ocean_lib.agreements.service_types import ServiceTypes
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.example_config import ExampleConfig
from ocean_lib.services.service import Service
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.web3_internal.currency import to_wei
from pydantic import BaseModel


class OceanMetadata(BaseModel):
    created: str
    updated: str
    description: str
    name: str
    type: str
    author: str
    license: str
    tags: list[str]


class OceanParameters(BaseModel):
    data_url: str
    data_nft_name: str
    data_nft_symbol: str
    dt_name: str
    dt_symbol: str
    metadata: dict
    fixed_price: int


class R3COceanTokenizer:
    def __init__(self, config_path: str, walled_key: str):
        self.ocean = Ocean(get_config(config_path))
        self.wallet = Wallet(self.ocean.web3, walled_key, self.ocean.config_dict.get('BLOCK_CONFIRMATIONS'),
                             self.ocean.config_dict.get('TRANSACTION_TIMEOUT'))

    def create_data_token_by_url(self, params: OceanParameters):
        try:
            print(dir(self.wallet))
            print(self.wallet.address)
            print(self.ocean.config_dict.get('RPC_URL'))
            print(self.ocean.config_dict.get('PROVIDER_URL'))

            data_nft, data_token = self.create_base_tokens(params.data_nft_name, params.data_nft_symbol, params.dt_name, params.dt_symbol)

            token_address = data_token.address
            print(token_address)

            self.enrich_data_token_with_metadata(data_nft, data_token, params.data_url, params.metadata, token_address)
            exchange_id = self.publish_dt_to_marketplace(data_token, fixed_rate=params.fixed_price)

            print(f'DataToken @{data_token} has a `ExchangeID` available @{exchange_id}')
            return {"status": "Valid", "dt_adress": token_address}

        except Exception as e:
            print("Exception: " + str(e))
            return {"status": "NonValid", "data": str(e)}

    def enrich_data_token_with_metadata(self, data_nft, data_token, data_url, metadata, token_address):
        dataset_files = [UrlFile(url=data_url, method="GET",  headers={"content-type": "application/json"})]

        dataset_compute_service = Service(
            service_id="1",
            service_type=ServiceTypes.ASSET_ACCESS,
            service_endpoint=self.ocean.config_dict["PROVIDER_URL"],
            datatoken=data_token.address,
            files=dataset_files,
            timeout=3600,
        )
        dataset_asset = self.ocean.assets.create(
            metadata=metadata,
            publisher_wallet=self.wallet,
            files=dataset_files,
            services=[dataset_compute_service],
            data_nft_address=data_nft.address,
            deployed_datatokens=[data_token],
            wait_for_aqua=False,
        )
        print(f'"DID" is @{dataset_asset.did}')
        assert token_address == dataset_asset.datatokens[0].get("address")

    def publish_dt_to_marketplace(self, data_token, fixed_rate: int):
        data_token.mint(self.wallet.address, to_wei(200), self.wallet)
        print(data_token.address)
        exchange_id = self.ocean.create_fixed_rate(
            datatoken=data_token,
            base_token=self.ocean.OCEAN_token,
            amount=self.ocean.to_wei(200),
            fixed_rate=self.ocean.to_wei(fixed_rate),
            from_wallet=self.wallet,
        )
        return exchange_id

    def create_base_tokens(self, data_nft_name, data_nft_symbol, dt_name, dt_symbol):

        data_nft = self.ocean.create_data_nft(data_nft_name, data_nft_symbol, self.wallet)
        data_token = data_nft.create_datatoken(dt_name, dt_symbol, from_wallet=self.wallet)
        return data_nft, data_token


def get_config(address: str) -> dict:
    return ExampleConfig.get_config(address)


# if __name__ == '__main__':
#     # the market is created here.,... we have to fix this.
#     conf_path = "https://polygon-mumbai.g.alchemy.com/v2/WM8RoyN8pAUKgTswYApVeQTcKIlXWv1l"
#     wallet_private_key = "b36504e44a35cff35a9fc80df9a9cee366f2058b73fe2a3fa0deab40347125f6"
#
#     r3c_tokenizer_service = R3COceanTokenizer(conf_path, wallet_private_key)
#
#     data_url = "http://18.196.32.197:3000/get/1667815332222.json"
#     data_nft_name = "test&test-NFT"
#     data_nft_symbol = "R3C-DS-T-NFT"
#     dt_name = "test&test-Token"
#     dt_symbol = "R3C-DS-T"
#
#     date_created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
#     metadata = OceanMetadata(
#         created=date_created,
#         updated=date_created,
#         description="test&test",
#         name="test&test",
#         type="dataset",
#         author="RIDDLE&CODE",
#         license="CC0: Public Domain",
#         tags=["RiddleandCode", "CAN-Data", "Car", "Drive&Stake", "DBC"],
#     )
#
#     ocean_params = OceanParameters(data_url=data_url, data_nft_name=data_nft_name, data_nft_symbol=data_nft_symbol,
#                                    dt_name=dt_name, dt_symbol=dt_symbol, metadata=metadata, fixed_price=1)
#
#     r3c_tokenizer_service.create_data_token_by_url(params=ocean_params)
