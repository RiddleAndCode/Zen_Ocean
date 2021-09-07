import os

from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.config import Config
#from ocean_lib.config_provider import ConfigProvider

from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_utils.agreements.service_factory import ServiceDescriptor


config = Config('config.ini')
ocean = Ocean(config)

alice_wallet = Wallet(ocean.web3, 0x376e05899a4ae00463a3a607c774069b7d6a647860dba723f39b735c91238ddf)
b'Uau3\xc8\x96`\xe5J\xa1\x88x\xeaT\xa6[}\x01kE\xcb\xf4AQ\xdd\xb0\xc2\xb3\xb9Q\xc1\xd5'


web3 = Web

#data_token = ocean.create_data_token('DataToken1', 'DT1', alice_wallet, blob=ocean.config.metadata_store_url)
#data_token = ocean.create_data_token('DataToken1', 'DT1', alice_wallet)
#token_address = data_token.address



