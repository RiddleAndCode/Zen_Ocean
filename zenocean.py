from ocean_lib.models import data_nft_factory
from ocean_lib.models.data_nft import DataNFT
from ocean_lib.models.data_nft_factory import DataNFTFactoryContract
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.example_config import ExampleConfig
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.ocean.util import get_address_of_type
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.models.datatoken import Datatoken
from ocean_lib.web3_internal.currency import to_wei


ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def get_config():
    config = ExampleConfig.get_config('https://eth-goerli.g.alchemy.com/v2/iNxmRj7JGw01fmAmgqh1rbAUyvhmhAmp')
    return config


def run_scenario(data_hash, data_nft_name: str, data_nft_symbol: str, dt_name: str, dt_symbol: str):
    try:
        config = ExampleConfig.get_config('https://eth-goerli.g.alchemy.com/v2/iNxmRj7JGw01fmAmgqh1rbAUyvhmhAmp')
        ocean = Ocean(config)
        wallet = Wallet(ocean.web3, "b36504e44a35cff35a9fc80df9a9cee366f2058b73fe2a3fa0deab40347125f6",
                        ocean.config_dict.get('BLOCK_CONFIRMATIONS'), ocean.config_dict.get('TRANSACTION_TIMEOUT'))
        # ConfigProvider.set_config(config)
        # Web3Provider.init_web3(provider=get_web3_connection_provider(config.network_url))
        # ContractHandler.set_artifacts_path(config.artifacts_path)

        print(dir(wallet))
        print(wallet.address)
        print(config.get('RPC_URL'))
        print(config.get('PROVIDER_URL'))

        data_nft = ocean.create_data_nft(data_nft_name, data_nft_symbol, wallet)
        data_token = data_nft.create_datatoken(dt_name, dt_symbol, from_wallet=alice_wallet)

        token_address = data_token.address
        print(token_address)

        # the market is created here.,... we have to fix this.
        date_created = "2021-03-30T10:55:11Z"
        service_attributes = {
            "main": {
                "name": "dataAssetAccessServiceAgreement",
                "creator": wallet.address,
                "timeout": 3600 * 24,
                "datePublished": date_created,
                "cost": 1.0,  # <don't change, this is obsolete>
            }
        }
        metadata = {
            "main": {
                "type": "dataset", "name": dt_name, "author": "RIDDLE&CODE",
                "license": "CC0: Public Domain", "dateCreated": date_created,
                "files": [
                    {"index": 0, "contentType": "application/json", "url": get_config()["data_url"] + data_hash},
                ],
                "name": "Drive&Stake Test CAN data"
            },
            "additionalInformation": {
                "description": 'Raw CAN data dump',
                "tags": ["RiddleandCode", "CAN-Data", "Car", "Drive&Stake", "DBC"]
            }
        }

        service_endpoint = DataServiceProvider.get_url(ocean.config_dict)
        asset = ocean.assets.create(metadata, wallet, provider_uri=[service_endpoint],
                                    data_token_address=token_address)
        assert token_address == asset.data_token_address

        data_token.mint(wallet.address, to_wei(200), wallet)
        print(data_token.address)

        ocean_token = ocean.OCEAN_token
        assert ocean_token.balanceOf(wallet.address) > 0, "need OCEAN"

        pool = ocean.pool.create(
            token_address,
            data_token_amount=to_wei(200),
            OCEAN_amount=to_wei(5),
            from_wallet=wallet
        )
        pool_address = pool.address
        print(f'DataToken @{data_token.address} has a `pool` available @{pool_address}')

        # Print values that we use in the next step

        return {"status": "Valid", "data": token_address, "pool": pool_address}

    except Exception as e:
        print("Exception: " + str(e))
        return {"status": "NonValid", "data": str(e)}


if __name__ == '__main__':
    run_scenario( "0x376e05899a4ae00463a3a607c774069b7d6a647860dba723f39b735c91238ddf", data_nft_name="Drive&Stake-NFT", data_nft_symbol="R3C-DS-T-NFT", dt_name="Drive&Stake-Token", dt_symbol="R3C-DS-T" )

